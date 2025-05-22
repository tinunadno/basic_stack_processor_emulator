
class Registers:
    def __init__(self):
        self.a: hex = 0x0
        self.b: hex = 0x0
        self.tos: hex = 0x0
        self.ps: hex = 0x0
        self.pc: hex = 0x0
        self.sp: hex = -1
        self.rp: hex = -1
        self.c: hex = 0x0
        self.v: hex = 0x0
