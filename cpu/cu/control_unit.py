from cpu.cu.decoder import Decoder
from cpu.cu.micro_command_rom import MicroCommandROM
from cpu.cu.signals import *
from utils.logs import logger


class ControlUnit:


    def __init__(self):
        # добавляем все сигналы
        signal_classes = [ControlSignals, AluSignals, DataStackSignals, LoadSignals]
        self.signals = {}
        for signal_class in signal_classes:
            for signal in signal_class:
                self.signals[signal] = 0

        self.current_micro_step = 0
        self.current_instruction = None
        self.microcode_steps = []
        self.microcode_index = 0
        self.running = False
        self.tact = 0

        # база микрокоманд
        self.micro_command_rom: MicroCommandROM = MicroCommandROM()

        # декодер инструкции в микрокомманды
        self.decoder: Decoder = Decoder()

    def set_signal(self, signal, value):
        self.signals[signal] = value

        if signal == ControlSignals.EXECUTE and value == 0:
            self.current_micro_step = 0

    def cycle(self):
        if self.signals[ControlSignals.HALT]:
            self.running = False

        self.tact += 1

        if self.current_micro_step == 0:
            self.set_signal(ControlSignals.FETCH_DECODE, 1)
            self.current_micro_step = 1
        elif self.current_micro_step == 1:
            self.set_signal(ControlSignals.FETCH_DECODE, 0)
            self.set_signal(ControlSignals.EXECUTE, 1)

            if self.microcode_index >= len(self.microcode_steps):
                self.current_micro_step = 0

    def get_microcode(self, opcode):
        return self.decoder.get_instruction(opcode)

    def is_running(self):
        return self.running

    def microcode_steps_to_str(self) -> str:
        text = ""
        for step in self.microcode_steps:
            text += step[1].name + " "
        return text
