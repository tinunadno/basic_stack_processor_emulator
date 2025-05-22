from cpu.cu.signals import AluSignals


class Alu:
    def __init__(self, cpu):
        self.cpu = cpu
        self.operations = {
            AluSignals.NOP:     self.nop,
            AluSignals.ADD: self.add,

        }

    def nop(self):
        self.cpu.registers.a = self.cpu.buffer

    def add(self):
        result: hex = self.cpu.registers.a + self.cpu.registers.b
        self.cpu.registers.c = 1 if result > 0xFFFF else 0
        self.cpu.registers.v = 1 if (self.cpu.registers.a > 0 > result and self.cpu.registers.b > 0) else 0
        self.cpu.registers.a = result

    def execute(self, signal):
        if signal in self.operations:
            self.operations[signal]()
        else:
            raise ValueError(f'Invalid signal: {signal}')

    def add_new_signal(self, signal, func):
        self.operations[signal] = func
