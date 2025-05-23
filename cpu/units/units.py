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
        signals = {
            "open_a": get_int_cut(sig.val, self.open_a) == 1,
            "open_b": get_int_cut(sig.val, self.open_b) == 1,
            "add": get_int_cut(sig.val, self.add) == 1,
            "sub": get_int_cut(sig.val, self.sub) == 1,
            "and": get_int_cut(sig.val, self.and_) == 1,
            "or": get_int_cut(sig.val, self.or_) == 1,
        }
        a = 0
        b = 0
        # по аналогии можешь добавить !!!!ВАЖНО!!!! НЕ ЗАБУДЬ ПРО ФОРМАТ МК КОГДА БУДЕШЬ ДОБАВЛЯТЬ
        if signals["open_a"]:
            a = cpu_.get_reg("A")
        if signals["open_b"]:
            b = cpu_.get_reg("B")
        if signals["add"]:
            return a + b
        if signals["sub"]:
            return a - b
        if signals["and"]:
            return a & b
        if signals["or"]:
            return a | b
        return 0

# если читает, кладет в A. адрес берется из imm (из инструкции) и верхушки стэка
class mem_unit:
    def __init__(self):
        self.need_mem = [0]
        self.write_read = [1]
    def handle(self, sig: common_signal, cpu_: cpu):
        signals = {
            "need_mem": get_int_cut(sig.val, self.need_mem) == 1,
            "write_read": get_int_cut(sig.val, self.write_read) == 1
        }
        if not signals["need_mem"]:
            return
        # тут можешь поменять что куда пишет и добавить еще какихнить функций
        if not signals["write_read"]:
            # eg write
            addr = cpu_.last_alu_output
            val = cpu_.data_stack.get_S()
            cpu_.mem.write(addr, val)
        else:
            addr = cpu_.last_alu_output
            val = cpu_.mem.read(addr)
            cpu_.set_reg("A", val)

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
        while get_int_cut(current_mc.bits, current_mc.term_mc) == 0:
            ret_sig.append([common_signal(get_int_cut(current_mc.bits, current_mc.alu_sig)),
                            common_signal(get_int_cut(current_mc.bits, current_mc.mem_sig)),
                            common_signal(get_int_cut(current_mc.bits, current_mc.other)),
                            ])
            mc_addr += 1
            current_mc = cpu_.mc_mem[mc_addr]
        cpu_.set_reg("PC", inst_addr+1)
        return imm, ret_sig