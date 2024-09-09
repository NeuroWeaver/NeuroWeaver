from distutils.command.config import config
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


def calc_idx(iter, strides, offsets):
    result = 0

    for i in range(len(offsets)):
        result += strides[i] * (iter // offsets[i])
        iter %= offsets[i]

    return result


def calc_loop_id(iter, iters):
    ranges = [np.prod(iters[i:]) for i in range(len(iters))]

    for i in range(ranges):
        if iter < ranges[i]:
            loop_id = i

    return loop_id


class Decode(Stage):
    def __init__(self, simd_lane_cnt, ld_st_bandwidth_per_cycle, ld_st_booting_time_cycle, banked_memory, ddr_memory):
        super(Decode, self).__init__(simd_lane_cnt)
        self.name = "Decode"
        self.index_tables = {
            "obuf": [{"base": 0, "stride": 0} for _ in range(32)],
            "ibuf": [{"base": 0, "stride": 0} for _ in range(32)],
            "vmem1": [{"base": 0, "stride": 0} for _ in range(32)],
            "vmem2": [{"base": 0, "stride": 0} for _ in range(32)],
            # "imm": [{"base": 0} for _ in range(32)] # imm have only base stride is always zero
        }
        self.loop_iter_tables = [
            0 for _ in range(32)
        ]
        self.ld_index_tables = {
            "vmem1-data-width": 0,
            "vmem1-req-size": 0,
            "vmem1": [{"base-addr": 0,
                       "tile-addr": 0,
                       "base-loop-iter": 0, "base-loop-stride": 0,
                       "tile-loop-iter": 0, "tile-loop-stride": 0} for _ in range(32)],
            "vmem2-data-width": 0,
            "vmem2-req-size": 0,
            "vmem2": [{"base-addr": 0,
                       "tile-addr": 0,
                       "base-loop-iter": 0, "base-loop-stride": 0,
                       "tile-loop-iter": 0, "tile-loop-stride": 0} for _ in range(32)],
        }
        self.st_index_tables = {
            "vmem1-data-width": 0,
            "vmem1-req-size": 0,
            "vmem1": [{"base-addr": 0,
                       "tile-addr": 0,
                       "base-loop-iter": 0, "base-loop-stride": 0,
                       "tile-loop-iter": 0, "tile-loop-stride": 0} for _ in range(32)],
            "vmem2-data-width": 0,
            "vmem2-req-size": 0,
            "vmem2": [{"base-addr": 0,
                       "tile-addr": 0,
                       "base-loop-iter": 0, "base-loop-stride": 0,
                       "tile-loop-iter": 0, "tile-loop-stride": 0} for _ in range(32)],
        }
        self.permutation_base_addr = 0
        self.permutation_index_tables = [
            {"num-iteration": 0, "stride": 0} for _ in range(32)
        ]
        self.is_permuting = False
        self.permutation_total_iteration = 0
        self.permutation_iteration_cnt = 0
        self.ld_st_bandwidth_per_cycle = ld_st_bandwidth_per_cycle
        self.ld_st_booting_time_cycle = ld_st_booting_time_cycle
        self.banked_memory = banked_memory
        self.ddr_memory = ddr_memory
        self.is_ld_st_data_transfer = False
        self.tile_total_iteration = 0
        self.tile_iteration_cnt = 0
        self.curr_tile_idx = 0
        self.req_total_iteration = 0

        self.base_total_iteration = 0
        self.base_iteration_cnt = 0
        self.should_inc_base_iter = False
        self.curr_base_idx = 0
        self.is_base_looping = False

        self.base_offsets = None
        self.tile_offsets = None
        self.base_strides = None
        self.tile_strides = None
        self.tile_iters_prod = None

        self.should_wait_for_alu = False

        #ld st tile sizes
        # self.ld_sizes = []
        # self.st_sizes = []
        # self.ld_st_size = 1
    
    def cycle(self):
        """
        Implement a cycle for a stage.
        """
        if self.is_idle() or self.input_inst_reg is None:
            return

        if self.cycle_executed == 0 or self.is_permuting or self.is_ld_st_data_transfer:
            self.output_inst_reg = self._handle()

        if self.cycle_executed + 1 == self.cycle_required:
            # set as idle
            self.cycle_executed = 0
            self.cycle_required = 0

            if self.is_permuting:
                self.is_permuting = False
        else:
            self.cycle_executed += 1

    def _handle(self):
        if self.input_inst_reg.is_nop():
            return self.input_inst_reg

        opcode = self.input_inst_reg.opcode

        if opcode > 4:
            if opcode == 5:
                self.__handle_load_and_store()
            elif opcode == 6:
                pass
            elif opcode == 7:
                self.__handle_loop()
            elif opcode == 8:
                self.__handle_permutation()

        return self.input_inst_reg

    def __read_index_table(self, ns, index_id):
        return self.index_tables[ns][index_id]["base"], self.index_tables[ns][index_id]["stride"]

    def __handle_load_and_store(self):
        function = self.input_inst_reg.function
        
        #--------- Record ld/st vmem read and write ---------#
        #--------- Record ld/st vmem read and write ---------#
        #--------- Record ld/st vmem read and write ---------#
        if self.input_inst_reg.opcode == 5:
            if self.input_inst_reg.function == 5:
                dst_ns = ns_dict[self.input_inst_reg.dst_ns_id]
                if dst_ns == 'vmem1' or dst_ns == 'vmem2':
                    for i in range(self.simd_lane_cnt):
                        self.statistics["memory-access"][dst_ns][i]["ldWrite"] += 1
            elif self.input_inst_reg.function == 13:
                dst_ns = ns_dict[self.input_inst_reg.dst_ns_id]
                if dst_ns == 'vmem1' or dst_ns == 'vmem2':
                    for i in range(self.simd_lane_cnt):
                        self.statistics["memory-access"][dst_ns][i]["stRead"] += 1

        #--------- Record ld/st vmem read and write ---------#
        #--------- Record ld/st vmem read and write ---------#
        #--------- Record ld/st vmem read and write ---------#       
        is_store = True if function // 8 == 1 else False
        index_tables = self.st_index_tables if is_store else self.ld_index_tables

        is_msb = True if self.input_inst_reg.dst_ns_id // 4 == 1 else False
        ns_id = self.input_inst_reg.dst_ns_id % 4
        index_id = self.input_inst_reg.dst_index_id
        immediate = self.input_inst_reg.immediate

        #############################
        # Calculating ld/st tile size
        #############################
        #############################

        # if self.input_inst_reg.opcode == 5:
        #     if self.input_inst_reg.function == 5:
        #         tile_iter = 1
        #         ld_size = immediate
        #         for i in range(32):
        #             iter = index_tables[ns_dict[ns_id]][i]['tile-loop-iter']
        #             if iter != 0:
        #                 tile_iter *= iter
        #         print("ld_size ", ld_size)
        #         print("tile_iter ", tile_iter)

        # if self.input_inst_reg.opcode == 5:
        #     if self.input_inst_reg.function == 13:
        #         tile_iter = 1
        #         st_size = immediate
        #         for i in range(32):
        #             iter = index_tables[ns_dict[ns_id]][i]['tile-loop-iter']
        #             if iter != 0:
        #                 tile_iter *= iter
        #         print("st_size", st_size)
        #         print("tile_iter", tile_iter)

        # for setting 32-bit data
        imm_16_bit = np.uint16(immediate)
        max_16_bit = np.uint16(pow(2, 16) - 1)
        max_high_32_bit = np.uint32(np.uint32(max_16_bit) << 16)  # just shifting in numpy make its type as int64
        max_low_32_bit = np.uint32(max_16_bit)

        fn_low_3_bit = function % 8
        if fn_low_3_bit == 0:
            # set BASE_ADDR
            prev_imm_32_bit = np.uint32(index_tables[ns_dict[ns_id]][index_id]["base-addr"])
            if is_msb:
                imm_32_bit = np.uint32(imm_16_bit << 16)
                immediate = np.int32((max_low_32_bit & prev_imm_32_bit) ^ imm_32_bit)
            else:
                # set lower 16 bits
                immediate = np.int32((max_high_32_bit & prev_imm_32_bit) ^ np.uint32(imm_16_bit))

            index_tables[ns_dict[ns_id]][index_id]["base-addr"] = np.int32(immediate)
        elif fn_low_3_bit == 1:
            index_tables[ns_dict[ns_id]][index_id]["base-loop-iter"] = np.int32(immediate) + 1
            #print (index_tables[ns_dict[ns_id]][index_id]["base-loop-iter"])
        elif fn_low_3_bit == 2:
            prev_imm_32_bit = np.uint32(index_tables[ns_dict[ns_id]][index_id]["base-loop-stride"])
            if is_msb:
                imm_32_bit = np.uint32(imm_16_bit << 16)
                immediate = np.int32((max_low_32_bit & prev_imm_32_bit) ^ imm_32_bit)
            else:
                # set lower 16 bits
                immediate = np.int32((max_high_32_bit & prev_imm_32_bit) ^ np.uint32(imm_16_bit))

            index_tables[ns_dict[ns_id]][index_id]["base-loop-stride"] = np.int32(immediate)
        elif fn_low_3_bit == 3:
            index_tables[ns_dict[ns_id]][index_id]["tile-loop-iter"] = np.int32(immediate) + 1
        elif fn_low_3_bit == 4:
            prev_imm_32_bit = np.uint32(index_tables[ns_dict[ns_id]][index_id]["tile-loop-stride"])
            if is_msb:
                imm_32_bit = np.uint32(imm_16_bit << 16)
                immediate = np.int32((max_low_32_bit & prev_imm_32_bit) ^ imm_32_bit)
            else:
                # set lower 16 bits
                immediate = np.int32((max_high_32_bit & prev_imm_32_bit) ^ np.uint32(imm_16_bit))

            index_tables[ns_dict[ns_id]][index_id]["tile-loop-stride"] = np.int32(immediate)

        elif fn_low_3_bit == 5:
            if self.is_ld_st_data_transfer:
                if self.should_wait_for_alu:
                    if self.cycle_executed < self.simd_lane_cnt:
                        return

                    self.should_wait_for_alu = False

                bw = self.ld_st_bandwidth_per_cycle // 4

                banked_mem = self.banked_memory[ns_dict[ns_id]]

                base_iter = self.base_iteration_cnt

                tile_iter = self.tile_iteration_cnt // self.req_total_iteration
                req_idx = (self.tile_iteration_cnt % self.req_total_iteration) * bw

                base_idx = calc_idx(base_iter, self.base_strides, self.base_offsets)
                tile_idx = calc_idx(tile_iter, self.tile_strides, self.tile_offsets)

                tile_addr = index_tables[ns_dict[ns_id]][0]["tile-addr"] * self.simd_lane_cnt
                idx_bm = self.curr_tile_idx + tile_addr

                base_addr = index_tables[ns_dict[ns_id]][0]["base-addr"] // 4
                ddr_idx = base_addr + base_idx + tile_idx + req_idx

                if is_store:
                    pass
                # rohan commented; fix later
                    #self.ddr_memory[ddr_idx:ddr_idx + bw] = banked_mem.transpose().flat[idx_bm:idx_bm + bw]
                else:
                    pass
                    #banked_mem.transpose().flat[idx_bm:idx_bm + bw] = self.ddr_memory[ddr_idx:ddr_idx + bw]

                self.curr_tile_idx += bw

                self.tile_iteration_cnt += 1
                if self.tile_iteration_cnt == self.tile_total_iteration:
                    self.is_ld_st_data_transfer = False
                    self.tile_iteration_cnt = 0
                    self.curr_tile_idx = 0
                    self.req_total_iteration = 0

                    if self.should_inc_base_iter:
                        self.base_iteration_cnt += 1
                        self.should_inc_base_iter = False
            else:
                index_tables[f"{ns_dict[ns_id]}-data-width"] = index_id
                req_size = np.int32(immediate)
                index_tables[f"{ns_dict[ns_id]}-req-size"] = req_size
                req_cnt = req_size // 4
                # bw: elements per cycle
                bw = self.ld_st_bandwidth_per_cycle // 4
                self.req_total_iteration = (self.simd_lane_cnt * req_cnt) // bw

                base_iters = []
                self.base_strides = []
                tile_iters = []
                self.tile_strides = []

                for i in range(32):
                    base_iter = index_tables[ns_dict[ns_id]][i]["base-loop-iter"]
                    base_stride = index_tables[ns_dict[ns_id]][i]["base-loop-stride"]
                    if base_iter > 1:
                        base_iters.append(base_iter)
                        if base_stride % 4 != 0:
                            raise ValueError(f"stride {base_stride} cannot divided by 4")
                        self.base_strides.append(base_stride // 4)

                    tile_iter = index_tables[ns_dict[ns_id]][i]["tile-loop-iter"]
                    tile_stride = index_tables[ns_dict[ns_id]][i]["tile-loop-stride"]
                    if tile_iter > 1:
                        tile_iters.append(tile_iter)
                        if tile_stride % 4 != 0:
                            raise ValueError(f"stride {tile_stride} cannot divided by 4")
                        self.tile_strides.append(tile_stride // 4)

                self.base_offsets = gen_offsets(base_iters)
                self.tile_offsets = gen_offsets(tile_iters)

                # calculation of st/ld data size based on instruction ASPLOS24
                # data width and simd lane counted
                self.tile_iters_prod = int(np.prod(tile_iters))
                # data_width_in_byte = (index_tables[f"{ns_dict[ns_id]}-data-width"]+1)/8 already in byte
                tile_req_size = self.tile_iters_prod * req_size * self.simd_lane_cnt # * data_width_in_byte

                self.is_ld_st_data_transfer = True
                self.tile_total_iteration = self.tile_iters_prod #* self.req_total_iteration
                if is_store:
                    self.pipeline.profiler.st_req_sizes.append(tile_req_size)
                else:
                    self.pipeline.profiler.ld_req_sizes[ns_dict[ns_id]] += tile_req_size
                self.cycle_required += self.tile_total_iteration

                if is_store:
                    self.should_wait_for_alu = True

                if self.ld_st_booting_time_cycle != 0:
                    raise ValueError("ld_st_booting_time_cycle is not 0")
        # TILE_ADDR
        elif fn_low_3_bit == 6:
            # set BASE_ADDR
            prev_imm_32_bit = np.uint32(index_tables[ns_dict[ns_id]][index_id]["tile-addr"])
            if is_msb:
                imm_32_bit = np.uint32(imm_16_bit << 16)
                immediate = np.int32((max_low_32_bit & prev_imm_32_bit) ^ imm_32_bit)
            else:
                # set lower 16 bits
                immediate = np.int32((max_high_32_bit & prev_imm_32_bit) ^ np.uint32(imm_16_bit))

            index_tables[ns_dict[ns_id]][index_id]["tile-addr"] = np.int32(immediate)
        else:
            raise ValueError(f"invalid function: {bin(fn_low_3_bit)} at opcode: {bin(self.input_inst_reg.opcode)}")
        


    def __handle_loop(self):
        function = self.input_inst_reg.function

        # loop
        if function == 0:
            pass

        elif function == 1:
            loop_id = self.input_inst_reg.dst_ns_id

            iteration_cnt = self.input_inst_reg.immediate
            self.loop_iter_tables[loop_id] = iteration_cnt

        elif function == 2:
            is_nested = bool(self.input_inst_reg.dst_ns_id)

            iteration_cnt = 1
            for i in range(32):
                if self.loop_iter_tables[i] != 0:
                    iteration_cnt *= self.loop_iter_tables[i]

            self.pipeline.start_alu_loop(instruction_cnt=self.input_inst_reg.immediate,
                                         iteration_cnt=int(iteration_cnt),
                                         is_nested=is_nested)

            for i in range(32):
                self.loop_iter_tables[i] = 0

            if not self.is_base_looping:
                iteration_cnt = 1
                ## todo: used ld_index_tables but this does not work for fused layers
                ## needs to use store index table
                for index_table in self.ld_index_tables["vmem1"]:
                    if index_table["base-loop-iter"] > 0:
                        iteration_cnt *= index_table["base-loop-iter"]
                self.pipeline.profiler.total_base_loop_iterations = iteration_cnt
                self.pipeline.try_to_set_base_loop(left_iteration_cnt=iteration_cnt - 1)
                self.is_base_looping = True

        else:
            raise ValueError(f"invalid function code: {function} in opcode 'loop'")

    def __handle_permutation(self):
        function = self.input_inst_reg.function

        if function == 0:
            # SET_BASE_ADDR
            base_addr = self.input_inst_reg.immediate
            self.permutation_base_addr = base_addr
        elif function == 1:
            # SET_LOOP_ITER
            index_id = self.input_inst_reg.dst_index_id
            num_iteration = self.input_inst_reg.immediate
            self.permutation_index_tables[index_id]["num-iteration"] = num_iteration
        elif function == 2:
            # SET_LOOP_STRIDE
            index_id = self.input_inst_reg.dst_index_id
            stride = self.input_inst_reg.immediate
            self.permutation_index_tables[index_id]["stride"] = stride
        elif function == 3:
            # START
            if not self.is_permuting:
                total_iteration = 1
                for i in range(32):
                    num_iteration = self.permutation_index_tables[i]["num-iteration"]
                    if num_iteration > 0:
                        total_iteration *= (num_iteration+1)
                
                self.pipeline.start_alu_loop(instruction_cnt=1,
                                         iteration_cnt= total_iteration,
                                         is_nested=True)
                
                self.cycle_required = total_iteration

                self.is_permuting = True
                
                if not self.is_base_looping:
                    iteration_cnt = 1
                    for index_table in self.ld_index_tables["vmem1"]:
                        if index_table["base-loop-iter"] > 0:
                            iteration_cnt *= index_table["base-loop-iter"]
                    self.pipeline.profiler.total_base_loop_iterations = iteration_cnt
                    self.pipeline.try_to_set_base_loop(left_iteration_cnt=iteration_cnt - 1)
                    self.is_base_looping = True
            
        else:
            raise ValueError(f"invalid function ({function}) in permutation")

