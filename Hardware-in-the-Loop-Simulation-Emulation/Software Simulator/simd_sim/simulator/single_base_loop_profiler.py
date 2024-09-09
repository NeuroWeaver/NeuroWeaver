from simd_sim.simulator.instruction import InstructionRegister
import numpy as np
import math 


class ProfiledInstruction:
    def __init__(self, inst_reg, ended_cycle):
        self.inst_reg = inst_reg
        self.ended_cycle = ended_cycle


class SingleBaseLoopProfiler:
    def __init__(self, config):
        self.config = config
        self.total_base_loop_iterations = None
        self.stage_cnt = None
        self.profiled_inst = []
        self.can_add = True
        self.ld_req_sizes = {"vmem1":0, "vmem2":0}
        self.st_req_sizes = []
        self.prev_reg = None

    def add(self, input_reg, ended_cycle):
        if self.__can_add(input_reg):
            self.profiled_inst.append(ProfiledInstruction(inst_reg=input_reg, ended_cycle=ended_cycle))

        self.prev_reg = input_reg

    def finish(self):
        self.can_add = False

    def profile(self):
        cycles = []
        ended_cycles = []
        insts = []
        log_cycles = 0
        loadCycles, loadTileSizes = self.__calculate_load_cycles_instruction_based()
        storeCycles, storeTileSizes = self.__calculate_store_cycles_instruction_based()

        for inst in self.profiled_inst:
            ended_cycles.append(inst.ended_cycle)
            insts.append(inst.inst_reg)

            # print(inst.inst_reg.instruction)
            # print(inst.ended_cycle)

        for i in range(len(self.profiled_inst)-1):
            if (self.profiled_inst[i].inst_reg.opcode == 0 or self.profiled_inst[i].inst_reg.opcode == 1
                    or self.profiled_inst[i].inst_reg.opcode == 2 or self.profiled_inst[i].inst_reg.opcode == 3 or 
                    self.profiled_inst[i].inst_reg.opcode == 10):
                
                # print(self.profiled_inst[i].inst_reg.instruction)
                # print(ended_cycles[i+1] - ended_cycles[i])
                if self.profiled_inst[i].inst_reg.is_nop():
                    cycles.append((ended_cycles[i+1] - ended_cycles[i])/2)
                # 5 time energy for 
                if self.profiled_inst[i].inst_reg.opcode == 1 and self.profiled_inst[i].inst_reg.function == 10:
                    log_cycles += (ended_cycles[i+1] - ended_cycles[i]) * 5
                    cycles.append(ended_cycles[i+1] - ended_cycles[i])
                else:
                    cycles.append(ended_cycles[i+1] - ended_cycles[i])

        total_cycle = 2 + (self.total_base_loop_iterations * np.sum(cycles) - 1) + self.stage_cnt
        #print("Per tile Compute Cycle: ", np.sum(cycles))
        perTileCycles = 2 + np.sum(cycles) + self.stage_cnt
        #print("Per tile Compute Cycle : ", perTileCycles)

        delays_per_base_iter = 0
        delays_per_base_iter += self.config["state-change-cnt"]

        delay_scale = self.config["ld-scale-of-delay"]

        #print ("ld size = ", self.ld_req_sizes)
        ## Replace below with Load/Store Time
        # for ld_req_size in self.ld_req_sizes:
        #     delays_per_base_iter += ld_req_size * delay_scale + self.config["ld-init-delay-cycles"]

        # delay_scale = self.config["st-scale-of-delay"]
        # for st_req_size in self.st_req_sizes:
        #     delays_per_base_iter += st_req_size * delay_scale + self.config["st-init-delay-cycles"]

        # # delays_per_base_iter += self.config["alu-input-delay"]

        # total_cycle_with_delays = total_cycle + self.total_base_loop_iterations * delays_per_base_iter
        
        numTiles = self.total_base_loop_iterations
        
        return perTileCycles, perTileCycles, loadCycles, storeCycles, numTiles, loadTileSizes, storeTileSizes, log_cycles

    # per tile
    def __calculate_load_cycles_json_based(self):
        loadTileSizes = {}
        loadCycles = {}

        if len(self.config['vmemInTileDims']) != 0:
            for k1,v1 in self.config['loadNS'].items():
                _localtileSize = 1
                
                for k,v in self.config['vmemInTileDims'][v1][0].items():
                    _localtileSize *= v

                if _localtileSize == 1:
                    _localtileSize == 0
                
                loadTileSizes[v1] = _localtileSize
            
                loadCycle = ((_localtileSize * 1.0)/self.config["ddrBandwidth"])/5e-9

                loadCycle += self.config["ddrLatency"]
                loadCycles[v1] = loadCycle
                
        return loadCycles, loadTileSizes

    # per tile
    def __calculate_store_cycles_json_based(self):

        _tileSize = 1

        for k,v in self.config['vmemOutTileDims'][self.config['storeNS']][0].items():
            _tileSize *= v 
        
        if _tileSize == 1:
            _tileSize = 0
        
        storeCycles = ((_tileSize * 1.0)/self.config["ddrBandwidth"])/5e-9
        storeCycles += self.config["ddrLatency"]

        return math.ceil(storeCycles), _tileSize

    # per tile
    def __calculate_load_cycles_instruction_based(self):
        loadTileSizes = {}
        loadCycles = {}
        for key in self.ld_req_sizes.keys():
            ld_size = self.ld_req_sizes[key]
            if ld_size > 0:
                loadCycles[key] = (ld_size/self.config["ddrBandwidth"])/(1e-9) + self.config["ddrLatency"] # 1215Mhz memory for A100 
    
        loadTileSizes = self.ld_req_sizes

        # print("load cycle: ", loadCycles)
        # print("load size ", loadTileSizes)    

        return loadCycles, loadTileSizes

    # per tile
    def __calculate_store_cycles_instruction_based(self):
        st_size = np.sum(self.st_req_sizes)
        storeCycle = ((st_size)/self.config["ddrBandwidth"])/(1e-9) + self.config["ddrLatency"] # 1215Mhz memory for A100 
        # print("store size ", st_size)
        return storeCycle, st_size


    def __can_add(self, input_reg: InstructionRegister):
        can_add = False
        if not self.can_add:
            return can_add

        if self.prev_reg != None and self.prev_reg.instruction != input_reg.instruction:
            opcode = self.prev_reg.opcode
            function = self.prev_reg.function

            if opcode == 7:
                if function == 2:
                    can_add = True
            
            elif opcode == 0 or opcode == 1 or opcode == 2 or opcode == 3 and not input_reg.is_nop:
                can_add = True

            # if opcode == 10:
            #     can_add = True
            # grab load star
            # elif opcode == 5:
            #     if (function == 5):
            #         can_add = True
            #     # if (function % 8) == 5:
            #     #     can_add = True
            
            # grab compute opt (always follows SET_INST)
            
            elif opcode == 8:
                    can_add = True

        return can_add
