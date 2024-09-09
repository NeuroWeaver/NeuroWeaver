import numpy as np
from inst_gen_fns import *
# ns_dict = {'obuf': 0, 'ibuf': 1, 'vmem1': 2, 'vmem2': 3, 'imm': 4, 'none' : 5} #in RTL, vmem2 is buffer index 5, not match with ISA
ns_dict = {'obuf': 0, 'ibuf': 1, 'vmem1': 2, 'vmem2': 3, 'imm': 4, 'none' : 5} #in RTL, vmem2 is buffer index 5, not match with ISA
initialize_memories()

# generate_random_numbers(100)
np.random.seed(100)
inst_file_name = 'instructions.txt'

empty_instructions_file(inst_file_name)
start("Start")

'''
set_iterator('vmem1', 0, 'linear', "set_iter_0_vmem1", base=0, stride=20)
set_iterator('none', 0, 'linear', "dummy", base=0, stride=0)
set_iterator('ibuf', 0, 'linear', "set_iter_0_ibuf", base=0, stride=20)

set_iterator('vmem1', 1, 'linear', "set_iter_1_vmem1", base=0, stride=5)
set_iterator('none', 1, 'linear', "dummy", base=0, stride=0)
set_iterator('ibuf', 1, 'linear', "set_iter_1_ibuf", base=0, stride=5)

set_iterator('vmem1', 2, 'linear', "set_iter_2_vmem1", base=0, stride=1)
set_iterator('none', 2, 'linear', "dummy", base=0, stride=0)
set_iterator('ibuf', 2, 'linear', "set_iter_2_ibuf", base=0, stride=1)

loop_set_index("SET_INDEX_0", ns_dict["ibuf"], 0, ns_dict["vmem1"], 0, 0, 0)
loop_set_iter("SET_ITER_0", loop_id=0, iteration_cnt=3)
loop_set_index("SET_INDEX_1", ns_dict["ibuf"], 1, ns_dict["vmem1"], 1, 0, 0)
loop_set_iter("SET_ITER_1", loop_id=1, iteration_cnt=4)
loop_set_index("SET_INDEX_2", ns_dict["ibuf"], 2, ns_dict["vmem1"], 2, 0, 0)
loop_set_iter("SET_ITER_2", loop_id=2, iteration_cnt=5)
loop_set_inst("SET_INST", instruction_cnt=1, is_nested=True)
#set_iterator('vmem1', 'linear', "set_iter_1", base=0, stride=1)
operation(1, 0, ['ibuf', 2], ['vmem1', 2], "relu", None)
'''

set_iterator('vmem1', 0, 'linear', "set_iter_vmem1", base=0, stride=1)
set_iterator('none', 0, 'linear', "dummy", base=0, stride=0)
set_iterator('ibuf', 0, 'linear', "set_iter_ibuf", base=0, stride=1)
loop_set_index("SET_INDEX", ns_dict["ibuf"], 1, ns_dict["vmem1"], 1, 1, 1)
loop_set_iter("SET_ITER", loop_id=0, iteration_cnt=60)
loop_set_inst("SET_INST", instruction_cnt=1, is_nested=True)
operation(1, 0, ['ibuf', 0], ['vmem1', 0], "relu", None)

'''
set_iterator('vmem1', 'linear', "set_iter_1", base=0, stride=1)
set_iterator('vmem2', 'linear', "set_iter_2", base=0, stride=1)
set_iterator('ibuf', 'linear',"set_iter_3", base=0, stride=1)

operation(0, 4, ['ibuf', 1], ['vmem1', 2], "operation", ['vmem2', 3])

set_iterator('vmem1', 'linear', "set_iter_1", base=0, stride=1)
set_iterator('none', 'linear', "set_iter_2", base=0, stride=1)
set_iterator('ibuf', 'linear',"set_iter_3", base=0, stride=1)

operation(1, 0, ['ibuf', 1], ['vmem1', 2], "operation", None)
'''

done("done")
print_memory_names()
dump_memories()