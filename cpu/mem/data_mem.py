# просто пара удобных функций вокруг bytearray
class data_mem:
    def __init__(self, size: int):
        self.mem = bytearray(size)
        self.size = size
    def write(self, address: int, value: int) -> None:
        if address <= self.size - 4:
            for i in range(4):
                self.mem[address + i] = (value & 0xFF)
                value >>= 8
        else:
            raise ValueError("Attempting to write memory out of address space")
    def write_byte(self, address: int, value: int) -> None:
        if address < self.size:
            self.mem[address] = (value & 0xFF)
        else:
            raise ValueError("Attempting to write memory out of address space")
    def read_byte(self, address: int) -> int:
        if address < self.size:
            return self.mem[address]
        else:
            raise ValueError("Attempting to read memory out of address space")
    def read(self, address: int) -> int:
        if address <= self.size - 4:
            ret = 0
            for i in range(4, 0, -1):
                ret <<= 8
                ret |= self.mem[address + i - 1]
            return ret
        else:
            raise ValueError("Attempting to read memory out of address space")