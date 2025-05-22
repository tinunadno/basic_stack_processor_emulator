from cpu.cu.decoder import Opcode


def assemble(source: str) -> list[hex]:
    result = []
    for line in source.strip().splitlines():
        line = line.strip()
        if not line or line.startswith(';'):
            continue
        parts = line.split()
        instr = parts[0].upper()

        try:
            opcode = Opcode[instr]
        except KeyError:
            raise ValueError(f"Unknown instruction: {instr}")

        if opcode == Opcode.LIT or opcode == Opcode.LD_ADDR:
            if len(parts) != 2:
                raise ValueError(f"{instr} requires a value")
            value = int(parts[1])
            word = (opcode.value << 24) | (value & 0xFFFFFF)
        else:
            word = opcode.value << 24

        result.append(word)
    return result
