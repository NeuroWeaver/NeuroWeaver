from collections import defaultdict

import numpy as np
#from fxpmath import Fxp

num_elem = 4

inst_file_name = 'instructions.txt'
#ns_dict = {'obuf': 0, 'ibuf': 1, 'vmem1': 2, 'imm': 3, 'ext_mem': 4, 'vmemR': 5, 'vmemW' : 6, 'vmem2': 7, 'none' : 8}
ns_dict = {'obuf': 0, 'ibuf': 1, 'vmem1': 2, 'vmem2': 3, 'imm': 4, 'none' : 5} #in RTL, vmem2 is buffer index 5, not match with ISA
ld_st_ns_dict = {'obuf': 0, 'ibuf': 1, 'vmem1': 1, 'imm': 3, 'ext_mem': 4, 'vmemR': 5, 'vmemW' : 6, 'vmem2': 2, 'none' : 8}

memories = defaultdict(list)
iterators = defaultdict(list)
instructions = []
instructions_bi = []
instructions_debug = []

loop_start_index = 0
iters = 10
memory_depth = num_elem*iters

n_max = 2 ** (31) - 1
n_min = -1 - n_max

def generate_random_numbers(num=1000, bits=31):
    n_max_local = 2 ** (bits) - 1
    n_min_local = -1 - n_max_local
    a = np.random.randint(0, n_max_local, num)
    b = np.random.randint(0, 8, num)
    data = []
    for ind, i in enumerate(b):
        if i == 0:
            data.append(n_max_local)
        elif i == 1:
            data.append(n_min_local)
        elif i == 2:
            data.append(a[ind] & 0xffff)
        elif i == 3:
            data.append(-1 * (a[ind] & 0xffff))
        elif i % 2 == 0:
            data.append(a[ind])
        else:
            data.append(-1 * a[ind])
    return data


def empty_instructions_file(file_n):
    global instructions
    global inst_file_name
    inst_file_name = file_n
    with open(inst_file_name, 'w') as f:
        a = 1


def set_iterator(ns, index_id, type, iHint, base=0, stride=1):
    if type == 'linear':
        if ns != 'none':
            base_inst = (6 << 28) + (3 << 24) + (ns_dict[ns] << 21) + (index_id << 16) + (int(base) & 0xffff)
            stride_inst = (6 << 28) + (7 << 24) + (ns_dict[ns] << 21) + (index_id << 16) + (stride & 0xffff)
            instructions.append(base_inst)
            instructions.append(stride_inst)
            instructions_bi.append('{:032b}'.format(base_inst))
            instructions_bi.append('{:032b}'.format(stride_inst))
            instructions_debug.append(iHint)
            instructions_debug.append(iHint)
        if ns not in iterators:
            iterators[ns] = defaultdict(list)
        iterators[ns][ns_dict[ns]] = [base, stride]


def loop_start(iHint): # why append 0, 0 is add
    global loop_start_index
    loop_start_index = len(instructions)
    instructions.append(0)
    instructions_bi.append('{:032b}'.format(0))
    instructions_debug.append(iHint)


def loop_end(iterations=100): # LOOP opcode does not have 8 specified from bit 24
    num_instructions = len(instructions) - loop_start_index - 1
    loop_inst = (7 << 28) + (8 << 24) + ((num_instructions & 0xfff) << 12) + (iterations & 0xfff)
    instructions[loop_start_index] = loop_inst
    instructions_bi[loop_start_index] = '{:032b}'.format(loop_inst)
    instructions_debug.append("Loop End")

memories_used = defaultdict(list)

def operation(opcode, func, dest, src1, iHint, src2=None):
    memories_used[dest[0]] = 1
    memories_used[src1[0]] = 1
    if src2 is None:
        src2 = ['none', 5]
    else:
        memories_used[src2[0]] = 1
    if src2[0] == 'none':
        inst = (opcode << 28) + (func << 24) + (ns_dict[dest[0]] << 21) + (dest[1] << 16) + (ns_dict[src1[0]] << 13) + (src1[1] << 8)
    else:
        inst = (opcode << 28) + (func << 24) + (ns_dict[dest[0]] << 21) + (dest[1] << 16) + (ns_dict[src1[0]] << 13) + (src1[1] << 8) + (ns_dict[src2[0]] << 5) + (src2[1])
    instructions.append(inst)
    instructions_bi.append('{:032b}'.format(inst))
    instructions_debug.append(iHint)
    src1_lv = iterators[src1[0]][src1[1]]

    src2_lv = iterators[src2[0]][src2[1]]
    dest_lv = iterators[dest[0]][dest[1]]

    return
    
    for i in range(iters*num_elem):
        src1_addr = src1_lv[0] + src1_lv[1] * i
        src2_addr = src2_lv[0] + src2_lv[1] * i
        dest_addr = dest_lv[0] + dest_lv[1] * i
        #print ("Iteration = ",i)
        if src2[0] == 'none':
            memories[dest[0]][dest_addr] = calculate_output(opcode, func, memories[src1[0]][src1_addr],
                                                        None)
        else:
            memories[dest[0]][dest_addr] = calculate_output(opcode, func, memories[src1[0]][src1_addr],
                                                        memories[src2[0]][src2_addr])


def set_immediate(ns_idx, iHint):
    base = np.random.random_integers(0, 10) * 0 + 17
    base = ((base * 4) << 16) + base
    inst = (6 << 28) + (8 << 24) + (3 << 21) + (ns_idx << 16) + (int(base) & 0xffff)
    instructions.append(inst)
    instructions_debug.append(iHint)
    inst = (6 << 28) + (9 << 24) + (3 << 21) + (ns_idx << 16) + (int(base >> 16) & 0xffff)
    instructions.append(inst)
    instructions_debug.append(iHint)
    memories['imm'][ns_idx] = base

def start(iHint): 
    inst = (10 << 28) + (8 << 24) + 0
    instructions.append(inst)
    instructions_bi.append('{:032b}'.format(inst))
    instructions_debug.append(iHint)

def done(iHint): #[31:28] = 1010 [27:22] = 001001
    inst = (10 << 28) + (12 << 24) + 0
    instructions.append(inst)
    instructions_bi.append('{:032b}'.format(inst))
    instructions_debug.append(iHint)
    print("Total Instructions = ", len(instructions))
    print("Total Instructions Hints = ", len(instructions_debug),"\n")
    
    print ("{:<10} {:<32}  {:<15}".format("Address", "Instructions", "Hint"))
    for j in range(len(instructions)):
        #print (instructions[j], instructions_debug[j])
        print ("{:<10} {:<33} {:<15}".format(j,instructions_bi[j], instructions_debug[j]))

    with open(inst_file_name, 'a') as f:
        for inst in instructions:
            f.write(str(inst) + '\n')


def initialize_memories(mem=None):
    if mem is None:
        mem = ns_dict.keys()
    for k, v in ns_dict.items():
        if k in mem and k != "none":
            data = generate_random_numbers(memory_depth)
            memories[k] = data

def out_of_bound(val):
    if val > n_max:
        return n_max
    elif val < n_min:
        return n_min
    else:
        return val

def sigmoid(x):
    return 1/(1+np.exp(-x))

def tanh(x):
    return np.tanh(x)

def RELU(x):
    if x < 0.0:
        return 0.0
    else:
        return x
    

def LRELU(x, alpha):
    if x < 0.0:
        return (alpha * x)
    else:
        return x

ISAOpcode = {'ALU': 0, 'CALCULUS' : 1, 'COMPARISON' : 2, 'DATATYPE_CAST' : 3, 'DATATYPE CONFIG' : 4, \
            'LD_ST' : 5, 'ITERATOR_CONFIG' : 6, 'LOOP': 7, 'none': 8}
ALUFunc = {'ADD' : 0, 'SUB' : 1, 'MUL' : 2, 'MACC' : 3, 'DIV' : 4, 'MAX' : 5, 'MIN' : 6, 'RSHIFT' : 7,\
            'LSHIFT' : 8, 'MOVE' : 9, 'COND MOVE TRUE' : 10, 'COND MOVE FALSE' : 11, 'NOT' : 12,\
            'AND' : 13, 'OR' : 14, 'NOP' : 15}
CALCULUSFunc = {'RELU': 0, 'LRELU': 1, 'SIGMOID': 3, 'TANH': 4, 'none': 5}
COMPARISONFunc = {'EQUAL': 0, 'NEQ': 1, 'GT': 2, 'GTE': 3, 'LT': 4, 'LTE': 5}

def calculate_output(opcode, func, src1, src2):
    #print ("opcode =", opcode )
    #print ("fn =", fn )
    #print ("src1 =", src1 )
    #print ("src2 =", src2 )
    if opcode == ISAOpcode['ALU']:  
        if func == ALUFunc['ADD']:  
            out = np.int64(src1) + np.int64(src2)
            out = out_of_bound(out)
            # print(src1,src2,out)
        if func == ALUFunc['SUB']:  
            out = np.int64(src1) - np.int64(src2)
            out = out_of_bound(out)
        if func == ALUFunc['MUL']:  
            out = np.int64(src1) * np.int64(src2)
            out = out_of_bound(out)
        if func == ALUFunc['MAX']:  
            out =  max(np.int64(src1), np.int64(src2))
            out = out_of_bound(out)
        if func == ALUFunc['MIN']:  
            out =  min(np.int64(src1), np.int64(src2))
            out = out_of_bound(out)
        if func == ALUFunc['NOT']:  
            out =  ~np.int64(src1)
            out = out_of_bound(out)
        if func == ALUFunc['AND']:  
            out =  np.int64(src1) & np.int64(src2)
            out = out_of_bound(out)
        if func == ALUFunc['OR']:  
            out =  np.int64(src1) | np.int64(src2)
            out = out_of_bound(out)
        if func == ALUFunc['DIV']:
            out =  np.int64(src1) / np.int64(src2)
            out = out_of_bound(out)
        
    elif opcode == ISAOpcode['CALCULUS']:
        if func == CALCULUSFunc['RELU']: 
            out = RELU(np.int64(src1))
            out = out_of_bound(out)
        if func == CALCULUSFunc['LRELU']:  
            out = LRELU(np.int64(src1), src2)
            out = out_of_bound(out)
        if func == CALCULUSFunc['SIGMOID']:  
            out = sigmoid(np.int64(src1))
            out = out_of_bound(out)
        if func == CALCULUSFunc['TANH']:  
            out = tanh(np.int64(src1))
            out = out_of_bound(out)

    elif opcode == ISAOpcode['COMPARISON']:
        if func == COMPARISONFunc['EQUAL']: 
            out = np.int64(src1) == np.int64(src2)
        if func == COMPARISONFunc['NEQ']: 
            out = np.int64(src1) != np.int64(src2)
        if func == COMPARISONFunc['GT']: 
            out = np.int64(src1) > np.int64(src2)
        if func == COMPARISONFunc['GTE']: 
            out = np.int64(src1) >= np.int64(src2)
        if func == COMPARISONFunc['LT']: 
            out = np.int64(src1) < np.int64(src2)
        if func == COMPARISONFunc['LTE']: 
            out = np.int64(src1) <= np.int64(src2)

    return out

LDST_OP = 5
LD_CONFIG_BASE_ADDR_func = 0 
LD_CONFIG_BASE_LOOP_ITER_func = 1
LD_CONFIG_BASE_LOOP_STRIDE_func = 2
LD_CONFIG_TILE_LOOP_ITER_func = 3
LD_CONFIG_TILE_LOOP_STRIDE_func = 4
LD_START_func = 5
ST_CONFIG_BASE_ADDR_func = 8 
ST_CONFIG_BASE_LOOP_ITER_func = 9 
ST_CONFIG_BASE_LOOP_STRIDE_func = 10
ST_CONFIG_TILE_LOOP_ITER_func = 11
ST_CONFIG_TILE_LOOP_STRIDE_func = 12
ST_START_func = 13

def load(iHint, mem = 'vmem1', loop_imm_val = 0, loop_index = 0, loop_stride = 1, tile_imm_val = 0, tile_stride = 1, data_width=0, req_size=0, base_lsb=0, base_msb=0):
    LD_CONFIG_BASE_LOOP_ITER = (LDST_OP << 28) + (LD_CONFIG_BASE_LOOP_ITER_func << 24) + (ld_st_ns_dict[mem] << 21) + (loop_index << 16) + loop_imm_val
    LD_CONFIG_BASE_LOOP_STRIDE = (LDST_OP << 28) + (LD_CONFIG_BASE_LOOP_STRIDE_func << 24) + (ld_st_ns_dict[mem] << 21) + (loop_index << 16) + loop_stride
    LD_CONFIG_BASE_ADDR_LSB = (LDST_OP << 28) + (LD_CONFIG_BASE_ADDR_func << 24) + (0 << 23) + (ld_st_ns_dict[mem] << 21) + (loop_index << 16) + base_lsb
    LD_CONFIG_BASE_ADDR_MSB = (LDST_OP << 28) + (LD_CONFIG_BASE_ADDR_func << 24) + (1 << 23) + (ld_st_ns_dict[mem] << 21) + (loop_index << 16) + base_msb
    LD_CONFIG_TILE_LOOP_ITER = (LDST_OP << 28) + (LD_CONFIG_TILE_LOOP_ITER_func << 24) + (ld_st_ns_dict[mem] << 21) + (loop_index << 16) + tile_imm_val
    LD_CONFIG_TILE_LOOP_STRIDE = (LDST_OP << 28) + (LD_CONFIG_TILE_LOOP_STRIDE_func << 24) + (ld_st_ns_dict[mem] << 21) + (loop_index << 16) + tile_stride
    LD_START = (LDST_OP << 28) + (LD_START_func << 24) + (ld_st_ns_dict[mem] << 21) + (data_width << 16) + req_size
    instructions.append(LD_CONFIG_BASE_LOOP_ITER)
    instructions.append(LD_CONFIG_BASE_LOOP_STRIDE)
    instructions.append(LD_CONFIG_BASE_ADDR_LSB)
    instructions.append(LD_CONFIG_BASE_ADDR_MSB)
    instructions.append(LD_CONFIG_TILE_LOOP_ITER)
    instructions.append(LD_CONFIG_TILE_LOOP_STRIDE)
    instructions.append(LD_START)

    instructions_bi.append('{:032b}'.format(LD_CONFIG_BASE_LOOP_ITER))
    instructions_bi.append('{:032b}'.format(LD_CONFIG_BASE_LOOP_STRIDE))
    instructions_bi.append('{:032b}'.format(LD_CONFIG_BASE_ADDR_LSB))
    instructions_bi.append('{:032b}'.format(LD_CONFIG_BASE_ADDR_MSB))
    instructions_bi.append('{:032b}'.format(LD_CONFIG_TILE_LOOP_ITER))
    instructions_bi.append('{:032b}'.format(LD_CONFIG_TILE_LOOP_STRIDE))
    instructions_bi.append('{:032b}'.format(LD_START))

    instructions_debug.append(iHint)
    instructions_debug.append(iHint)
    instructions_debug.append(iHint)
    instructions_debug.append(iHint)
    instructions_debug.append(iHint)
    instructions_debug.append(iHint)
    instructions_debug.append(iHint)


    # mem, loop_imm_val = num_of_tiles, loop_index = for loop index,  
#store('vmem1', 1, 0, 0, 1, 1, 32, 16, 8192,0)
def store(iHint, mem = 'vmem1', loop_imm_val = 0, loop_index = 0, loop_stride = 1, tile_imm_val = 0, tile_stride = 1, data_width=0, req_size=0,base_lsb=0, base_msb=0):
    ST_CONFIG_BASE_ADDR_LSB = (LDST_OP << 28) + (ST_CONFIG_BASE_ADDR_func << 24) + (0 << 23) + (ld_st_ns_dict[mem] << 21) + (loop_index << 16) + base_lsb
    ST_CONFIG_BASE_ADDR_MSB = (LDST_OP << 28) + (ST_CONFIG_BASE_ADDR_func << 24) + (1 << 23) + (ld_st_ns_dict[mem] << 21) + (loop_index << 16) + base_msb

    ST_CONFIG_BASE_LOOP_ITER = (LDST_OP << 28) + (ST_CONFIG_BASE_LOOP_ITER_func << 24) + (ld_st_ns_dict[mem] << 21) + (loop_index << 16) + loop_imm_val

    ST_CONFIG_BASE_LOOP_STRIDE = (LDST_OP << 28) + (ST_CONFIG_BASE_LOOP_STRIDE_func << 24) + (ld_st_ns_dict[mem] << 21) + (loop_index << 16) + loop_stride
    
    # to generate address - ST_CONFIG_TILE_LOOP_ITER each is to generate one address - if 4 iterations, 4 requests and each address ld st chunk of data
    ST_CONFIG_TILE_LOOP_ITER = (LDST_OP << 28) + (ST_CONFIG_TILE_LOOP_ITER_func << 24) + (ld_st_ns_dict[mem] << 21) + (loop_index << 16) + tile_imm_val
    # to update the address
    # chunk size if calculated in hardware
    ST_CONFIG_TILE_LOOP_STRIDE = (LDST_OP << 28) + (ST_CONFIG_TILE_LOOP_STRIDE_func << 24) + (ld_st_ns_dict[mem] << 21) + (loop_index << 16) + tile_stride
    ST_START = (LDST_OP << 28) + (ST_START_func << 24) + (ld_st_ns_dict[mem] << 21) + (data_width << 16) + req_size

    instructions.append(ST_CONFIG_BASE_LOOP_ITER)
    instructions.append(ST_CONFIG_BASE_LOOP_STRIDE)
    instructions.append(ST_CONFIG_BASE_ADDR_LSB) 
    instructions.append(ST_CONFIG_BASE_ADDR_MSB) 
    instructions.append(ST_CONFIG_TILE_LOOP_ITER)
    instructions.append(ST_CONFIG_TILE_LOOP_STRIDE)
    instructions.append(ST_START)

    instructions_bi.append('{:032b}'.format(ST_CONFIG_BASE_LOOP_ITER))
    instructions_bi.append('{:032b}'.format(ST_CONFIG_BASE_LOOP_STRIDE))
    instructions_bi.append('{:032b}'.format(ST_CONFIG_BASE_ADDR_LSB))
    instructions_bi.append('{:032b}'.format(ST_CONFIG_BASE_ADDR_MSB))
    instructions_bi.append('{:032b}'.format(ST_CONFIG_TILE_LOOP_ITER))
    instructions_bi.append('{:032b}'.format(ST_CONFIG_TILE_LOOP_STRIDE))
    instructions_bi.append('{:032b}'.format(ST_START))
    
    instructions_debug.append(iHint)
    instructions_debug.append(iHint)
    instructions_debug.append(iHint)
    instructions_debug.append(iHint)
    instructions_debug.append(iHint)
    instructions_debug.append(iHint)
    instructions_debug.append(iHint)

def print_memories():
    for i in memories:
        print(memories[i])

def print_memory_names():
    print(memories.keys())

def dump_memories():
    for i in memories_used.keys():
        with open(i + '.txt', 'w') as f:
            for data in memories[i]:
                f.write(str(int(data)) + '\n')


def loop_set_index(iHint,
                   dst_ns_id, dst_index_id,
                   src1_ns_id, src1_index_id,
                   src2_ns_id, src2_index_id):
    inst = (7 << 28) + (0 << 24)
    inst += (dst_ns_id << 21) + (dst_index_id << 16)
    inst += (src1_ns_id << 13) + (src1_index_id << 8)
    inst += (src2_ns_id << 5) + src2_index_id

    instructions.append(inst)
    instructions_bi.append('{:032b}'.format(inst))
    instructions_debug.append(iHint)


def loop_set_iter(iHint,
                  loop_id,
                  iteration_cnt):
    inst = (7 << 28) + (1 << 24)
    inst += (loop_id << 21)
    inst += iteration_cnt

    instructions.append(inst)
    instructions_bi.append('{:032b}'.format(inst))
    instructions_debug.append(iHint)


def loop_set_inst(iHint,
                  instruction_cnt,
                  is_nested=False):
    inst = (7 << 28) + (2 << 24)
    inst += ((1 if is_nested else 0) << 21)
    inst += instruction_cnt

    instructions.append(inst)
    instructions_bi.append('{:032b}'.format(inst))
    instructions_debug.append(iHint)


'''
base_inst = (6 << 28) + (3 << 24) + (ns_dict[ns] << 21) + (ns_dict[ns] << 16) + (int(base) & 0xffff)
            stride_inst = (6 << 28) + (7 << 24) + (ns_dict[ns] << 21) + (ns_dict[ns] << 16) + (stride & 0xffff)
            instructions.append(base_inst)
            instructions.append(stride_inst)
            instructions_bi.append('{:032b}'.format(base_inst))
            instructions_bi.append('{:032b}'.format(stride_inst))
            instructions_debug.append(iHint)
            instructions_debug.append(iHint)
'''