# по факту просто обертка вокруг инта с форматом, при желании можно вынести формат в конфиг и сделать фактори интов
class inst:
    def __init__(self, val: int):
        self.mc_addr = [0, 7]
        self.imm = [8, 31]
        self.bits = val