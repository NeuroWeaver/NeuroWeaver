from simd_sim.simulator.stage import Stage
from simd_sim.simulator.instruction import InstructionRegister


class InstructionFetch(Stage):
    def __init__(self, simd_lane_cnt):
        super(InstructionFetch, self).__init__(simd_lane_cnt)
        self.name = "InstructionFetch"
        self.inst_list = []

        # act like pc
        self.pc = 0
        self.pc_end = None
        self.pc_loop_start = None

        # for loop
        self.is_looping = False
        self.inst_cnt_per_loop = None
        self.is_nested = False

        # ALU loop iterations: (left_redo_loop + 1) times
        self.left_redo_loop = 0

        # ld/st base loop iterations: (left_redo_base_loop + 1) times
        self.left_redo_base_loop = 0

        # delegators, but access data directly for now
        self.decode = None
        self.address_generation = None

    def _handle(self):
        return self.input_inst_reg

    def feed_inst(self, instruction):
        if instruction is not None:
            self._feed_inst_reg(InstructionRegister(instruction))

    def iter_loop_inst(self):
        overhead_cycle = 0

        if self.left_redo_loop > 0:
            # print(self.pc, self.left_redo_loop, self.pc_loop_start, self.inst_cnt_per_loop)
            
            if self.pc == self.pc_loop_start + self.inst_cnt_per_loop:
                self.pc = self.pc_loop_start
                self.left_redo_loop -= 1
                overhead_cycle = 1 if not self.is_nested else 0

                if self.left_redo_loop == 0:
                    self.is_looping = False

        return overhead_cycle

    def start_loop(self, instruction_cnt, left_iteration_cnt, is_nested):
        self.inst_cnt_per_loop = instruction_cnt
        self.left_redo_loop = left_iteration_cnt
        self.is_nested = is_nested
        self.pc_loop_start = self.pc
        self.is_looping = True

    def set_base_loop(self, left_iteration_cnt):
        self.left_redo_base_loop = left_iteration_cnt

    def pull_inst_reg(self, prev_stage):
        if prev_stage is not None:
            raise ValueError(f"instruction fetch must not have a previous stage")

        if self.is_idle():
            self.input_inst_reg = None
            self.output_inst_reg = None

            self.pc += 1

            overhead_cycle = 0
            if self.is_looping:
                overhead_cycle = self.iter_loop_inst()

            if self.pc < self.pc_end:
                if self.pc == self.pc_end - 1:
                    self.__handle_base_loop()

                inst = self.inst_list[self.pc]

                self.feed_inst(inst)
                if overhead_cycle > 0:
                    self.cycle_required += overhead_cycle

    def __handle_base_loop(self):
        if self.left_redo_base_loop > 0:
            self.pc = 1
            self.left_redo_base_loop -= 1

            self.decode.should_inc_base_iter = True
            #print(f"left base loop: {self.left_redo_base_loop}")
