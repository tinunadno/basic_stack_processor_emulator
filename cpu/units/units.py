from stack_machine.cpu.cpu import cpu
from stack_machine.cpu.signals.signals import common_signal
from stack_machine.utils.bitwise_utils import get_int_cut
from stack_machine.cpu.instruction.instruction import inst

# в тупую интерпритирует сигналы
class alu_unit:
    def __init__(self):
        # по аналогии можешь добавить
        self.open_a = [0]
        self.open_b = [1]
        self.add = [2]
        self.sub = [3]
        self.and_ = [4]
        self.or_ = [5]
    def handle(self, sig: common_signal, cpu_: cpu):
        signals = sig.val
        a = 0
        b = 0
        # по аналогии можешь добавить !!!!ВАЖНО!!!! НЕ ЗАБУДЬ ПРО ФОРМАТ МК КОГДА БУДЕШЬ ДОБАВЛЯТЬ
        if "open_a" in signals:
            a = cpu_.get_reg("A")
        if "open_b" in signals:
            b = cpu_.get_reg("B")
        if "add" in signals:
            return a + b
        if "sub" in signals:
            return a - b
        if "and" in signals:
            return a & b
        if "or" in signals:
            return a | b
        return 0

# если читает, кладет в A. адрес берется из imm (из инструкции) и верхушки стэка
class mem_unit:
    def __init__(self):
        self.need_mem = [0]
        self.write_read = [1]
    def handle(self, sig: common_signal, cpu_: cpu):
        signals = sig.val
        if not "do_mem" in signals:
            return
        # тут можешь поменять что куда пишет и добавить еще какихнить функций
        if not "read" in signals:
            # eg write
            addr = cpu_.last_alu_output
            val = cpu_.data_stack.get_T()
            cpu_.mem.write(addr, val)
        else:
            addr = cpu_.last_alu_output
            val = cpu_.mem.read(addr)
            cpu_.data_stack.push(val)

# смотри на аддрес мк (в самой инструкции) и набивает список сигналов
class decoder_unit:
    def handle(self, cpu_: cpu) -> [int, list[list[common_signal]]]:
        inst_addr = cpu_.get_reg("PC")
        inst_ = inst(cpu_.i_mem.get_inst(inst_addr))
        imm = get_int_cut(inst_.bits, inst_.imm)
        mc_addr = get_int_cut(inst_.bits, inst_.mc_addr)
        # тут если хочешь, можешь добавить более сложную логику fetcha, но в формате инструкции заложено 255 мк, а этого хватит
        current_mc = cpu_.mc_mem[mc_addr]
        ret_sig = []
        while not "term_mc" in current_mc.get_signal("mc"):
            ret_sig.append([common_signal(current_mc.get_signal("alu")),
                            common_signal(current_mc.get_signal("mem")),
                            common_signal(current_mc.get_signal("cpu")),
                            ])
            mc_addr += 1
            current_mc = cpu_.mc_mem[mc_addr]
        cpu_.set_reg("PC", inst_addr+1)
        return imm, ret_sig