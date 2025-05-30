from fontTools.ttLib.tables.ttProgram import instructions

from stack_machine.cpu.cpu import cpu
from stack_machine.cpu.instruction.instruction import inst
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
        # fst block
        mc([("alu", ["open_b", "add"]), ("cpu", ["load_imm", "push_stack"])], "push_imm"),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_b", "add"]), ("mem", ["do_mem", "read"]), ("cpu", ["load_imm"])], "lw_from_im_addr"),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_a", "add"]),  ("mem", ["do_mem", "read"])], "lw_from_a_addr"),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_b", "add"]), ("mem", ["do_mem", "read"])], "lw_from_b_addr"),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_a", "add"]), ("mem", ["do_mem", "read"])], "lw_from_b_addr_inc_a"),
        mc([("alu", ["open_a", "inc"]), ("cpu", ["push_stack"])]),
        mc([("cpu", ["load_T_a", "pop_stack"])]),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_b", "add"]), ("mem", ["do_mem"]), ("cpu", ["load_imm", "pop_stack"])], "sw_to_imm_addr"),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_a", "add"]), ("mem", ["do_mem"]), ("cpu", ["pop_stack"])], "sw_to_a_addr"),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_b", "add"]), ("mem", ["do_mem"]), ("cpu", ["pop_stack"])], "sw_to_b_addr"),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_a", "add"]), ("mem", ["do_mem"]), ("cpu", ["pop_stack"])], "sw_to_a_addr_inc_a"),
        mc([("alu", ["open_a", "inc"]), ("cpu", ["push_stack"])]),
        mc([("cpu", ["load_T_a", "pop_stack"])]),
        mc([("mc", ["term_mc"])]),
        mc([("cpu", ["load_T_a", "pop_stack"])], "load_T_a_pop"),
        mc([("mc", ["term_mc"])]),
        mc([("cpu", ["load_T_b", "pop_stack"])], "load_T_b_push"),
        mc([("mc", ["term_mc"])]),
        mc([("alu", ["open_a", "add"]), ("cpu", ["push_stack"])], "push_a"),
        mc([("mc", ["term_mc"])]),
        # arithm
        mc([("cpu", ["load_T_a", "pop_stack"])], "+"),
        mc([("cpu", ["load_T_a", "pop_stack"])]),
        mc([("alu", ["open_a", "open_b", "add"]), ("cpu", ["push_stack"])]),
        mc([("mc", ["term_mc"])]),
        mc([("cpu", ["load_T_a", "pop_stack"])], "-"),
        mc([("cpu", ["load_T_a", "pop_stack"])]),
        mc([("alu", ["open_a", "open_b", "sub"]), ("cpu", ["push_stack"])]),
        mc([("mc", ["term_mc"])]),
        mc([("cpu", ["load_T_a", "pop_stack"])], "*"),
        mc([("cpu", ["load_T_a", "pop_stack"])]),
        mc([("alu", ["open_a", "open_b", "mul"]), ("cpu", ["push_stack"])]),
        mc([("mc", ["term_mc"])]),
        mc([("cpu", ["load_T_a", "pop_stack"])], "/"),
        mc([("cpu", ["load_T_a", "pop_stack"])]),
        mc([("alu", ["open_a", "open_b", "div"]), ("cpu", ["push_stack"])]),
        mc([("mc", ["term_mc"])]),
        mc([("cpu", ["load_T_a", "pop_stack"])], "<<"),
        mc([("cpu", ["load_T_a", "pop_stack"])]),
        mc([("alu", ["open_a", "shl"]), ("cpu", ["push_stack"])]),
        mc([("mc", ["term_mc"])]),
        mc([("cpu", ["load_T_a", "pop_stack"])], ">>"),
        mc([("cpu", ["load_T_a", "pop_stack"])]),
        mc([("alu", ["open_a", "shr"]), ("cpu", ["push_stack"])]),
        mc([("mc", ["term_mc"])]),
        mc([("cpu", ["load_T_a", "pop_stack"])], "not"),
        mc([("cpu", ["load_T_a", "pop_stack"])]),
        mc([("alu", ["open_a", "not"]), ("cpu", ["push_stack"])]),
        mc([("mc", ["term_mc"])]),
    ]
    insts = [ # manually setting up instructions
        # imm                      mc_addr
        inst.generate_inst(mc_, "push_imm", 73),
        inst.generate_inst(mc_, "push_imm", 74),
        inst.generate_inst(mc_, "not", 74),

    ]
    # 0b0_0000000_00_000000
    i_mem = inst_mem(insts)
    mem = data_mem(32, [80, 84], [1, 2, 3, 4, 5])
    return cpu(8, mem, i_mem, mc_)