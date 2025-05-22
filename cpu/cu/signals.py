from enum import Enum


class AluSignals(Enum):
    NAME = "ALU"
    VECTOR_MODE = "VECTOR_MODE"

    NOP = "NOP"

    # логические
    AND = "AND"
    OR = "OR"
    NOT = "NOT"

    # арифмитические
    ADD = "ADD"
    MUL = "MUL"
    DIV = "DIV"
    INC = "INC"

    # сдвиги
    LEFT_SHIFT = "LEFT_SHIFT"
    RIGHT_SHIFT = "RIGHT_SHIFT"
    RIGHT_AR_SHIFT = "RIGHT_AR_SHIFT"

    # сравнения
    CMP = "CMP"


class DataStackSignals(Enum):
    NAME = "DATA_STACK"

    STACK_PUSH = "STACK_PUSH"
    STACK_PUSH_BUFFER = "STACK_PUSH_BUFFER"
    STACK_POP = "STACK_POP"


class ReturnStackSignals(Enum):
    NAME = "RET_STACK"

    RETURN_PUSH = "RETURN_PUSH"
    RETURN_POP = "RETURN_POP"


class ControlSignals(Enum):
    NAME = "CONTROL"
    FETCH = "FETCH"
    DECODE = "DECODE"
    FETCH_DECODE = "FETCH_DECODE"
    EXECUTE = "EXECUTE"
    HALT = "HALT"


class LoadSignals(Enum):
    NAME = "LOAD"

    LOAD_BUFFER_A = "LOAD_BUFFER_A"
    LOAD_TOS_A = "LOAD_TOS_A"
    LOAD_TOS_B = "LOAD_TOS_B"

    MEM_BUFFER_LOAD = "MEM_BUFFER_LOAD"
    MEM_A_LOAD = "MEM_A_LOAD"
    MEM_B_LOAD = "MEM_B_LOAD"
