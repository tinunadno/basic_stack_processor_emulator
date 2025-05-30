# просто обертка, ее можно убрать (пока делал, думал, что понадобится доп функционал)
class common_signal:
    def __init__(self, sig: dict[str, bool]):
        self.val = sig