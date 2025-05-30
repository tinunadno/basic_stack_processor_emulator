from stack_machine.utils.bitwise_utils import set_int_cut, get_int_cut


class mc_signals_descriptions:
    def __init__(self, signals: dict[str, int], rang: list[int]):
        self.sig_range = rang
        self.signals = signals
    def get_signal_as_dict(self, signal: int) -> dict[str, bool]:
        ret = {}
        for i in self.signals.items():
            val = get_int_cut(signal, [i[1]])
            if val != 0:
                ret[i[0]] = True
        return ret

mc_sigs_info : dict[str, mc_signals_descriptions] = {
    "alu": mc_signals_descriptions( {"open_a": 0,"open_b": 1,"add": 2,"sub": 3,"and": 4,"or": 5, "inc": 6, "mul": 7, "div": 8, "shl": 9, "shr": 10, "not": 11}, [0, 11]),
    "mem": mc_signals_descriptions( {"do_mem": 0,"read": 1}, [12, 13]),
    "cpu": mc_signals_descriptions( {"load_imm": 0,"push_stack": 1,"pop_stack": 2,"push_ret": 3,"load_T_a": 4,"load_T_b": 5,"load_S": 6,
                              "fetch_pc": 7,"restore_pc": 8,"kill_cpu": 9,}, [14, 23]),
    "mc": mc_signals_descriptions( {"term_mc": 0}, [24]),
}

class mc:
    def __init__(self, signals: list[tuple[str, list[str]]], desc: str = ""):
        self.bits: int = 0
        self.desc = desc
        for sig in signals:
            name = sig[0]
            for signal_bit in sig[1]:
                self.bits = set_int_cut(self.bits, [mc_sigs_info[name].signals[signal_bit] + mc_sigs_info[name].sig_range[0]], 1)
    def get_signal(self, name: str) -> dict[str, bool]:
        return mc_sigs_info[name].get_signal_as_dict(get_int_cut(self.bits, mc_sigs_info[name].sig_range))

