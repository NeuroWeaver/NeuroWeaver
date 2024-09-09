from simd_sim.simulator.stage import Stage, ns_dict
import numpy as np


def gen_offsets(iters):
    len_iters = len(iters)
    offsets = []
    for i in range(len_iters):
        if i == len_iters - 1:
            offsets.append(1)
        else:
            offsets.append(int(np.prod(iters[i + 1:])))

    return offsets


def calc_idx(iter, strides, offsets, debug = False):
    result = 0
    #if debug:
    # print (f"{len(strides)} {len(offsets)})")

    #print(strides)
    for i in range(len(offsets)):
        # print (f"i = {i}")
        # print (f"{strides[i]} * ({iter} // {offsets[i]})")

        result += strides[i] * (iter // offsets[i])
        iter %= offsets[i]
    return result


def calc_loop_id(iter, iters):
    ranges = [np.prod(iters[i:]) for i in range(len(iters))]

    for i in range(ranges):
        if iter < ranges[i]:
            loop_id = i

    return loop_id

class Tlist(list):
    def append(self, value):
        super(Tlist, self).append(value)


class AddressGeneration(Stage):
    def __init__(self, simd_lane_cnt, banked_memory, dest_bank_write_address):
        super(AddressGeneration, self).__init__(simd_lane_cnt)
        self.name = "AddressGeneration"
        
        # for permutation
        self.is_permuting =False
        self.bank_shuffle = False
        self.src_loop_iters = []
        self.dest_loop_iters = []
        self.src_offsets = None
        self.dest_offsets = None
        self.src_strides = []
        self.dest_strides = []
        
        self.dest_bank = 0
        self.dest_bank_write_address = dest_bank_write_address
        self.permutation_src_base_addr = 0
        self.permutation_src_index_tables = [
            {"num-iteration": 0, "stride": 0} for _ in range(32)
        ]
        self.permutation_dest_base_addr = 0
        self.permutation_dest_index_tables = [
            {"num-iteration": 0, "stride": 0} for _ in range(32)
        ]
        
        # for loop
        self.index_tables = {
            "obuf": [{"base": 0, "stride": 0} for _ in range(32)],
            "ibuf": [{"base": 0, "stride": 0} for _ in range(32)],
            "vmem1": [{"base": 0, "stride": 0} for _ in range(32)],
            "vmem2": [{"base": 0, "stride": 0} for _ in range(32)],
            "imm": [{"base": 0, "stride": 0} for _ in range(32)]  # imm have only base stride is always zero
        }
        self.loop_iter_tables = [
            0 for _ in range(32)
        ]
        self.loop_iters = []
        self.loop_indices = []
        self.is_nested = False
        self.iteration_cnt = 0

        self.is_looping = False
        self.total_iteration_cnt = 0

        self.offsets = None
        self.dst_strides = []
        self.src1_strides = []
        self.src2_strides = []

        self.is_loop_indice_fixed = False

        self.banked_memory = banked_memory
    
    # @property
    # def loop_indices(self):
    #     return self._loop_indices
    
    # @loop_indices.setter
    # def loop_indices(self, value):
    #     self._loop_indices.append(value)
    
    def pull_inst_reg(self, prev_stage):
        is_stalled = True

        if self.is_idle():
            self.input_inst_reg = None
            self.output_inst_reg = None

            if prev_stage is not None:
                if prev_stage.is_idle():
                    self._feed_inst_reg(prev_stage.output_inst_reg)
                    prev_stage.output_inst_reg = None
                    is_stalled = False
                elif prev_stage.is_permuting:
                    self._feed_inst_reg(prev_stage.output_inst_reg)
                    is_stalled = False

        return is_stalled

    def __start_loop(self):
        """
        start ALU loop
        """

        '''
        clear variables
        '''
        self.loop_iters.clear()
        self.dst_strides.clear()
        self.src1_strides.clear()
        self.src2_strides.clear()
        self.iteration_cnt = 0

        '''
        a new set of loop iterations to calculate total # of iterations:
        [an example]:
        for i range(3):
          for j in range(4):
             ...
        => self.loop_iters = [3, 4]
        '''
        for loop_iter in self.loop_iter_tables:
            if loop_iter != 0:
                self.loop_iters.append(loop_iter)
        self.offsets = gen_offsets(self.loop_iters)

        for i in range(len(self.loop_indices)):
            index = self.loop_indices[i]

            _, stride = self.__read_index_table(ns=ns_dict[index["dst-ns-id"]],
                                                index_id=index["dst-index-id"])
            self.dst_strides.append(stride)

            _, stride = self.__read_index_table(ns=ns_dict[index["src1-ns-id"]],
                                                index_id=index["src1-index-id"])
            self.src1_strides.append(stride)

            _, stride = self.__read_index_table(ns=ns_dict[index["src2-ns-id"]],
                                                index_id=index["src2-index-id"])
            self.src2_strides.append(stride)

        '''
        set other related variables
        '''
        self.is_nested = bool(self.input_inst_reg.dst_ns_id)
        self.is_loop_indice_fixed = True
        self.is_looping = True

    def _handle(self):
        # print(f'{self.name}')
        if self._should_skip():
            return self.input_inst_reg
        opcode = self.input_inst_reg.opcode
        # if self.is_looping:
        #     self.__handle_loop()
        if opcode == 6:
            self.__handle_iterator_config()
        elif opcode == 7:
            self.__handle_loop_config()
        elif opcode == 8:
            self.__handle_permutation()
        elif opcode != 14:
            self.__handle_loop()

        return self.input_inst_reg

    def _should_skip(self):
        # we accept nop in this stage because of the NOP loop
        opcode = self.input_inst_reg.opcode
        if opcode == 4 or opcode == 5 or opcode == 10 or opcode == 14:
            return True

        return False

    def __handle_loop_config(self):
        function = self.input_inst_reg.function

        '''
        SET_INDEX:
        each loop index of a namespace has base/stride information
        in a same loop, dst/src1/src2 can have different base addresses and their strides
        they only share # of iterations
        '''
        if function == 0:
            if not self.is_loop_indice_fixed:
                self.loop_indices.append({
                    "dst-ns-id": self.input_inst_reg.dst_ns_id,
                    "dst-index-id": self.input_inst_reg.dst_index_id,
                    "src1-ns-id": self.input_inst_reg.src1_ns_id,
                    "src1-index-id": self.input_inst_reg.src1_index_id,
                    "src2-ns-id": self.input_inst_reg.src2_ns_id,
                    "src2-index-id": self.input_inst_reg.src2_index_id
                })

        # SET_ITER: set loop iteration
        elif function == 1:
            loop_id = self.input_inst_reg.dst_ns_id
            iteration_cnt = self.input_inst_reg.immediate

            self.loop_iter_tables[loop_id] = iteration_cnt

        # SET_INST: set # of instruction and start ALU loop
        elif function == 2:
            self.__start_loop()

    def __handle_permutation(self):
        function = self.input_inst_reg.function
        
        # SET_BASE_ADDR
        if function == 0:
            base_addr = self.input_inst_reg.immediate
            
            if self.input_inst_reg.dst_ns_id == 0:
                self.permutation_src_base_addr = base_addr
            elif self.input_inst_reg.dst_ns_id == 1:
                self.permutation_dest_base_addr = base_addr
            else:
                raise ValueError(f"Permutatoion Base Address Configure Error on Src/Dst")
        
        # SET_LOOP_ITER
        elif function == 1:
            index_id = self.input_inst_reg.dst_index_id
            num_iteration = self.input_inst_reg.immediate
            
            if self.input_inst_reg.dst_ns_id == 0:
                self.permutation_src_index_tables[index_id]["num-iteration"] = num_iteration
            elif self.input_inst_reg.dst_ns_id == 1:
                self.permutation_dest_index_tables[index_id]["num-iteration"] = num_iteration
            else:
                raise ValueError(f"Permutatoion Iter Configure Error on Src/Dst")
        
        # SET_LOOP_STRIDE
        elif function == 2:
            index_id = self.input_inst_reg.dst_index_id
            stride = self.input_inst_reg.immediate
            
            if self.input_inst_reg.dst_ns_id == 0:
                self.permutation_src_index_tables[index_id]["stride"] = stride
            elif self.input_inst_reg.dst_ns_id == 1:
                self.permutation_dest_index_tables[index_id]["stride"] = stride
            else:
                raise ValueError(f"Permutatoion Stride Address Configure Error on Src/Dst")
        
        # Start and supply addresses
        elif function == 3:
            if not self.is_permuting:
                #print("start permute")
                self.__start_permute()
            else:
                #print("handle permute")
                self.__handle_permute()
                
        else:
            raise ValueError(f"invalid function ({function}) in permutation")
    
    def __start_permute(self):
        self.src_loop_iters.clear()
        self.dest_loop_iters.clear()
        self.src_strides.clear()
        self.dest_strides.clear()
        self.iteration_cnt = 0
        
        for row in self.permutation_src_index_tables:
            iteration = row["num-iteration"]
            stride = row["stride"]
            if iteration != 0:
                self.src_loop_iters.append(iteration)
                self.src_strides.append(stride)
                
        for row in self.permutation_dest_index_tables:
            iteration = row["num-iteration"]
            stride = row["stride"]
            if iteration != 0:
                self.dest_loop_iters.append(iteration)
                self.dest_strides.append(stride)
        
        self.src_offsets = gen_offsets(self.src_loop_iters)
        self.dest_offsets = gen_offsets(self.dest_loop_iters)
        
        self.is_permuting = True 
        self.input_inst_reg.first_permute = True 
        self.bank_shuffle = (self.input_inst_reg.src2_index_id == 1)
        
    def __handle_permute(self):
        if self.is_permuting:
            if self.input_inst_reg.first_permute:
                self.input_inst_reg.first_permute = False
            
            if not self.input_inst_reg.is_nop():
                self.__gen_addr_permutation()
            
            self.iteration_cnt += 1
            
            # Permutation Done Reset Everything 
            if self.total_iteration_cnt == self.iteration_cnt:
                self.is_permuting =False
                self.bank_shuffle = False
                self.is_base_looping = False
                self.permutation_src_base_addr = 0
                self.permutation_dest_base_addr = 0
                
                for row in self.permutation_src_index_tables:
                    row["num-iteration"] = 0
                    row["stride"] = 0
                    
                for row in self.permutation_dest_index_tables:
                    row["num-iteration"] = 0
                    row["stride"] = 0               
           
    def __gen_addr_permutation(self):
        #print("CALLLLL!!!! in addr gen")
        self.input_inst_reg.dest_bank = self.iteration_cnt % self.simd_lane_cnt
        self.input_inst_reg.addr_dst = self.permutation_dest_base_addr + calc_idx(self.iteration_cnt, self.dest_strides, self.dest_offsets)
        self.input_inst_reg.addr_src1 = self.permutation_src_base_addr + calc_idx(self.iteration_cnt, self.src_strides, self.src_offsets)
        
    def __gen_addr_nested_loop(self):
        # innermost loop index
        if (len(self.loop_indices) > 0):
            last_index = self.loop_indices[-1]
            base_dst, _ = self.__read_index_table(ns=ns_dict[last_index["dst-ns-id"]],
                                                index_id=last_index["dst-index-id"])

            base_src1, _ = self.__read_index_table(ns=ns_dict[last_index["src1-ns-id"]],
                                                index_id=last_index["src1-index-id"])

            base_src2, _ = self.__read_index_table(ns=ns_dict[last_index["src2-ns-id"]],
                                                index_id=last_index["src2-index-id"])
            
            self.input_inst_reg.addr_dst = base_dst + calc_idx(self.iteration_cnt, self.dst_strides, self.offsets)
            #print ('\n')
            self.input_inst_reg.addr_src1 = base_src1 + calc_idx(self.iteration_cnt, self.src1_strides, self.offsets)
            self.input_inst_reg.addr_src2 = base_src2 + calc_idx(self.iteration_cnt, self.src2_strides, self.offsets)

    def __gen_addr_single_loop(self):
        base_dst, stride_dst = self.__read_index_table(ns=ns_dict[self.input_inst_reg.dst_ns_id],
                                                       index_id=self.input_inst_reg.dst_index_id)

        base_src1, stride_src1 = self.__read_index_table(ns=ns_dict[self.input_inst_reg.src1_ns_id],
                                                         index_id=self.input_inst_reg.src1_index_id)

        base_src2, stride_src2 = self.__read_index_table(ns=ns_dict[self.input_inst_reg.src2_ns_id],
                                                         index_id=self.input_inst_reg.src2_index_id)

        iter_cnt = self.iteration_cnt

        self.input_inst_reg.addr_dst = base_dst * iter_cnt * (stride_dst)
        self.input_inst_reg.addr_src1 = base_src1 * iter_cnt * (stride_src1)
        self.input_inst_reg.addr_src2 = base_src2 * iter_cnt * (stride_src2)

    def __read_index_table(self, ns, index_id):
        return self.index_tables[ns][index_id]["base"], self.index_tables[ns][index_id]["stride"]

    def __handle_iterator_config(self):
        # iterator config (opcode: 0110)
        dst_ns = ns_dict[self.input_inst_reg.dst_ns_id]
        dst_index_id = self.input_inst_reg.dst_index_id

        # immediate must be under '2^16 - 1' (65535)
        if np.uint32(self.input_inst_reg.immediate) > 65535:
            raise ValueError(f"immediate must be under 65535 (2^16 - 1), but it is {self.input_inst_reg.immediate}")

        imm_16_bit = np.uint16(self.input_inst_reg.immediate)
        max_16_bit = np.uint16(pow(2, 16) - 1)
        max_high_32_bit = np.uint32(np.uint32(max_16_bit) << 16)  # just shifting in numpy make its type as int64
        max_low_32_bit = np.uint32(max_16_bit)

        function = self.input_inst_reg.function
        if function // 8 == 1:
            # set imm
            prev_imm_32_bit = np.uint32(self.index_tables["imm"][dst_index_id]["base"])

            remainder = function % 8
            if remainder == 0:
                # clear low bits & set
                immediate = np.int32((max_high_32_bit & prev_imm_32_bit) ^ np.uint32(imm_16_bit))
            elif remainder == 1:
                # clear high bits & set
                imm_32_bit = np.uint32(imm_16_bit << 16)
                immediate = np.int32((max_low_32_bit & prev_imm_32_bit) ^ imm_32_bit)
            elif remainder == 2:
                # signed extension
                immediate = np.int32(np.int16(imm_16_bit))
            else:
                raise ValueError(f"invalid function bits for SET_IMMEDIATE: {function}")

            self.banked_memory["imm"][dst_index_id] = immediate

        else:
            # set base or stride
            dst_key = "base" if function >> 2 == 0 else "stride"
            prev_32_bit = np.uint32(self.index_tables[dst_ns][dst_index_id][dst_key])

            remainder = function % 4
            if remainder == 0:
                # signed extension
                immediate = np.int32(np.int16(imm_16_bit))
            elif remainder == 1:
                # clear low bits & set
                immediate = np.int32((max_high_32_bit & prev_32_bit) ^ np.uint32(imm_16_bit))
            elif remainder == 2:
                # clear high bits & set
                imm_32_bit = np.uint32(imm_16_bit << 16)
                immediate = np.int32((max_low_32_bit & prev_32_bit) ^ imm_32_bit)
            elif remainder == 3:
                # zero fill
                immediate = np.int32(imm_16_bit)
            else:
                raise ValueError(f"invalid function bits to set BASE/STRIDE: {function}")

            self.index_tables[dst_ns][dst_index_id][dst_key] = immediate

    # Assumption is PC should not increament util loop handling is done
    def __handle_loop(self):
        if self.is_looping:
            if not self.input_inst_reg.is_nop():
                if self.is_nested:
                    self.__gen_addr_nested_loop()
                else:
                    self.__gen_addr_single_loop()

            self.iteration_cnt += 1

            # print(self.iteration_cnt, self.total_iteration_cnt)
            
            if self.total_iteration_cnt == self.iteration_cnt:
                '''
                stop looping
                '''
                for i in range(len(self.loop_iter_tables)):
                    self.loop_iter_tables[i] = 0

                for key in self.index_tables.keys():
                    table = self.index_tables[key]

                    if key == "imm":
                        for i in range(len(table)):
                            table[i]["base"] = 0
                    else:
                        for i in range(len(table)):
                            table[i]["base"] = 0
                            table[i]["stride"] = 0

                '''
                reset variables
                '''
                self.iteration_cnt = 0
                self.is_looping = False
                #print ('Reinitializing Loop Indices')
                self.is_base_looping = False
                self.loop_indices = Tlist()
                self.is_loop_indice_fixed = False

    def set_total_iteration_cnt(self, total_iteration_cnt):
        self.total_iteration_cnt = total_iteration_cnt
