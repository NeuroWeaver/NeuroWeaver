import re
import json
import os
import copy
from systolic_sim.utils import *


class ConfigParser:
    def __init__(self,  testPath, testName, ddrBandwidth, sim_config_path, layerType = 'simd'):
        self.sim_config_path = sim_config_path
        self.ddrBandwidth = ddrBandwidth
        self.testPath = testPath 
        self.testName = testName
        self.layerType = layerType

    def parse(self):
        config = {}
        with open(self.sim_config_path, "r") as f:
            json_data = json.load(f)
            config["should-validate-dram-output"] = False if json_data["fast-run"] else True
            config["layer-example-path"] = json_data["layer-example-path"]
            config["layer-example-name"] = os.path.basename(json_data["layer-example-path"])
            config["fast-run"] = json_data["fast-run"]
            config["ld-init-delay-cycles"] = json_data["ld-init-delay-cycles"]
            config["ld-scale-of-delay"] = json_data["ld-scale-of-delay"]
            config["st-init-delay-cycles"] = json_data["st-init-delay-cycles"]
            config["st-scale-of-delay"] = json_data["st-scale-of-delay"]
            num_load_inputs = json_data["num-input-to-load-from-ddr"]
            num_store_outputs = json_data["num-output-to-store-to-ddr"]
            config["ddrBandwidth"] = self.ddrBandwidth
            config["ddrLatency"] =  json_data["ddrLatency"]
            #print(config["layer-example-name"])
            # config["alu-input-delay"] = json_data["alu-input-delay"]

        layer_example_path = self.testPath
        layer_example_name = self.testName
        #with open(f"{layer_example_path}/{layer_example_name}_arch_cfg.json", "r") as f:
        _archCfgPath = findFile(layer_example_path, '../*arch_cfg.json')
        with open(_archCfgPath, "r") as f:
            json_data = json.load(f)

            config["simd-lane-cnt"] = json_data["SIMD_WIDTH"]
            config["ld-st-bandwidth-per-cycle"] = json_data["SIMD_CHANNEL_BW"] // 8
            config["ld-st-booting-time-cycle"] = 0 # TODO: should be configured later
            config["vmem-depth"] = json_data["VMEM_DEPTH"]

            config["dram-depth"] = json_data["DRAM_DEPTH"]
            config["dram-width"] = json_data["DRAM_WIDTH"]
            config["dram-banks"] = json_data["DRAM_BANKS"]

            #todo: add Buffer depths and caclcuate utilization later
        if 'fused' in  self.layerType:
            extn = '*_binary_SIMD.txt'
        else:
            extn = '*_binary.txt'
        
        #with open(f"{layer_example_path}/{layer_example_name}{extn}", "r") as f:
        _filePath = findFile(layer_example_path,extn)
        with open(_filePath, "r") as f:
            curr_opcode = 10
            cnt_state_change = 0
            for line in f.readlines():
                line = line.rstrip()
                opcode = int(line[0:4], 2)
                if opcode != curr_opcode:
                    curr_opcode = opcode
                    cnt_state_change += 1
            # print(f"cnt_state_change: {cnt_state_change}")
            config["state-change-cnt"] = cnt_state_change

        if 'fused' in  self.layerType:
            extn = '*_string_final_SIMD.txt'
        else:
            extn = '*_string_final.txt'

        _filePath = findFile(layer_example_path, extn)
     
        #ld_base, st_base, storeNS, loadNS = self.__parse_ld_st_base(f"{layer_example_path}/{layer_example_name}{extn}")
        ld_base, st_base, storeNS, loadNS = self.__parse_ld_st_base(_filePath)

        if len(st_base) > 1:
            raise ValueError("# of output should be one")

        config["dram-init-config"] = [{"file-path": f"{layer_example_path}/input{i+1}_raw.txt" if num_load_inputs > 1 else f"{layer_example_path}/input1_raw.txt",
                                       "base-offset": ld_base[i]} for i in range(num_load_inputs)]
        #print("dram-init-config", config["dram-init-config"])

        config["dram-output-config"] = {"file-path": f"{layer_example_path}/output.txt",
                                         "base-offset": st_base[0]}

        if 'fused' in  self.layerType:
            extn = '*_decimal_SIMD.txt'
        else:
            extn = '*_decimal.txt'
        _filePath = findFile(layer_example_path, extn)
        #config["instructions_path"] = f"{layer_example_path}/{layer_example_name}{extn}"
        config["instructions_path"] = _filePath

        #print("dram-init-config", config["dram-init-config"])
        #print("dram-output-config", config["dram-output-config"])
        #exit()
        vmemTileDims = {}
        vmemTileDimsop = {}

        _filePath = findFile(layer_example_path, "*_json.json")
        #with open(f"{layer_example_path}/{layer_example_name}_json.json", "r") as f:
        with open(_filePath, "r") as f:
            json_data = json.load(f)
            for i in range(len(json_data['program'][0]['inputs'])):
                #nspace = 'VMEM1' if json_data['program'][0]['inputs'][i]['tiling'].__contains__('VMEM1') else 'VMEM2'
                nspace = list(json_data['program'][0]['inputs'][i]['tiling'])[1]
                if 'VMEM1' in nspace or 'VMEM2' in nspace:
                    vmemTileDims[nspace] = [{},{}]
                    for k,v in json_data['program'][0]['inputs'][i]['tiling'][nspace].items():
                        vmemTileDims[nspace][0][k] = v
                    vmemTileDims[nspace][1]['dtype'] = json_data['program'][0]['inputs'][i]['dtype']

            for i in range(len(json_data['program'][0]['outputs'])):
                nspace = 'VMEM1' if json_data['program'][0]['outputs'][i]['tiling'].__contains__('VMEM1') else 'VMEM2'
                vmemTileDimsop[nspace] = [{},{}]
                for k,v in json_data['program'][0]['outputs'][i]['tiling'][nspace].items():
                    vmemTileDimsop[nspace][0][k] = v
                vmemTileDimsop[nspace][1]['dtype'] = json_data['program'][0]['outputs'][i]['dtype']

        
        
        config['vmemInTileDims'] = copy.deepcopy(vmemTileDims)
        config['vmemOutTileDims'] = copy.deepcopy(vmemTileDimsop)
        config['storeNS'] = storeNS
        config['loadNS'] = loadNS

        return config

    def __parse_ld_st_base(self, string_instruction_path):
        bases = {
            "load": {
                "VMEM1": [],
                "VMEM2": []
            },
            "store": {
                "VMEM1": [],
                "VMEM2": []
            }
        }

        result = {
            "input": [],
            "output": []
        }

        loadNS = {}

        with open(string_instruction_path, "r") as f:
            for line in f.readlines():
                line = line.rstrip().lstrip()
                elements = re.split(", | ", line)
                # print(elements)

                if "_CONFIG_BASE_ADDR" in elements[0]:
                    is_msb = True if elements[1] == "MSB" else False
                    is_store = True if "ST_" in elements[0] else False
                    ns = elements[2]
                    if is_store is False:
                        loadNS[ns] = ns 
                    #print ('ns = ', ns, 'is_store = ', is_store)
                    loop_idx = int(elements[3])
                    if loop_idx != 0:
                        raise ValueError(f"{elements[0]} has larger loop index more than 0 as {loop_idx}")
                    imm = int(elements[4])
                    imm = (imm << 16) if is_msb else imm

                    if len(bases["store" if is_store else "load"][ns]) == 0:
                        bases["store" if is_store else "load"][ns].append(imm)
                    else:
                        bases["store" if is_store else "load"][ns][0] += imm

        ld_bases = bases["load"]
        ld_result = result["input"]
        st_bases = bases["store"]
        st_result = result["output"]

        for key in ["VMEM1", "VMEM2"]:
            for val in ld_bases[key]:
                ld_result.append(val // 4)
            for val in st_bases[key]:
                st_result.append(val // 4)
        # to find which VMEM is used for store
        storeNS = ns if is_store is True else ''
        #loadNS = ns if is_store is False else ''
        #print ('loadNS  = ', loadNS, 'is_store = ', is_store)
        
        return ld_result, st_result, storeNS, loadNS


'''
config = {
        "simd-lane-cnt": 64, #64,
        "ld-st-bandwidth-per-cycle": 64, # TODO (Yoonsung): it's bytes. should be bits
        "ld-st-wr-bandwidth-per-cycle": 128,
        "ld-st-booting-time-cycle": 0,
        "vmem-depth": 2048,

        "dram-depth": 100000,
        "dram-width": 8,
        "dram-banks": 64,
        "dram-init-config": [
            {"file-path": "input.txt", "base-offset": (580) // 4, "shape": [1, 113, 113, 128]},
        ],
        "dram-output-config": {
            "file-path": "output.txt",
            "base-offset": ((101 << 16) + 35396) // 4, #((99 << 16) + 49664) // 4,
            "shape": [1, 56, 56, 128]
        },
        "should-validate-dram-output": True,
    }
'''

if __name__ == "__main__":
    cfg_parser = ConfigParser(sim_config_path="sim_config.json")

    parsed_data = cfg_parser.parse()

    #print(parsed_data)
