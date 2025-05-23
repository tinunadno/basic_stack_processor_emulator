# тоже по факту обертка над интом, можно вынести форматы в конфиг, и сделать фабрику
class mc:
    def __init__(self, mc_val: int):
        self.alu_sig = [0, 5]   # open a, open b, add sub and or You can add watever you want to
        self.mem_sig = [6, 7]   # need_mem, write\read (write's T, readt to A, adress is always ALU result)
        self.other = [8, 16]    # other cpu signals
        self.term_mc = [17]
        self.bits = mc_val