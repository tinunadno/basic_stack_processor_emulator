from csa_4th_lab.new.common_utils.bitwise_utils import set_int_cut
from mc import microcommand

class ALU_signal:
    def __init__(self, val: int | None):
        # подумать над размером
        self.bits = [0 for i in range(1)]
        self.signal_range = [0, 31]
        # итд
        self.add_bits = [0]

    # получаем срез из мк
    def set_ALU_signal(self, signals: int):
        # тут просто устанавливаем сигнал
        self.bits = set_int_cut(self.signal_range, int)

class decoder:
    def __init__(self, microcommands: list[microcommand]):
        self.mc = microcommands

    # тут подставляй сигнал
    def perform_decode(self, command: int):
        mc_index = 0
        while 1:
            if self.mc[mc_index].is_jump_bit:
                # тут подумай, как сделать переход, либо в комманду, либо доп логика в мк
                mc_index = 111
            while not self.mc[mc_index].is_term_bit():
                alu_sig = ALU_signal() # тут ставишь сигнал из мк
                # заполняешь остальные сигналы
                # перформишь execute или типа того
                mc_index += 1
