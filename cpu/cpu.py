from cpu.alu import Alu
from cpu.cu.control_unit import ControlUnit

from cpu.mem import DataMem, InstructionMem
from cpu.registers import Registers
from cpu.stack import Stack
from utils.logs import logger
from cpu.cu.signals import *


class CPU:

    def __init__(self, data_memory_size: int = 256, instruction_memory_size: int = 256):
        self.data_memory: DataMem = DataMem(data_memory_size)
        self.instruction_memory: InstructionMem = InstructionMem(instruction_memory_size)

        self.alu: Alu = Alu(self)

        self.data_stack = [0x0] * (data_memory_size // 2)
        self.return_stack = [0x0] * (data_memory_size // 2)

        self.stack: Stack = Stack(data_memory_size // 2, self)

        self.registers: Registers = Registers()
        self.control_unit: ControlUnit = ControlUnit()

        self.instruction: hex = None
        self.opcode: hex = None
        self.buffer: hex = None

    def execute_micro_step(self):
        category, step = self.control_unit.microcode_steps[self.control_unit.microcode_index]
        if category in self.control_unit.micro_command_rom.micro_ops and \
                step in self.control_unit.micro_command_rom.micro_ops[category]:
            self.control_unit.micro_command_rom.get(category, step)(self)
            logger.info(f"Micro-op: {step}")
        else:
            logger.error(f"Undefined Micro-op: {category} {step}")

        self.control_unit.microcode_index += 1
        if self.control_unit.microcode_index >= len(self.control_unit.microcode_steps):
            return False
        return True

    def run(self):
        self.control_unit.running = True
        logger.info(f"Program start running")

        self.control_unit.cycle()

        while self.control_unit.is_running():
            logger.info(f" --- tact: {self.control_unit.tact} ---")

            if self.control_unit.signals[ControlSignals.FETCH_DECODE]:
                logger.info(f" --- new instruction ---")
                self.instruction = self.instruction_memory.read(self.registers.pc)
                if self.instruction is None:
                    self.control_unit.set_signal(ControlSignals.HALT, 1)
                    break
                self.registers.pc += 1
                logger.info(f"Load instruction: {self.instruction}")

                self.opcode = self.instruction >> 24
                self.buffer = self.instruction & 0x00FF_FFFF
                self.control_unit.microcode_steps = self.control_unit.get_microcode(self.opcode)
                self.control_unit.microcode_index = 0
                logger.info(f"Decode instruction: {self.control_unit.microcode_steps_to_str()}")
                logger.info(f"Decode buffer: {self.buffer}")

            if self.control_unit.signals[ControlSignals.EXECUTE]:
                logger.info(f"Executing")
                if not self.execute_micro_step():
                    self.control_unit.set_signal(ControlSignals.EXECUTE, 0)
            self.control_unit.cycle()
            logger.info(f"PC: {self.registers.pc}, Data Stack: {self.data_stack[:self.registers.sp + 1]}, "
                        f"Return Stack: {self.return_stack[:self.registers.rp + 1]}, "
                        f"A: {self.registers.a}, B: {self.registers.b}, TOS: {self.registers.tos}, "
                        f"C: {self.registers.c}, V: {self.registers.v}")
