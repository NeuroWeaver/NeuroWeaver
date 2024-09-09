#from asyncio.windows_events import NULL
#from collections import defaultdict
#from email.policy import default
from fileinput import filename
from systolic_sim.utils import *
import json
import os
import fnmatch
import glob

class decoder():
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
        self.isGemmlayer = False
        

    def parse_json_file(self) -> None:
        _jsonPath = findFile(self.testPath, '*json.json')
        with open(_jsonPath, 'r') as f:
            _data = json.load(f)
            for item in _data['program'][0]['iterable_dimensions']:
                self.DDRDims[item] = _data['program'][0]['iterable_dimensions'][item]
            
            self.strd = _data['program'][0]['operation_parameters']['stride']
            self.pad = _data['program'][0]['operation_parameters']['pad']
            
            for k,v in _data['program'][0]['inputs'][0]['tiling']['IBUF'].items():
                self.IBUFtileDims[k] = v
            for k,v in _data['program'][0]['inputs'][1]['tiling']['WBUF'].items():
                self.WBUFtileDims[k] = v    
            for k,v in _data['program'][0]['inputs'][2]['tiling']['BBUF'].items():
                self.BBUFtileDims[k] = v        
            out_key = (_data['program'][0]['outputs'][0]['tiling'])  
            
            #print (self.layerType, type(out_key))
            
            if self.layerType == 'systolic':
            
                if type(out_key) == dict: 
                    out_key_1 = 'OBUF' in (_data['program'][0]['outputs'][0]['tiling'])   
                    out_key_2 = 'VMEM1' in (_data['program'][0]['outputs'][0]['tiling'])   
                    out_key_3 = 'DDR' in (_data['program'][0]['outputs'][0]['tiling'])   
                    #print (out_key_1,out_key_2,out_key_3)
                    if out_key_1:    
                        for k,v in _data['program'][0]['outputs'][0]['tiling']['OBUF'].items():
                            self.OBUFtileDims[k] = v
                    elif out_key_2:    
                        for k,v in _data['program'][0]['outputs'][0]['tiling']['VMEM1'].items():
                            self.VMEMtileDims[k] = v
                    elif out_key_3:    
                        for k,v in _data['program'][0]['outputs'][0]['tiling']['VMEM2'].items():
                            self.VMEMtileDims[k] = v
                    else:
                        for k,v in _data['program'][0]['outputs'][0]['tiling']['DDR'].items():
                            self.VMEMtileDims = {}    
                else:
                    out_key = next(iter(_data['program'][0]['outputs'][0]['tiling']))  
                    if 'OBUF' in out_key:    
                        for k,v in _data['program'][0]['outputs'][0]['tiling'][out_key].items():
                            self.OBUFtileDims[k] = v
                    else:
                        for k,v in _data['program'][0]['outputs'][0]['tiling'][out_key].items():
                            self.VMEMtileDims[k] = v
            else:
                for _i in range(len(_data['program'][0]['intermediate'])):
                    _val = _data['program'][0]['intermediate'][_i]
                    if 'conv_out' == _val['name']:
                        #print ('data == ',_val)
                        for k,v in _val['tiling']['OBUF'].items():
                            self.OBUFtileDims[k] = v
        #print ("ITile Dims = ", self.IBUFtileDims)
        #print ("WTile Dims = ", self.WBUFtileDims)
        #print ("BTile Dims = ", self.BBUFtileDims)
        #print ("OTile Dims = ", self.OBUFtileDims)
        #print ("VTile Dims = ", self.VMEMtileDims)
            
    def layerName(self):
        _layerName = self.testPath.split('/')[-1]
        #print (f"Simulating Test: {_layerName}")
        return _layerName
                
    def parse_instruction_file(self) -> None:
        _instrPath = findFile(self.testPath, '*string_final.txt')
        with open(_instrPath, 'r') as f:
            for line in f:
                if "SA_LOOP_CFG 0" in line:
                    _loop = line.split(',')
                    _loopIter = int(_loop[2].strip('\n')) + 1
                    _loop = int(_loop[1].strip())
                    if _loop < 7:
                        #print ("SA_LOOP_CFG 0 ", _loop, _loopIter)
                        self.tileDims[dimMapping[_loop]] = _loopIter
                        self.numComputeTiles = self.numComputeTiles * _loopIter
                    if _loop == 2 or _loop == 5 or _loop == 6:
                        self.IBUFnumTiles = self.IBUFnumTiles * _loopIter
                    if _loop == 0 or _loop == 5 or _loop == 6:
                        self.OBUFnumTiles = self.OBUFnumTiles * _loopIter
                    if _loop == 0 or _loop == 2:
                        self.WBUFnumTiles = self.WBUFnumTiles * _loopIter
                    if _loop == 0:
                        self.BBUFnumTiles = self.BBUFnumTiles * _loopIter
        
        #print (self.numComputeTiles)
                    
        
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
            self.IBUFinfBandwidth = _data["IBUFinfBandwidth"] 
            self.IBUFperAccessReadEnergy = _data["IBUFperAccessReadEnergy"]
            self.IBUFperAccessWriteEnergy = _data["IBUFperAccessWriteEnergy"]
            self.OBUFinfBandwidth = _data["OBUFinfBandwidth"]
            self.OBUFperAccessReadEnergy = _data["OBUFperAccessReadEnergy"]
            self.OBUFperAccessWriteEnergy = _data["OBUFperAccessWriteEnergy"]
            self.WBUFinfBandwidth = _data["WBUFinfBandwidth"]
            self.WBUFperAccessReadEnergy = _data["WBUFperAccessReadEnergy"]
            self.WBUFperAccessWriteEnergy = _data["WBUFperAccessWriteEnergy"]
            self.BBUFinfBandwidth = _data["BBUFinfBandwidth"]
            self.BBUFperAccessReadEnergy = _data["BBUFperAccessReadEnergy"]
            self.BBUFperAccessWriteEnergy = _data["BBUFperAccessWriteEnergy"]
            self.numTags = _data["numTags"]
            self.decoderCycles = _data["decoderCycles"]
            self.energyPerMAC = _data["energyPerMAC"]

    def getTileReusePerBuffer(self):
        _N = self.tileDims['N']
        _OC = self.tileDims['OC']
        _IC = self.tileDims['IC']
        _KH = self.tileDims['KH']
        _KW = self.tileDims['KW']
        _OH = self.tileDims['OH']
        _OW = self.tileDims['OW']
        _oldN = -1
        _oldOC = -1
        _oldIC = -1
        _oldKH = -1
        _oldKW = -1
        _oldOH = -1
        _oldOW = -1
        #print (f"HERE {_OC}, {_N}, {_IC}, {_KH}, {_KW}, {_OH}, {_OW}")
        
        for oc in range(_OC):
            for n in range(_N):
                for ic in range(_IC):
                    for kh in range(_KH):
                        for kw in range(_KW):
                            for oh in range(_OH):
                                for ow in range(_OW):
                                    ## We need an iterator to index array with elements = total number of tiles 
                                    _arr1DIndex = get1DIndex(oc, ic, oh, ow, _IC, _OH, _OW)
                                    #print (f'array idx {_arr1DIndex}')
                                    if _oldN != n:   
                                        self.obufReuse[_arr1DIndex] = 0
                                        self.ibufReuse[_arr1DIndex] = 0
                                    if _oldOC != oc:
                                        self.obufReuse[_arr1DIndex] = 0
                                        self.wbufReuse[_arr1DIndex] = 0
                                        self.bbufReuse[_arr1DIndex] = 0
                                    if _oldIC != ic:
                                        self.ibufReuse[_arr1DIndex] = 0
                                        self.wbufReuse[_arr1DIndex] = 0
                                    if _oldKH != kh:
                                        self.wbufReuse[_arr1DIndex] = 0
                                    if _oldKW != kw:
                                        self.wbufReuse[_arr1DIndex] = 0
                                    if _oldOH != oh:
                                        self.ibufReuse[_arr1DIndex] = 0
                                        self.obufReuse[_arr1DIndex] = 0
                                    if _oldOW != ow:
                                        self.ibufReuse[_arr1DIndex] = 0
                                        self.obufReuse[_arr1DIndex] = 0
                                    #print (f"HERE new val = {oc}, {n}, {ic}, {kh}, {kw}, {oh}, {ow}")
                                    #print (f"HERE old val ={_oldOC}, {_oldN}, {_oldIC}, {_oldKH}, {_oldKW}, {_oldOH}, {_oldOW}\n")
                                    _oldN = n
                                    _oldOC = oc
                                    _oldIC = ic
                                    _oldKH = kh
                                    _oldKW = kw
                                    _oldOH = oh
                                    _oldOW = ow
        
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
