from typing import List, Dict


class Memory:

    def __init__(self, size: int):
        self.mem: List[hex] = [0x0]
        self.size = size
        self.mem *= size

    def write(self, pos: hex, val: hex):
        if int(pos) > self.size or int(pos) < self.size:
            raise ValueError("Pos out of bounds")
        self.mem[int(pos)] = val

    def read(self, pos: hex) -> hex:
        pos = int(pos)
        if pos > self.size or pos < 0x0:
            raise ValueError("Pos out of bounds")
        return self.mem[pos]

    def print_mem(self):
        for i in range(len(self.mem)):
            print(hex(i), hex(self.mem[i]))


class DataMem(Memory):
    def write_memory(self, mem: Dict[hex, hex]):
        for word in mem:
            self.mem[word] = mem[word]


class InstructionMem(Memory):
    def write_program(self, prog: List[hex]):
        self.mem[:len(prog)] = prog
