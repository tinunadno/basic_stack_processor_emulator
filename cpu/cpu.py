from csa_4th_lab.src.common_utils.bitwise_utils import get_int_cut
from stack_machine.cpu.mc.mc import mc
from stack_machine.cpu.mem.data_mem import data_mem
from stack_machine.cpu.mem.inst_mem import inst_mem
from stack_machine.cpu.signals.signals import common_signal
from stack_machine.cpu.stack.stack import stack


class cpu:
    def __init__(self, stack_size: int, mem: data_mem, i_mem: inst_mem, mc_mem: list[mc], ep: int):
        self.data_stack = stack(stack_size)
        self.ret_stack = stack(stack_size)
        self.mem = mem
        self.i_mem = i_mem
        self.regs = [0 for i in range(4)]
        self.reg_names = {
            "A": 0,
            "B": 1,
            "PC": 2,
            "I": 3
        }
        self.set_reg("PC", ep)
        # тут получился циклический импорт, но ты на пэкэджи все равно переделаешь, так что не буду заморачиваться
        from stack_machine.cpu.units.units import alu_unit, mem_unit, decoder_unit
        self.alu = alu_unit()
        self.mem_unit = mem_unit()
        self.decoder = decoder_unit()
        self.last_alu_output = 0
        self.mc_mem = mc_mem
        self.tick_count = 0
        self.running = True

    def tick(self):
        imm, tick_signals = self.decoder.handle(self)
        for i in tick_signals:
            self.tick_count += 1
            if self.tick_count == 11:
                a = 1
            other: common_signal = i[2]

            cpu_signals = other.val
            # в тупую интерпритируем сигналы
            if "load_imm" in cpu_signals:
                self.set_reg("B", imm)
            if "load_T_a" in cpu_signals:
                self.set_reg("A", self.data_stack.get_T())
            if "load_T_b" in cpu_signals:
                self.set_reg("B", self.data_stack.get_T())
            if "load_S" in cpu_signals:
                self.set_reg("B", self.data_stack.get_S())
            if "load_PC" in cpu_signals:
                self.set_reg("A", self.get_reg("PC"))
            self.last_alu_output = self.alu.handle(i[0], self)
            self.mem_unit.handle(i[1], self)
            if "fetch_pc" in cpu_signals:
                self.set_reg("PC", self.last_alu_output)
            if "push_stack" in cpu_signals:
                self.data_stack.push(self.last_alu_output)
            if "pop_stack" in cpu_signals:
                self.data_stack.pop()
            if "call" in cpu_signals:
                self.ret_stack.push(self.get_reg("PC"))
                self.set_reg("PC", self.last_alu_output)
            if "restore_pc" in cpu_signals:
                self.set_reg("PC", self.ret_stack.get_T())
                self.ret_stack.pop()
            if "over" in cpu_signals:
                self.data_stack.over()
            if "kill_cpu" in cpu_signals:
                self.running = False
        # a bit of readabl code
        cpu_condition = f"""tick {self.tick_count}
A  {self.regs[0]}
B  {self.regs[1]}
PC {self.regs[2]}
I  {self.regs[3]}
MEM {self.mem.mem}
data_stack {self.data_stack.stack}"""
        print(cpu_condition)
        print()
        print()




    def get_reg(self, reg: int | str):
        if isinstance(reg, str):
            reg = self.reg_names[reg]
        return self.regs[reg]
    def set_reg(self, reg: [int|str], val: int):
        if isinstance(reg, str):
            reg = self.reg_names[reg]
        self.regs[reg] = val