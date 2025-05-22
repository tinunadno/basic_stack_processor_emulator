from cpu.cu.signals import ControlSignals, DataStackSignals, AluSignals, LoadSignals, ReturnStackSignals


class MicroCommandROM:
    # микрокоманды
    micro_ops = {
        ControlSignals.NAME: {
            ControlSignals.HALT: lambda cpu: cpu.control_unit.set_signal(ControlSignals.HALT, 1),
        },
        DataStackSignals.NAME: {
            DataStackSignals.STACK_PUSH: lambda cpu: cpu.stack.push(),  # пушиться значние a в стек
            DataStackSignals.STACK_PUSH_BUFFER: lambda cpu: cpu.stack.push(value=cpu.buffer),
            DataStackSignals.STACK_POP: lambda cpu: cpu.stack.pop(),    # поп значения из стека
        },
        ReturnStackSignals.NAME: {
            ReturnStackSignals.RETURN_PUSH: lambda cpu: cpu.stack.push("return"),
            ReturnStackSignals.RETURN_POP: lambda cpu: cpu.stack.pop("return"),
        },
        AluSignals.NAME: {
            AluSignals.ADD: lambda cpu: cpu.alu.execute(AluSignals.ADD),
            AluSignals.NOP: lambda cpu: cpu.alu.execute(AluSignals.NOP),
        },
        LoadSignals.NAME: {
            # загрузка операнда в a
            LoadSignals.LOAD_BUFFER_A: lambda cpu: setattr(cpu.registers, "a", cpu.buffer),

            # загрузка вершины стека в a
            LoadSignals.LOAD_TOS_A: lambda cpu: setattr(cpu.registers, "a", cpu.registers.tos),

            # загрузка вершины стека в b
            LoadSignals.LOAD_TOS_B: lambda cpu: setattr(cpu.registers, "b", cpu.registers.tos),

            # загрузить значение по адресу в buffer-e в buffer
            LoadSignals.MEM_BUFFER_LOAD: lambda cpu: setattr(cpu, "buffer",
                                                              cpu.data_memory.read(cpu.buffer)),

            # загрузить значение по адресу в регистре a в buffer
            LoadSignals.MEM_A_LOAD: lambda cpu: setattr(cpu, "buffer",
                                                              cpu.data_memory.read(cpu.registers.a)),

            # загрузить значение по адресу в регистре b в buffer
            LoadSignals.MEM_B_LOAD: lambda cpu: setattr(cpu, "buffer",
                                                              cpu.data_memory.read(cpu.registers.b)),
        }
    }

    def get(self, category, signal):
        return self.micro_ops[category][signal]
