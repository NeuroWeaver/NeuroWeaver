import copy
import time
import numpy as np
from simd_sim.simulator.instruction_fetch import InstructionFetch
from simd_sim.simulator.decode import Decode
from simd_sim.simulator.address_generation import AddressGeneration
from simd_sim.simulator.alu import ALU
from tqdm import tqdm
from simd_sim.simulator.config_parser import ConfigParser
from simd_sim.simulator.single_base_loop_profiler import SingleBaseLoopProfiler


def int_to_bin_str(inst):
    """
    :param inst:
    A decimal number
    :return:
    A converted binary string
    """
    return f"{inst:032b}"


class Pipeline:
    def __init__(self, config):
        self.config = config
        self.simd_lane_cnt = config["simd-lane-cnt"]
        self.global_cycle = 0

        # for on chip memory
        self.banked_memory = self.__init_on_chip_memory()

        # for off chip memory
        self.ddr_memory = self.__init_ddr_memory(config,
                                                 input_config=config["dram-init-config"])
        
        # shared transpose dest buffer address
        self.dest_bank_write_address = [0] * self.simd_lane_cnt
        
        # stages
        self.stages = []

        self.instruction_fetch = InstructionFetch(self.simd_lane_cnt)
        self.stages.append(self.instruction_fetch)

        decode = Decode(self.simd_lane_cnt,
                        ld_st_bandwidth_per_cycle=config["ld-st-bandwidth-per-cycle"],
                        ld_st_booting_time_cycle=config["ld-st-booting-time-cycle"],
                        banked_memory=self.banked_memory,
                        ddr_memory=self.ddr_memory)
        # delegators
        decode.instruction_fetch = self.instruction_fetch
        decode.pipeline = self
        self.stages.append(decode)

        self.instruction_fetch.decode = decode

        self.address_generation = AddressGeneration(self.simd_lane_cnt, self.banked_memory, self.dest_bank_write_address)
        self.stages.append(self.address_generation)

        self.instruction_fetch.address_generation = self.address_generation

        for idx in range(self.simd_lane_cnt):
            self.stages.append(ALU(self.simd_lane_cnt,
                                   execution_idx=idx,
                                   banked_memory=self.banked_memory,
                                   dest_bank_write_address = self.dest_bank_write_address,
                                   pipeline=self if idx == self.simd_lane_cnt-1 else None))

        self.stage_cnt = len(self.stages)

        self.profiler = SingleBaseLoopProfiler(config=self.config)
        self.profiler.stage_cnt = self.stage_cnt

    def run(self, inst_file_path):
        """
        Read instructions from a file path, and execute a pipeline cycle by cycle.
        :param inst_file_path:
        A .txt file path including decimal instructions line by line
        :return:
        A summary dictionary consisting of simulated statistics
        """
        inst_list = []

        with open(inst_file_path, 'r') as file:
            for line in file:
                inst_int = int(line.strip())
                inst_bin_str = int_to_bin_str(inst_int)
                inst_list.append(inst_bin_str)

        if len(inst_list) != 0:
            self.stages[0].inst_list = inst_list
            self.stages[0].pc_end = len(inst_list)

            inst = self.stages[0].inst_list[self.stages[0].pc]
            self.stages[0].feed_inst(inst)
            self.__cycle()

            while self.__is_finished() is False:
                self.__cycle()

        if self.config["should-validate-dram-output"]:
            self.__validate_output(self.config["dram-output-config"])

        return self.__summary()

    def start_alu_loop(self, instruction_cnt, iteration_cnt, is_nested):
        # instruction fetch
        self.instruction_fetch.start_loop(instruction_cnt=instruction_cnt,
                                          left_iteration_cnt=iteration_cnt-1,
                                          is_nested=is_nested)

        # address generation
        self.address_generation.set_total_iteration_cnt(instruction_cnt * iteration_cnt)

    def try_to_set_base_loop(self, left_iteration_cnt):
        if self.config["fast-run"]:
            left_iteration_cnt = 0
        self.instruction_fetch.set_base_loop(left_iteration_cnt)

    def __cycle(self):
        self.global_cycle += 1

        for stage in self.stages:
            stage.cycle()

        self.__handle_stall()

    def __is_finished(self):
        for stage in self.stages:
            if not stage._is_finish():
                return False
            # if stage.input_inst_reg is not None:
            #     return False

        # when the excution is finished, give profiler the ld/st table
        # self.profiler.ld_sizes = self.stages[1].ld_sizes # stage 1 is decode
        # self.profiler.st_sizes = self.stages[1].st_sizes # stage 1 is decode

        return True

    def __init_on_chip_memory(self):
        elem_cnt_per_simd_lane = self.config["vmem-depth"]

        memory = []
        for lane in range(self.simd_lane_cnt):
            memory.append([float(-1.) for _ in range(elem_cnt_per_simd_lane)])
        memory = np.array(memory)

        # Rohan: Why 32? Assuming instruction depth is always 32?
        imm_memory = np.array([-1 for _ in range(32)])

        return {"obuf": copy.deepcopy(memory),
                "ibuf": copy.deepcopy(memory),
                "vmem1": copy.deepcopy(memory),
                "vmem2": copy.deepcopy(memory),
                "imm": copy.deepcopy(imm_memory)}

    def __init_ddr_memory(self, config, input_config):
        width = config["dram-width"]
        depth = config["dram-depth"]
        banks = config["dram-banks"]

        if width % 8 != 0:
            raise ValueError(f"invalid dram width({width} bits)")


	# todo: Rohan added as memory was using all the DRAM in the system and failing simulation
        length = (width // 8) * banks
        #length = (width // 8) * depth * banks

        #memory = [float("-inf")] * length
        ## Rohan commented, who initializes something with -inf
        memory = [float(1)] * length

        #print("load input data into DDR memory...")
        '''
        # Rohan removed this as it was talking a lot of time
        for config in input_config:
            idx = config["base-offset"]
            with open(config["file-path"], "r") as f:
                #for line in tqdm(f.readlines()):
                for line in f.readlines():
                    memory[idx] = float(line.rstrip())
                    idx += 1
        '''

        return memory

    def __validate_output(self, output_config):
        print("validating output... ", end="")

        output = []
        with open(output_config["file-path"], "r") as f:
            for line in f.readlines():
                output.append(float(line.rstrip()))

        out_length = len(output)

        base = output_config["base-offset"]
        output_from_ddr = self.ddr_memory[base:base+out_length]

        for i in tqdm(range(out_length)):
            if np.abs(output_from_ddr[i] - output[i]) > 0.01:
                print(f"failed {i}th, output: {output_from_ddr[i]}, answer: {output[i]}")
                return

        print("passed")

    def __summary(self):
        stats = self.profiler.profile() if self.config["fast-run"] else self.global_cycle
        #print(stats)
        ddrLoadCycles = stats[2]
        ddrLoadCycleVmem1 = ddrLoadCycles["vmem1"] if "vmem1" in ddrLoadCycles.keys() else 0
        ddrLoadCycleVmem2 = ddrLoadCycles["vmem2"] if "vmem2" in ddrLoadCycles.keys() else 0

        ddrLoadTileSizes = stats[5]
        ddrLoadTileSizeVmem1 = ddrLoadTileSizes["vmem1"] if "vmem1" in ddrLoadTileSizes.keys() else 0
        ddrLoadTileSizeVmem2 = ddrLoadTileSizes["vmem2"] if "vmem2" in ddrLoadTileSizes.keys() else 0

        summary = {
            "cycle": stats[0] ,
            "perTileCycles": stats[1] ,
            "ddrLoadCycleVmem1": ddrLoadCycleVmem1,
            "ddrLoadCycleVmem2": ddrLoadCycleVmem2,
            "StoreCycles": stats[3] ,
            "numTiles": stats[4] ,
            "ddrLoadTileSizeVmem1": ddrLoadTileSizeVmem1,
            "ddrLoadTileSizeVmem2": ddrLoadTileSizeVmem2,
            "storeTileSize": stats[6],
            "memory-access": {
                "obuf": {
                    i: {"read": 0} for i in range(self.simd_lane_cnt)
                    
                },
                "ibuf": {
                    i: {"write": 0} for i in range(self.simd_lane_cnt) 
                },
                # "vmem1": {
                #     i: {"read": 0, "write": 0} for i in range(self.simd_lane_cnt)
                # },
                # "vmem2": {
                #     i: {"read": 0, "write": 0} for i in range(self.simd_lane_cnt)
                # },
                "imm": {
                    0: {"read": 0, "write": 0},
                },
                "total": {
                    "obuf": 0,
                    "ibuf": 0,
                    "vmem1_computeRead": 0,
                    "vmem1_computeWrite": 0,
                    "vmem1_ldWrite": 0,
                    "vmem1_stRead": 0,
                    "vmem2_computeRead": 0,
                    "vmem2_computeWrite": 0,
                    "vmem2_ldWrite": 0,
                    "vmem2_stRead": 0,                    
                    "imm_read": 0,
                    "imm_write": 0
                }
            },
            "perTileSoftmax": stats[7]
            
        }

        mem_acc = summary["memory-access"]

        for stage in self.stages:
            stage_mem_acc = stage.statistics["memory-access"]
            for i in range(self.simd_lane_cnt):
                mem_acc["obuf"][i]["read"] += stage_mem_acc["obuf"][i]["read"]
                mem_acc["total"]["obuf"] += stage_mem_acc["obuf"][i]["read"]
                mem_acc["ibuf"][i]["write"] += stage_mem_acc["ibuf"][i]["write"]
                mem_acc["total"]["ibuf"] += stage_mem_acc["ibuf"][i]["write"]

                mem_acc["total"]["vmem1_computeRead"] += stage_mem_acc["vmem1"][i]["computeRead"]
                mem_acc["total"]["vmem1_computeWrite"] += stage_mem_acc["vmem1"][i]["computeWrite"]
                mem_acc["total"]["vmem1_ldWrite"] += stage_mem_acc["vmem1"][i]["ldWrite"]
                mem_acc["total"]["vmem1_stRead"] += stage_mem_acc["vmem1"][i]["stRead"]
                
                mem_acc["total"]["vmem2_computeRead"] += stage_mem_acc["vmem2"][i]["computeRead"]
                mem_acc["total"]["vmem2_computeWrite"] += stage_mem_acc["vmem2"][i]["computeWrite"]
                mem_acc["total"]["vmem2_ldWrite"] += stage_mem_acc["vmem2"][i]["ldWrite"]
                mem_acc["total"]["vmem2_stRead"] += stage_mem_acc["vmem2"][i]["stRead"]

            mem_acc["imm"][0]["read"] += stage_mem_acc["imm"][0]["read"]
            mem_acc["total"]["imm_read"] += stage_mem_acc["imm"][0]["read"]
            mem_acc["total"]["imm_write"] += stage_mem_acc["imm"][0]["read"]
        
        #print(mem_acc["total"]["vmem1_computeWrite"])
        return summary, mem_acc['total']

    def __handle_stall(self):
        is_stalled = False

        for i in range(self.stage_cnt - 1, -1, -1):
            ir = self.stages[i].input_inst_reg
            if ir is not None and ir.is_nop():
                is_stalled = False

            if is_stalled:
                continue

            is_stalled = self.stages[i].pull_inst_reg(prev_stage=None if i == 0 else self.stages[i - 1])

    def add_to_profiler(self, inst_reg):
        self.profiler.add(inst_reg, ended_cycle=self.global_cycle)


if __name__ == "__main__":
    config = ConfigParser(sim_config_path="sim_config.json").parse()

    pipeline = Pipeline(config)

    start = time.time()
    summary = pipeline.run(inst_file_path=config["instructions_path"])
    end = time.time()
    #print(f"elapsed time: {(end - start) / 1000_000_000:.3f} seconds")

    #print(f"summary...")
    #print(f"fast-run: {config['fast-run']}")
    print(f"cycles: {summary['cycle']}")
    print(f"Per Tile Cycles: {summary['perTileCycles']}")
    print(f"Store Cycles: {summary['StoreCycles']}")
    print(f"Num Tiles: {summary['numTiles']}")
    '''
    mem_acc = summary["memory-access"]
    print(f"memory access")
    for i in range(1):
        print(f"lane {i}")
        print(f"obuf read: {mem_acc['obuf'][i]['read']}")
        print(f"ibuf write: {mem_acc['ibuf'][i]['write']}")
        print(f"vmem1 (read, write): ({mem_acc['vmem1'][i]['read']}, {mem_acc['vmem1'][i]['write']})")
        print(f"vmem2 (read, write): ({mem_acc['vmem2'][i]['read']}, {mem_acc['vmem2'][i]['write']})")
    print(f"imm read: {mem_acc['imm'][0]['read']}")
    '''

    
