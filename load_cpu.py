from stack_machine.cpu.cpu import cpu
from stack_machine.cpu.mc.mc import mc
from stack_machine.cpu.mem.data_mem import data_mem
from stack_machine.cpu.mem.inst_mem import inst_mem

def load_cpu() -> cpu:
    # 0b0_0000000_00_000000
    mc_: list[mc] = [ # manually setting up microcommands, u can make beautiful constructor for mc class and it'll be readable
        #               w|n |&-+ba
        mc(0b0_000110010_00_000111),  # 0 | A + B -> T
        mc(0b1_000000000_00_000000),  # 1 | term
        mc(0b0_000010001_11_000111),  # 2 | imm -> B; T -> A; mem[B + A] -> T
        mc(0b1_000000000_00_000000),  # 3 | term
        mc(0b0_000010001_01_000111),  # 4 | imm -> B; T -> A; S -> mem[B + A]
        mc(0b1_000000000_00_000000),  # 5 | term
        mc(0b0_000110010_00_000111),  # 6 | T -> A; S -> B; A + B ->T
        mc(0b1_000000000_00_000000),  # 7 | term
        mc(0b0_000000100_00_000000),  # 8 | pop
        mc(0b1_000000000_00_000000),  # 9 | term
        mc(0b0_000000011_00_000110),  # 10| imm -> B; B + 0 -> T
        mc(0b1_000000000_00_000000),  # 11| term
        mc(0b0_100000000_00_000000),  # 12| halt
        mc(0b1_000000000_00_000000),  # 13| term
        mc(0b0_000000010_00_000101),  # 14| A -> T
        mc(0b1_000000000_00_000000),  # 15| term
    ]
    inst = [ # manually setting up instructions
        # imm                      mc_addr
        0b000011111111111111111111_00001010,   # li 0b1111                               stack: [0b1111]
        0b000000000000000001001011_00001010,   # li 0b1011                               stack: [0b1011, 0b1111]
        0b000000000000000000000000_00000000,   # sum_top                                 stack: [sum, 0b1011, 0b1111]
        0b000000000000000000010000_00001010,   # li 0b10000 (it's 'gonna be an address)  stack: [0b10000, sum, 0b1011, 0b1111]
        0b000000000000000000000000_00000100,   # T -> A; imm -> B; S -> mem[A + B]       writing
        0b000000000000000000000000_00001000,   # pop                                     stack: [sum, 0b1011, 0b1111]
        0b000000000000000000000000_00001000,   # pop                                     stack: [0b1011, 0b1111]
        0b000000000000000000000000_00001000,   # pop                                     stack: [0b1111]
        0b000000000000000000000000_00001000,   # pop                                     stack: []
        0b000000000000000000010000_00001010,   # li 0b10000 (let's try to read that shit)stack: [0b10000]
        0b000000000000000000000001_00000010,   #(i'll read it with one byte displacement)stack: [0b10000]
        0b000000000000000000000000_00001110,   # push A (mem is in a right now)          stack: [mem, 0b10000]
        0b000000000000000000000000_00001000,   # pop                                     stack: [0b10000]
        0b000000000000000000000000_00001000,   # pop                                     stack: []
        0b000000000000000000000000_00001100,   # halt
    ]
    i_mem = inst_mem(inst)
    mem = data_mem(32, [80, 84], [1, 2, 3, 4, 5])
    return cpu(8, mem, i_mem, mc_)