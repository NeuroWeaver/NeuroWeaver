#from asyncio.windows_events import NULL
#from collections import defaultdict
#from email.policy import default
from fileinput import filename
from systolic_sim.utils import *
import json
import os
import fnmatch
import glob

class decoderGemm():
    """
        Used to parse and decode the compiler output
        *_operation.txt: Get the loops and iteration
        *_string.txt: Get the number of requests and request size per ld/st  
    """
    def __init__(self, configPath, testPath, ddrBandwidth, layerType) -> None:
        #
        self.testPath = testPath
        self.configPath = configPath
        self.freq = 200
        self.infBandwidth = ddrBandwidth
        self.layerType = layerType
        self.infLatency = 15000
        self.arrayN = 8
        self.array = 8
        self.IBUFBankDepth = 1024
        self.OBUFBankDepth = 1024
        self.WBUFBankDepth = 1024
        self.BBUFBankDepth = 1024

        self.DDRDims = {}
        self.layerName = self.layerName()

        self.IBUFTileSize = 0
        self.WBUFTileSize = 0
        self.BBUFTileSize = 0
        self.numComputeTiles = 1
        self.IBUFnumTiles = 1
        self.OBUFnumTiles = 1
        self.WBUFnumTiles = 1
        self.BBUFnumTiles = 1
        
        self.IBUFtileDims = {}
        self.OBUFtileDims = {}
        self.WBUFtileDims = {}
        self.BBUFtileDims = {}
        self.VMEMtileDims = {}
        #self.ibufNumReqs = 0
        #self.obufNumReqs = 0
        #self.wbufNumReqs = 0
        #self.bbufNumReqs = 0
        self.tileDims = {}
        self.dims = {}    
        self.ibufReuse = []
        self.obufReuse = []
        self.wbufReuse = []
        self.bbufReuse = []
        self.totalInputBufSize = 0
        self.gemm4d = False
        self.matmul = False
        self.gemm = False
        self.isGemmlayer = True
        

    def parse_json_file(self) -> None:
        _jsonPath = findFile(self.testPath, '*json.json')
        with open(_jsonPath, 'r') as f:
            _data = json.load(f)
            #print (_data['program'][0]['operation_parameters'])
            if len(_data['program'][0]['iterable_dimensions']) == 5:
                self.gemm4d = True

            elif 'gemm' == _data['program'][0]['operation']:
                self.gemm = True

            elif 'matmul' in _data['program'][0]['operation']:
                self.matmul = True

            self.isGemmlayer = self.gemm4d or self.matmul or self.gemm
            for item in _data['program'][0]['iterable_dimensions']:
                self.DDRDims[item] = _data['program'][0]['iterable_dimensions'][item]
            
            input_key = _data['program'][0]['inputs'][0]['data_path']
            in_key = 'IBUF' in input_key
            if in_key:
                for k,v in _data['program'][0]['inputs'][0]['tiling']['IBUF'].items():
                    self.IBUFtileDims[k] = v
            input_key = _data['program'][0]['inputs'][1]['data_path']
            in_key = 'WBUF' in input_key
            if in_key:
                for k,v in _data['program'][0]['inputs'][1]['tiling']['WBUF'].items():
                    self.WBUFtileDims[k] = v   
            if len(_data['program'][0]['inputs']) > 2:
                input_key = _data['program'][0]['inputs'][2]['data_path']
                in_key = 'BBUF' in input_key
                if in_key:
                    for k,v in _data['program'][0]['inputs'][2]['tiling']['BBUF'].items():
                        self.BBUFtileDims[k] = v
            out_key = _data['program'][0]['outputs'][0]['data_path']
            out_key_1 = 'OBUF' in out_key
            if out_key_1:   
                for k,v in _data['program'][0]['outputs'][0]['tiling']['OBUF'].items():
                    self.OBUFtileDims[k] = v
            else:
                out_key = _data['program'][0]['intermediate'][0]['data_path']
                out_key_1 = 'OBUF' in out_key
                if out_key_1:   
                    for k,v in _data['program'][0]['intermediate'][0]['tiling']['OBUF'].items():
                        self.OBUFtileDims[k] = v
                
    def layerName(self):
        _layerName = self.testPath.split('/')[-1]
        #print (f"Simulating Test: {_layerName}")
        return _layerName
                
    def parse_instruction_file(self) -> None:
       _instrPath = findFile(self.testPath, '*string_final.txt')
       with open(_instrPath, 'r') as f:
            for line in f:
                ## To find number of tiles
                if self.gemm4d == True:
                    if "SA_LOOP_CFG 0" in line:
                        _loop = line.split(',')
                        _loopIter = int(_loop[2].strip('\n')) + 1
                        _loop = int(_loop[1].strip())
                        if _loop < 7:
                            self.tileDims[gemm4dDimMapping[_loop]] = _loopIter
                            self.numComputeTiles = self.numComputeTiles * _loopIter
                        if _loop == 0 or _loop == 1 or _loop == 2 or _loop == 3:
                            self.IBUFnumTiles = self.IBUFnumTiles * _loopIter
                        if _loop == 0 or _loop == 1 or _loop == 2 or _loop == 4:
                            self.OBUFnumTiles = self.OBUFnumTiles * _loopIter
                        if _loop == 0 or _loop == 1 or _loop == 3 or _loop == 4:
                            self.WBUFnumTiles = self.WBUFnumTiles * _loopIter
                        if _loop == 4:
                            self.BBUFnumTiles = self.BBUFnumTiles * _loopIter
                            
                elif self.gemm: # gemmDimMapping = {0: 'M', 1: 'N', 2: 'P' }
                    if "SA_LOOP_CFG 0" in line:
                        _loop = line.split(',')
                        _loopIter = int(_loop[2].strip('\n')) + 1
                        _loop = int(_loop[1].strip())
                        #print("Dims ", gemmDimMapping, _loop)
                        if _loop < 7:
                            #print("Dim ", gemmDimMapping[_loop])
                            self.tileDims[gemmDimMapping[_loop]] = _loopIter
                            self.numComputeTiles = self.numComputeTiles * _loopIter
                        if _loop == 0 or _loop == 1 or _loop == 2:
                            self.IBUFnumTiles = self.IBUFnumTiles * _loopIter
                        if _loop == 0 or _loop == 2 or _loop == 3:
                            self.OBUFnumTiles = self.OBUFnumTiles * _loopIter
                        if _loop == 2 or _loop == 3:
                            self.WBUFnumTiles = self.WBUFnumTiles * _loopIter
                        if _loop == 3:
                            self.BBUFnumTiles = self.BBUFnumTiles * _loopIter
                        
                        self.tileDims['B'] = 1
                        self.tileDims['C'] = 1
                                
                elif self.matmul: # matmulMapping = {0: 'B', 1: 'M', 2: 'N', 3: 'P' }
                    if "SA_LOOP_CFG 0" in line:
                        _loop = line.split(',')
                        _loopIter = int(_loop[2].strip('\n')) + 1
                        _loop = int(_loop[1].strip())
                        if _loop < 7:
                            self.tileDims[matmulMapping[_loop]] = _loopIter
                            self.numComputeTiles = self.numComputeTiles * _loopIter
                        if _loop == 0 or _loop == 1 or _loop == 2:
                            self.IBUFnumTiles = self.IBUFnumTiles * _loopIter
                        if _loop == 0 or _loop == 2 or _loop == 3:
                            self.OBUFnumTiles = self.OBUFnumTiles * _loopIter
                        if _loop == 2 or _loop == 3:
                            self.WBUFnumTiles = self.WBUFnumTiles * _loopIter
                        if _loop == 3:
                            self.BBUFnumTiles = self.BBUFnumTiles * _loopIter
                        
                        self.tileDims['C'] = 1

                else: # dimMapping = { 0: 'OC', 1: 'N', 2: 'IC', 3: 'KH', 4: 'KW', 5: 'OH', 6: 'OW' }
                    if "SA_LOOP_CFG 0" in line: 
                        _loop = line.split(',')
                        _loopIter = int(_loop[2].strip('\n')) + 1
                        _loop = int(_loop[1].strip())
                        if _loop < 7:
                            self.tileDims[matmulMapping[_loop]] = _loopIter
                            self.numComputeTiles = self.numComputeTiles * _loopIter
                        if _loop == 0 or _loop == 1 or _loop == 2:
                            self.IBUFnumTiles = self.IBUFnumTiles * _loopIter
                        if _loop == 0 or _loop == 2 or _loop == 3:
                            self.OBUFnumTiles = self.OBUFnumTiles * _loopIter
                        if _loop == 2 or _loop == 3:
                            self.WBUFnumTiles = self.WBUFnumTiles * _loopIter
                        if _loop == 3:
                            self.BBUFnumTiles = self.BBUFnumTiles * _loopIter  
                       
    def parse_arch_cfg(self):
        #_archCfgPath = findFile(self.testPath, '*arch_cfg.json')
        _archCfgPath = findFile(self.testPath, '../*arch_cfg.json')
        with open(_archCfgPath, 'r') as f:
            _data = json.load(f)
            self.IBUFbitwidth = _data['DATA_WIDTH']
            self.OBUFbitwidth = _data['ACC_WIDTH']
            self.WBUFbitwidth = _data['WGT_WIDTH']
            self.BBUFbitwidth = _data['BIAS_WIDTH']
            self.IBUFBankDepth = _data['IBUF_DEPTH']
            self.OBUFBankDepth = _data['OBUF_DEPTH'] * 2
            self.WBUFBankDepth = _data['WBUF_DEPTH']
            self.BBUFBankDepth = _data['BBUF_DEPTH']
            self.IBUFinfwidth = self.infBandwidth
            self.OBUFinfwidth = self.infBandwidth
            self.WBUFinfwidth = self.infBandwidth
            self.BBUFinfwidth = self.infBandwidth
            self.arrayN = _data['ARRAY_N']
            self.arrayM = _data['ARRAY_M']
            self.IBUFNumBanks = self.arrayN
            self.OBUFNumBanks = self.arrayM
            self.WBUFNumBanks = self.arrayM * self.arrayM
            self.BBUFNumBanks = self.arrayM
        
        _configPath = self.configPath
        _archCfgPath = findFile(_configPath, 'systolic_config.json')
        with open(_archCfgPath, 'r') as f:
            _data = json.load(f)
            self.infLatency = _data["infLatency"]
            self.freq = _data['frequency']
            self.IBUFinfBandwidth = self.infBandwidth
            self.IBUFperAccessReadEnergy = _data["IBUFperAccessReadEnergy"]
            self.IBUFperAccessWriteEnergy = _data["IBUFperAccessWriteEnergy"]
            self.OBUFinfBandwidth = self.infBandwidth
            self.OBUFperAccessReadEnergy = _data["OBUFperAccessReadEnergy"]
            self.OBUFperAccessWriteEnergy = _data["OBUFperAccessWriteEnergy"]
            self.WBUFinfBandwidth = self.infBandwidth
            self.WBUFperAccessReadEnergy = _data["WBUFperAccessReadEnergy"]
            self.WBUFperAccessWriteEnergy = _data["WBUFperAccessWriteEnergy"]
            self.BBUFinfBandwidth = self.infBandwidth
            self.BBUFperAccessReadEnergy = _data["BBUFperAccessReadEnergy"]
            self.BBUFperAccessWriteEnergy = _data["BBUFperAccessWriteEnergy"]
            self.numTags = _data["numTags"]
            self.decoderCycles = _data["decoderCycles"]
            self.energyPerMAC = _data["energyPerMAC"]

    def getTileReusePerBuffer(self):
        _B = self.tileDims['B']
        _C = self.tileDims['C'] if self.gemm4d is True else 1
        _M = self.tileDims['M']
        _N = self.tileDims['N']
        _P = self.tileDims['P']
        _oldB = -1
        _oldC = -1
        _oldM = -1
        _oldN = -1
        _oldP = -1
        #print (self.tileDims['C'])
        for b in range(_B):
            for c in range(_C):
                for m in range(_M):
                    for n in range(_N):
                        for p in range(_P):
                            #_arr1DIndex = get1DIndex(b, c, m, p, _C, _M, _P)
                            _arr1DIndex = get5Dto1DIndex(p, n, m, c, b, _N, _M, _C, _B)
                            #print (f'array idx {_arr1DIndex}')
                            if _oldB != b:   
                                self.ibufReuse[_arr1DIndex] = 0
                                self.wbufReuse[_arr1DIndex] = 0
                                self.obufReuse[_arr1DIndex] = 0
                            if _oldC != c:
                                self.ibufReuse[_arr1DIndex] = 0
                                self.wbufReuse[_arr1DIndex] = 0
                                self.obufReuse[_arr1DIndex] = 0
                            if _oldM != m:
                                self.ibufReuse[_arr1DIndex] = 0
                                self.obufReuse[_arr1DIndex] = 0
                            if _oldN != n:
                                self.ibufReuse[_arr1DIndex] = 0
                                self.wbufReuse[_arr1DIndex] = 0
                            if _oldP != p:
                                self.wbufReuse[_arr1DIndex] = 0
                                self.bbufReuse[_arr1DIndex] = 0
                                self.obufReuse[_arr1DIndex] = 0
                            #print (f"HERE new val = {oc}, {n}, {ic}, {kh}, {kw}, {oh}, {ow}")
                            #print (f"HERE old val ={_oldOC}, {_oldN}, {_oldIC}, {_oldKH}, {_oldKW}, {_oldOH}, {_oldOW}\n")
                            _oldB = b
                            _oldC = c
                            _oldM = m
                            _oldN = n
                            _oldP = p
                            
        #print ("\n ibuf reuse Here 10:", self.ibufReuse)
        #print ("\n obuf reuse Here 10:", self.obufReuse)
        #print ("\n wbuf reuse Here 10:", self.wbufReuse)
        #print ("\n bbuf reuse Here 10:", self.bbufReuse)


    def updateVariable(self):
        self.ibufReuse = [1 for i in range(self.numComputeTiles + 1)]  ## +1 to account for the last tile in the compute cycle, else out of bound error
        self.obufReuse = [1 for i in range(self.numComputeTiles + 1)]  ## +1 to account for the last tile in the compute cycle, else out of bound error
        self.wbufReuse = [1 for i in range(self.numComputeTiles + 1)]  ## +1 to account for the last tile in the compute cycle, else out of bound error
        self.bbufReuse = [1 for i in range(self.numComputeTiles + 1)]  ## +1 to account for the last tile in the compute cycle, else out of bound error
        

    def computeTileSize(self, _tileDims):
        _tsize = 1
        for k,v in _tileDims.items():
            _tsize *= v
        _tsize *= self.IBUFbitwidth
        return _tsize//8 # in bytes

    def totalInputOnChipBuffer(self):
        self.IBUFTileSize = self.computeTileSize(self.IBUFtileDims)
        self.WBUFTileSize = self.computeTileSize(self.WBUFtileDims)
        self.BBUFTileSize = self.computeTileSize(self.BBUFtileDims)
        #print (f"{self.IBUFTileSize}, {self.WBUFTileSize}, {self.BBUFTileSize}")
        return self.IBUFTileSize + self.WBUFTileSize + self.BBUFTileSize
    

    def cycle(self) -> int:
        self.parse_json_file()
        self.parse_instruction_file()
        self.parse_arch_cfg()
        self.updateVariable()
        self.getTileReusePerBuffer()
        self.totalInputOnChipBuffer()

        return self.decoderCycles
