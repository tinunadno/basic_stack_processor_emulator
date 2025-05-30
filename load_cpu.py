from stack_machine.cpu.cpu import cpu
from stack_machine.cpu.mc.mc import mc
from stack_machine.cpu.mem.data_mem import data_mem
from stack_machine.cpu.mem.inst_mem import inst_mem


# mc_sigs_info : dict[str, mc_signals_descriptions] = {
#     "alu": mc_signals_descriptions( {"open_a": 0,"open_b": 1,"add": 2,"sub": 3,"and": 4,"or": 5,}),
#     "mem": mc_signals_descriptions( {"do_mem": 0,"write_read": 1}),
#     "cpu": mc_signals_descriptions( {"load_imm": 0,"push_stack": 1,"pop_stack": 2,"push_ret": 3,"load_T": 4,"load_S": 5,
#                               "fetch_pc": 6,"restore_pc": 7,"kill_cpu": 8,}),
#     "mc": mc_signals_descriptions( {"term_mc": 0}),
# }

def load_cpu() -> cpu:
    mc_: list[mc] = [ # manually setting up microcommands, u can make beautiful constructor for mc class and it'll be readable
        # mc([("alu", ["open_a", "open_b", "add"]), ("cpu", ["push_stack", "load_T", "load_S"])], "add"),
        # mc([("mc", ["term_mc"])]),
        # mc([("alu", ["open_a", "open_b", "add"]), ("mem", ["do_mem", "write_read"]), ("cpu", ["load_imm", "load_T"])], "load"),
        # mc([("mc", ["term_mc"])]),
        # mc([("alu", ["open_a", "open_b", "add"]), ("mem", ["do_mem"]), ("cpu", ["load_imm", "load_T"])], "store"),
        # mc([("mc", ["term_mc"])]),
        # mc([("alu", ["open_a", "open_b", "add"]), ("cpu", ["push_stack", "load_T", "load_S"])], "sum_top"),
        # mc([("mc", ["term_mc"])]),
        # mc([("cpu", ["pop_stack"])], "pop"),
        # mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_b", "add"]), ("cpu", ["load_imm", "push_stack"])], "push_imm"),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_b", "add"]), ("mem", ["do_mem", "read"]), ("cpu", ["load_imm"])], "lw_from_im_addr"),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_a", "add"]),  ("mem", ["do_mem", "read"])], "lw_from_a_addr"),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_b", "add"]), ("mem", ["do_mem", "read"])], "lw_from_b_addr"),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_a", "add"]), ("mem", ["do_mem", "read"])], "lw_from_b_addr"),
        mc([("alu", ["open_a", "inc"]), ("cpu", ["push_stack"])], "inc_a"),
        mc([("cpu", ["load_T_a", "pop_stack"])], "inc_a"),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_b", "add"]), ("mem", ["do_mem"]), ("cpu", ["load_imm", "pop_stack"])], "sw_to_imm_addr"),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_a", "add"]), ("mem", ["do_mem"]), ("cpu", ["pop_stack"])], "sw_to_a_addr"),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_b", "add"]), ("mem", ["do_mem"]), ("cpu", ["pop_stack"])], "sw_to_b_addr"),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_a", "add"]), ("mem", ["do_mem"]), ("cpu", ["pop_stack"])], "sw_to_a_addr"),
        mc([("alu", ["open_a", "inc"]), ("cpu", ["push_stack"])], "inc_a"),
        mc([("cpu", ["load_T_a", "pop_stack"])], "inc_a"),
        mc([("mc", ["term_mc"])]),
        mc([("cpu", ["load_T_a", "pop_stack"])], "ST -> A; pop"),
        mc([("mc", ["term_mc"])]),
        mc([("cpu", ["load_T_b", "pop_stack"])], "ST -> B; pop"),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_a", "add"]), ("cpu", ["push_stack"])], "push_a"),
        mc([("mc", ["term_mc"])]),
        # mc(0b0_000110010_00_000111),  # 0 | A + B -> T
        # mc(0b1_000000000_00_000000),  # 1 | term
        # mc(0b0_000010001_11_000111),  # 2 | imm -> B; T -> A; mem[B + A] -> T
        # mc(0b1_000000000_00_000000),  # 3 | term
        # mc(0b0_000010001_01_000111),  # 4 | imm -> B; T -> A; S -> mem[B + A]
        # mc(0b1_000000000_00_000000),  # 5 | term
        # mc(0b0_000110010_00_000111),  # 6 | T -> A; S -> B; A + B ->T
        # mc(0b1_000000000_00_000000),  # 7 | term
        # mc(0b0_000000100_00_000000),  # 8 | pop
        # mc(0b1_000000000_00_000000),  # 9 | term
        # mc(0b0_000000011_00_000110),  # 10| imm -> B; B + 0 -> T
        # mc(0b1_000000000_00_000000),  # 11| term

        # mc(0b0_100000000_00_000000),  # 12| halt
        # mc(0b1_000000000_00_000000),  # 13| term
        # mc(0b0_000000010_00_000101),  # 14| A -> T
        # mc(0b1_000000000_00_000000),  # 15| term
    ]
    inst = [ # manually setting up instructions
        # imm                      mc_addr
        0b000011111111111111111111_00000000,   # li 0b1111                               stack: [0b1111]
        0b000011111111111111111111_00010110,   # li 0b1111                               stack: [0b1111]
        0b000011111111111111111111_00011000,   # li 0b1111                               stack: [0b1111]
        0b000011111111111111111111_00011010,   # li 0b1111                               stack: [0b1111]



    ]
    # 0b0_0000000_00_000000
    i_mem = inst_mem(inst)
    mem = data_mem(32, [80, 84], [1, 2, 3, 4, 5])
    return cpu(8, mem, i_mem, mc_)