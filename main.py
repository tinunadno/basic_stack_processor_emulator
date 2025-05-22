from typing import List, Dict

from cpu.cpu import CPU
from utils.translator import assemble


def main():
    cpu: CPU = CPU()

    program = """
        LD_ADDR 10
        LIT 20
        ADD
        HALT
    """

    prog: List[hex] = assemble(program)

    print(prog)

    mem: Dict[hex, hex] = {
        0x0A: 0x0000_000B,
        0x0B: 0x0000_000C,
    }

    cpu.instruction_memory.write_program(prog=prog)
    cpu.data_memory.write_memory(mem=mem)

    cpu.run()

    pass


if __name__ == '__main__':
    main()
