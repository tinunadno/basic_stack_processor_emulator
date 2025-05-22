from cpu.cu.signals import *
from utils.logs import logger


class Opcode(Enum):
    # стек
    LIT  = 0b0001_0001  # datastack.push(<value>)
    DUP  = 0b0001_0010  # datastack.push(tos)
    SWAP = 0b0001_0011  # A <- datastack.pop(), B <- datastack.pop(), datastack.push(A), datastack.push(B)
    DROP = 0b0001_0100  # datastack.pop()

    # alu
    #   - arithmetic
    ADD = 0b0000_0001  # datastack.push(datastack.pop() + datastack.pop() + C)
    SUB = 0b0000_0010  # datastack.push(datastack.pop() - datastack.pop())
    MUL = 0b0000_0011  # a * b
    DIV = 0b0000_0100  # a / b
    #   - logic
    AND = 0b0000_0101  # a & b
    OR  = 0b0000_0110  # a | b
    NOT = 0b0000_0111  # not tos
    SHL = 0b0000_1000  # tos >> 1
    SHR = 0b0000_1001  # tos << 1

    # memory access
    LD_ADDR             = 0b0010_0001  # datastack.push(mem[<value>])
    LD_ADDR_A           = 0b0010_0010  # datastack.push(mem[A])
    LD_ADDR_A_PLUS      = 0b0010_0011  # datastack.push(mem[A]), A++
    LD_ADDR_B           = 0b0010_0001  # datastack.push(mem[B])
    ST_ADDR_A           = 0b0010_0010  # mem[A] <- datastack.pop()
    ST_ADDR_A_PLUS      = 0b0010_0011  # mem[A] <- datastack.pop(), А++
    ST_ADDR_B           = 0b0010_0100  # mem[B] <- datastack.pop()
    ST_A                = 0b0010_0101  # A <- datastack.pop()
    ST_B                = 0b0010_0110  # B <- datastack.pop()
    A                   = 0b0010_0111  # datastack.push(A)

    # control
    HALT = 0b0000_0011



class Decoder:
    instructions = {
        Opcode.LIT: [
            (DataStackSignals.NAME, DataStackSignals.STACK_PUSH_BUFFER)
        ],
        Opcode.LD_ADDR: [
            (LoadSignals.NAME, LoadSignals.MEM_BUFFER_LOAD),
            (DataStackSignals.NAME, DataStackSignals.STACK_PUSH_BUFFER)
        ],
        Opcode.ADD: [
            (LoadSignals.NAME, LoadSignals.LOAD_TOS_A),
            (DataStackSignals.NAME, DataStackSignals.STACK_POP),
            (LoadSignals.NAME, LoadSignals.LOAD_TOS_B),
            (DataStackSignals.NAME, DataStackSignals.STACK_POP),
            (AluSignals.NAME, AluSignals.ADD),
            (DataStackSignals.NAME, DataStackSignals.STACK_PUSH)
        ],
        Opcode.HALT: [
            (ControlSignals.NAME, ControlSignals.HALT)
        ]
    }

    def get_instruction(self, opcode: hex):
        for op in Opcode:
            if op.value == opcode:
                return self.instructions.get(op, [])
        else:
            logger.error("Undefined opcode")
