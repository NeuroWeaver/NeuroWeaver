from simd_sim.simulator.stage import Stage, read_data, execute, write_data
import copy


class ALU(Stage):
    def __init__(self, simd_lane_cnt, execution_idx, banked_memory, dest_bank_write_address, pipeline=None):
        super(ALU, self).__init__(simd_lane_cnt)
        self.name = "ALU"
        self.execution_idx = execution_idx
        self.banked_memory = banked_memory
        self.pipeline = pipeline
        self.dest_bank_write_address = dest_bank_write_address
        self.inst_queue = []

    def cycle(self):
        """
        Implement a cycle for a stage.
        """
        output_inst_reg = self._handle()

        if self.is_idle() or self.input_inst_reg is None:
            return

        if self.cycle_executed == 0:
            self.output_inst_reg = output_inst_reg

        if self.cycle_executed + 1 == self.cycle_required:
            # set as idle
            self.cycle_executed = 0
            self.cycle_required = 0
        else:
            self.cycle_executed += 1

    def _get_required_cycle(self):
        return 1

    def _is_finish(self):
        # TODO: check queue
        # return True if self.input_inst_reg is None else False

        is_empty_queue = True if len(self.inst_queue) == 0 else False
        is_empty_inst_reg = True if self.input_inst_reg is None else False

        return is_empty_inst_reg and is_empty_queue

    def _feed_inst_reg(self, inst_reg):
        self.input_inst_reg = inst_reg

        if self.input_inst_reg is not None:

            # if (inst_reg.opcode == 8 and inst_reg.function == 3):
            #     print(inst_reg.instruction)
            
            self.cycle_required = self._get_required_cycle()

            if not self._should_skip():
                # inst_reg = copy.deepcopy(self.input_inst_reg)
                inst_reg = self.input_inst_reg.copy_instr()
                inst_reg.remain_cycle = self.__calculate_remain_cycle(inst_reg.opcode,
                                                                      inst_reg.function)
                self.inst_queue.append(inst_reg)

    def _handle(self):
        if self.pipeline is not None and self.input_inst_reg is not None:
            self.pipeline.add_to_profiler(self.input_inst_reg)

        if len(self.inst_queue) > 0:
            for i in range(len(self.inst_queue)):
                self.inst_queue[i].remain_cycle -= 1

            if self.inst_queue[0].remain_cycle == 0:
                inst = self.inst_queue.pop(0)
                if inst.opcode != 13 and inst.opcode != 14:
                    bank_shuffling = (inst.src2_index_id == 1)
                    if inst.opcode == 8 and inst.function == 3 and bank_shuffling and not inst.first_permute:
                        # Update the write address at current bank
                        self.dest_bank_write_address[self.execution_idx] = inst.addr_dst
                        read_data(inst, self.execution_idx, self.banked_memory, self.statistics)
                        execute(inst, self.execution_idx, self.banked_memory, self.statistics)
                        # read from a different bank
                        actual_write_address = self.dest_bank_write_address[inst.dest_bank]
                        inst.addr_dst = actual_write_address
                        write_data(inst, inst.dest_bank, self.banked_memory, self.statistics)
                    else:
                        read_data(inst, self.execution_idx, self.banked_memory, self.statistics)
                        execute(inst, self.execution_idx, self.banked_memory, self.statistics)
                        write_data(inst, self.execution_idx, self.banked_memory, self.statistics)
                        
                    if inst.first_permute:
                        inst.first_permute = False

        return self.input_inst_reg

    def _should_skip(self):
        if self.input_inst_reg.is_nop():
            return True

        opcode = self.input_inst_reg.opcode
        if opcode == 4 or opcode == 5 or opcode == 6 or opcode == 7 or opcode == 10 or opcode == 11:
            return True

        if opcode == 8:
            if self.input_inst_reg.function < 3 or self.input_inst_reg.first_permute:                 
                return True

        return False

    def __calculate_remain_cycle(self, opcode, function):
        if opcode == 1:
            if function == 2:
                return 4

        return 1
