from enum import Enum


class StackType(Enum):
    DATA = 1
    RETURN = 2


class Stack:
    def __init__(self, size: int, cpu):
        self.size = size
        self.cpu = cpu

    def push(self, stack_type: StackType = StackType.DATA, value: int = None):
        stack = self.cpu.data_stack if stack_type == StackType.DATA else self.cpu.return_stack
        pointer = self.cpu.registers.sp if stack_type == StackType.DATA else self.cpu.registers.sp

        if value is None:
            value = self.cpu.registers.a

        if pointer + 1 < self.size:
            pointer += 1
            stack[pointer] = value
            if stack_type == StackType.DATA:
                self.cpu.registers.sp = pointer
                self.cpu.registers.tos = value
            else:
                self.cpu.registers.rp = pointer

    def pop(self, stack_type: StackType = StackType.DATA):
        stack = self.cpu.data_stack if stack_type == StackType.DATA else self.cpu.return_stack
        pointer = self.cpu.registers.sp if stack_type == StackType.DATA else self.cpu.registers.sp
        if pointer >= 0:
            pointer -= 1
            if stack_type == StackType.DATA:
                self.cpu.registers.sp = pointer
                self.cpu.registers.tos = stack[pointer] if pointer >= 0 else 0
            else:
                self.cpu.registers.rp = pointer
