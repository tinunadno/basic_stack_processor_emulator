from bit_utils import get_int_cut

class microcommand:
    # можно сделать удобный конструктор
    # например по аналогии с твоими установками мк, только через сеттеры, или по именам
    def __init__(self):
        # тут конфигурируется формат мк
        self.bits = [0 for i in range(1)] # тут подумай, сколько понадобиться битов
        self.is_jump_bit = [31]
        self.alu_bits = [15, 29]
        self.mem_nits = [10, 14]   # тут подумай, как их лучше определить
        self.bit_match = [0, 5]
        self.is_term_bit = [30]
                                  # адрес перехода можно кодировать в сами комманды, их немного
    def get_is_jump(self):
        return get_int_cut(self.bits, self.is_jump_bit)
    def get_alu_signals(self):
        return get_int_cut(self.bits, self.alu_bits)
    def is_term_bit(self):
        return get_int_cut(self.bits, self.is_term_bit)
    # и дальше по аналогии
    #! ВАЖНО подумай над форматом мк