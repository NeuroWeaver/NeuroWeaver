import numpy as np
from fxpmath import Fxp
from collections.abc import Iterable
import math

ns_dict = {
    0: "obuf",
    1: "ibuf",
    2: "vmem1",
    3: "vmem2",
    4: "imm"
}

FXP_CONFIGS = {
    "FXP32": {"signed": True, "n_int": 15, "n_frac": 16, "overflow": "saturate", "n_word": 32}
}


def sigmoid_pw(xval, dtype):
    if not isinstance(xval, Iterable):
        xval = np.asarray([xval])

    def inner(x, slope, start):
        result = (((x) >> slope) + start)
        return result

    pw5 = Fxp(5.0, **FXP_CONFIGS[dtype])
    pw2375 = Fxp(2.375, **FXP_CONFIGS[dtype])
    pw1 = Fxp(1.0, **FXP_CONFIGS[dtype])

    conds = [
        xval < -pw5.val,
        (xval < -pw2375.val) & (xval >= -pw5.val),
        (xval < -pw1.val) & (xval >= -pw2375.val),
        (xval < 0) & (xval >= -pw1.val),
        (xval >= 0) & (xval < (pw1.val)),
        (xval >= pw1.val) & (xval < (pw2375.val)),
        (xval >= pw2375.val) & (xval < (pw5.val)),
        (xval >= pw5.val)]

    p5 = Fxp(0.5, **FXP_CONFIGS[dtype]).val
    p625 = Fxp(0.625, **FXP_CONFIGS[dtype]).val
    p84375 = Fxp(0.84375, **FXP_CONFIGS[dtype]).val
    p375 = Fxp(0.375, **FXP_CONFIGS[dtype]).val
    p15625 = Fxp(0.15625, **FXP_CONFIGS[dtype]).val

    fns = [lambda x: 0,
           lambda x: inner(x, 5, p15625),
           lambda x: inner(x, 3, p375),
           lambda x: inner(x, 2, p5),
           lambda x: inner(x, 2, p5),
           lambda x: inner(x, 3, p625),
           lambda x: inner(x, 5, p84375),
           lambda x: pw1.val]

    res = np.piecewise(xval, conds, fns)
    return res


def read_data(inst_reg, bank_idx, banked_memory, statistics):
    opcode = inst_reg.opcode
    function = inst_reg.function

    """
    Instruction opcodes which can read data from dst || src1 || src2:
    
    1. 0b_0000: ALU
    2. 0b_0001: CALCULUS
    3. 0b_0010: COMPARISON
    4. 0b_0011: DATATYPE_CAST
    
    Opcodes over 0100 is invalid. Should be skipped by callers (i.e Stage instances).
    """
    if opcode >= 4 and opcode != 8:
        raise ValueError(f"read_data(): invalid opcode {opcode}")

    should_access_src1 = False
    if opcode < 4 or opcode == 8 and function != 15:
        should_access_src1 = True

    if should_access_src1:
        src1_ns = ns_dict[inst_reg.src1_ns_id]
        # Rohan todo
        #idx_src1 = inst_reg.addr_src1 # // 4
        idx_src1 = inst_reg.addr_src1 % 511 if inst_reg.addr_src1 is not None and inst_reg.addr_src1 > 511 else inst_reg.addr_src1 # // 4

        if src1_ns == "imm":
            inst_reg.alu_src1 = banked_memory[src1_ns][inst_reg.src1_index_id]
            #rohan commented
            #inst_reg.alu_src1 = Fxp(0, **FXP_CONFIGS["FXP32"]).set_val(inst_reg.alu_src1, raw=True)
            statistics["memory-access"][src1_ns][0]["read"] += 1
        elif 'obuf' in src1_ns: ## Hanyang: Genesys only takes vmem access so obuf gets counted in vmem1 here
            statistics["memory-access"]['vmem1'][bank_idx]["computeRead"] += 1
        elif 'vmem' in src1_ns:
            statistics["memory-access"][src1_ns][bank_idx]["computeRead"] += 1
        else:
            inst_reg.alu_src1 = banked_memory[src1_ns][bank_idx][idx_src1]
            statistics["memory-access"][src1_ns][bank_idx]["read"] += 1

    """
    Some instructions don't require src2.
    """
    should_access_src2 = True
    if opcode == 0 and function == 15:
        # ALU NOP
        should_access_src2 = False

    elif opcode == 0 and function == 9:
        should_access_src2 = False
        
    elif opcode == 1 and (function >= 3 or function == 0):
        should_access_src2 = False
    
    elif opcode == 8 and function == 3:
        should_access_src2 = False

    if should_access_src2:
        if opcode == 3:
            # src2 ns of DATATYPE_CAST is always from IMM
            ns_id = 4
        else:
            ns_id = inst_reg.src2_ns_id

        src2_ns = ns_dict[ns_id]
        # Rohan added, todo hack
        #idx_src2 = inst_reg.addr_src2 # // 4
        idx_src2 = inst_reg.addr_src2 % 511 if inst_reg.addr_src2 is not None and inst_reg.addr_src2 > 511 else inst_reg.addr_src2 # // 4

        if src2_ns == "imm":
            #inst_reg.alu_src2 = banked_memory[src2_ns][inst_reg.src2_index_id]
            # rohan commented
            #inst_reg.alu_src2 = Fxp(0, **FXP_CONFIGS["FXP32"]).set_val(inst_reg.alu_src2, raw=True)
            statistics["memory-access"][src2_ns][0]["read"] += 1
        elif 'obuf' in src2_ns:
            statistics["memory-access"]['vmem1'][bank_idx]["computeRead"] += 1
        elif 'vmem' in src2_ns:
            statistics["memory-access"][src2_ns][bank_idx]["computeRead"] += 1
        else:
            #inst_reg.alu_src2 = banked_memory[src2_ns][bank_idx][idx_src2]
            statistics["memory-access"][src2_ns][bank_idx]["read"] += 1


def write_data(inst_reg, bank_idx, banked_memory, statistics):
    opcode = inst_reg.opcode
    function = inst_reg.function
    """
    Instruction opcodes which can read data from dst || src1 || src2:

    1. 0b_0000: ALU
    2. 0b_0001: CALCULUS
    3. 0b_0010: COMPARISON
    4. 0b_0011: DATATYPE_CAST
    
    Opcodes over 0100 is invalid. Should be skipped by callers (i.e Stage instances).
    """
    if opcode >= 4 and opcode != 8:
        raise ValueError(f"read_data(): invalid opcode {opcode}")
        #pass
    #if inst_reg.addr_dst % 4 != 0:
    #    raise ValueError(f"invalid address: should multiples of 4")
    #Rohan added: todo, add %512 to reduce simulation time
    #idx_dst = inst_reg.addr_dst # // 4
    idx_dst = inst_reg.addr_dst % 511 if inst_reg.addr_dst is not None and inst_reg.addr_dst > 511 else inst_reg.addr_dst # // 4
    dst_ns = ns_dict[inst_reg.dst_ns_id]
    #print ("Here = ", dst_ns, bank_idx, idx_dst)
    #print (f"here === {len(banked_memory[dst_ns])} , {len(banked_memory[dst_ns][bank_idx])}")
    #banked_memory[dst_ns][bank_idx][idx_dst] = inst_reg.alu_dst
    inst_reg.alu_dst = None
    
    #print(f"[wr] ns: {dst_ns}, val: {banked_memory[dst_ns][bank_idx][idx_dst]}")

    # write output
    ## Rohan: Because we do not need write for obuf 
    dst_ns = ns_dict[inst_reg.dst_ns_id]
    if 'vmem1' in dst_ns or 'vmem2' in dst_ns:
        statistics["memory-access"][dst_ns][bank_idx]["computeWrite"] += 1
    elif 'obuf' in dst_ns:
        statistics["memory-access"]['vmem1'][bank_idx]["computeWrite"] += 1


def execute(inst_reg, bank_idx, banked_memory, statistics):
    opcode = inst_reg.opcode
    function = inst_reg.function

    if opcode >= 4 and opcode != 8:
        raise ValueError(f"execute(): invalid opcode({opcode})")

    src1 = inst_reg.alu_src1 if inst_reg.alu_src1 is not None else 1 
    src2 = inst_reg.alu_src2 if inst_reg.alu_src2 is not None else 1
    
    if opcode == 0:
        if function == 0:
            # ADD
            inst_reg.alu_dst = src1 + src2
        elif function == 1:
            # SUB
            inst_reg.alu_dst = src1 - src2
        elif function == 2:
            # MUL
            #print (f"{inst_reg.alu_dst} = {src1} * {src2} = src1 * src2")
            inst_reg.alu_dst = src1 * src2
        elif function == 3:
            # MACC
            idx_dst = inst_reg.addr_dst  # // 4
            dst_ns = ns_dict[inst_reg.dst_ns_id]
            ## Rohan added since mobilenet sw pipeline was failing with out of bound
            #banked_memory[dst_ns][bank_idx][idx_dst%511] += src1 * src2
            # banked_memory[dst_ns][bank_idx][idx_dst] += src1 * src2
        elif function == 4:
            inst_reg.alu_dst = src1 / src2
        elif function == 5:
            # MAX
            inst_reg.alu_dst = src1 if src1 > src2 else src2
        elif function == 6:
            # MIN
            inst_reg.alu_dst = src1 if src1 < src2 else src2
        elif function == 7:
            # todo: RSHIFT
            inst_reg.alu_dst = src1 #>> src2
        elif function == 8:
            # todo: LSHIFT
            inst_reg.alu_dst = src1 #<< src2
        elif function == 9:
            # MOVE
            inst_reg.alu_dst = src1
        elif function == 10:
            # todo 
            inst_reg.alu_dst = src1 if src1 < src2 else src2
        elif function == 11:
            # todo 
            inst_reg.alu_dst = src1 if src1 > src2 else src2
        elif function == 12:
            # todo
            inst_reg.alu_dst = ~src1
        elif function == 13:
            # todo
            inst_reg.alu_dst = src1 & src2
        elif function == 14:
            # todo
            inst_reg.alu_dst = src1 | src2
        elif function == 15:
            # todo
            pass
        else:
            raise ValueError(f"not implemented instruciton: opcode({opcode}), function({function})")
    elif opcode == 1:
        if function == 0:
            # RELU
            inst_reg.alu_dst = src1 if src1 > 0 else 0
        elif function == 1:
            # LEAKY RELU
            inst_reg.alu_dst = src1 if src1 > 0 else src1 * src2
        elif function == 2:
            # SIGMOID
            inst_reg.alu_dst = 1 / (1 + math.exp(-src1))
        elif function == 3:
            # TANH
            inst_reg.alu_dst = math.tanh(src1)
        elif function == 5:
            inst_reg.alu_dst = math.log(src1) if src1 > 0 else -1
        elif function == 8:
            inst_reg.alu_dst = math.sqrt(src1) if src1 > 0 else -1
        elif function == 10:
            inst_reg.alu_dst = math.log(src1) if src1 > 0 else -1
        else:
            raise ValueError(f"not implemented instruciton: opcode({opcode}), function({function})")
    elif opcode == 3:
        # FLOOR
        if function == 8:
            inst_reg.alu_dst = math.floor(src1)
        # CEIL
        elif function == 9:
            inst_reg.alu_dst = math.ceil(src1)
            
    elif opcode == 8:
        if function == 3:
            inst_reg.alu_dst = src1
    
    else:
        #raise ValueError(f"not implemented instruciton: opcode({opcode}), function({function})")
        pass

class Stage:
    def __init__(self, simd_lane_cnt):
        self.input_inst_reg = None
        self.output_inst_reg = None
        self.cycle_executed = 0
        self.cycle_required = 0

        self.name = "Stage"
        self.simd_lane_cnt = simd_lane_cnt
        '''
        self.statistics = {
            "cycle": 0,
            "memory-access": {
                "obuf": {
                    i: {"read": 0} for i in range(simd_lane_cnt)
                },
                "ibuf": {
                    i: {"write": 0} for i in range(simd_lane_cnt)
                },
                "vmem1": {
                    i: {"read": 0, "write": 0} for i in range(simd_lane_cnt)
                },
                "vmem2": {
                    i: {"read": 0, "write": 0} for i in range(simd_lane_cnt)
                },
                "imm": {
                    0: {"read": 0, "write": 0}
                }
            }
        }
        '''
        self.statistics = {}
        self.statistics['cycles'] = 0
        self.statistics['memory-access'] = {}
        self.statistics['memory-access']['obuf'] = {}
        self.statistics['memory-access']['ibuf'] = {}
        self.statistics['memory-access']['vmem1'] = {}
        self.statistics['memory-access']['vmem2'] = {}
        self.statistics['memory-access']['imm'] = {}
        self.statistics['memory-access']['imm'][0] = {"read": 0, "write": 0}

        for i in range (simd_lane_cnt):
            self.statistics['memory-access']['obuf'][i] = {"read": 0}
            self.statistics['memory-access']['ibuf'][i] = {"write": 0}
            self.statistics['memory-access']['vmem1'][i] = {"computeRead": 0, "computeWrite": 0, "ldWrite": 0, "stRead": 0}
            self.statistics['memory-access']['vmem2'][i] = {"computeRead": 0, "computeWrite": 0, "ldWrite": 0, "stRead": 0}

    def cycle(self):
        """
        Implement a cycle for a stage.
        """
        if self.is_idle() or self.input_inst_reg is None:
            return

        if self.cycle_executed == 0:
            self.output_inst_reg = self._handle()

        if self.cycle_executed + 1 == self.cycle_required:
            # set as idle
            self.cycle_executed = 0
            self.cycle_required = 0
        else:
            self.cycle_executed += 1

    def pull_inst_reg(self, prev_stage):
        is_stalled = True

        if self.is_idle():
            self.input_inst_reg = None
            self.output_inst_reg = None

            if prev_stage is not None and prev_stage.is_idle():
                self._feed_inst_reg(prev_stage.output_inst_reg)
                prev_stage.output_inst_reg = None
                is_stalled = False

        return is_stalled

    def __str__(self):
        in_reg = False
        if self.input_inst_reg is not None:
            in_reg = True
            in_op = self.input_inst_reg.opcode
            in_fn = self.input_inst_reg.function

        return (
            f"{self.name:<20} "
            f"op: {in_op if in_reg else 'none':>4}, "
            f"fn: {in_fn if in_reg else 'none':>4}")

    def is_idle(self):
        """
        Return a status if a stage is ready to get an instruction to execute.
        :return:
        """
        return True if self.cycle_required == self.cycle_executed else False

    def _is_finish(self):
        return True if self.input_inst_reg is None else False

    def _feed_inst_reg(self, inst_reg):
        self.input_inst_reg = inst_reg

        if self.input_inst_reg is not None:
            self.cycle_required = self._get_required_cycle()

    def _get_required_cycle(self):
        return 1

    def _handle(self):
        raise ValueError("not implemented: Stage._handle(self). should override it in derived classes.")

    def _should_skip(self):
        raise ValueError("not implemented: Stage._should_skip(self). should override it in derived classes.")
