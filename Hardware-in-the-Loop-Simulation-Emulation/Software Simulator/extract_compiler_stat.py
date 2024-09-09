
from collections import defaultdict
import json
import sys
import os
import glob

dimMapping = { 0: 'OC', 1: 'N', 2: 'IC', 3: 'KH', 4: 'KW', 5: 'OH', 6: 'OW' }

class parser():
    def __init__(self, testPath) -> None:
        self.testPath = testPath
        self.arrayN = 8
        self.arrayM = 8
        self.obuf_ld = 0
        self.DDRDims = {}
        self.IBUFTileSize = 0
        self.OBUFTileSize = 0
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
        self.tileDims = {}
        self.ibufReqsPerTile = 1
        self.obufLdReqsPerTile = 1
        self.obufStReqsPerTile = 1
        self.wbufReqsPerTile = 1
        self.bbufReqsPerTile = 1
        self.sysComputeLoops = 1
        self.ibufSizePerReq = 0
        self.wbufSizePerReq = 0
        self.bbufSizePerReq = 0
        self.obufSizePerReq = 0
    
    def findFile(self, dirPath, searchStr):  
        for file in glob.glob(os.path.join(dirPath, searchStr)):
            return file
        return 'Error'

    def parse_json_file(self) -> None:
        _jsonPath = self.findFile(self.testPath, '*json.json')
        with open(_jsonPath, 'r') as f:
            _data = json.load(f)
            #print (_data['program'][0]['operation_parameters'])
            self.strd = _data['program'][0]['operation_parameters']["stride"]
            self.pad = _data['program'][0]['operation_parameters']['pad']
            
            for item in _data['program'][0]['iterable_dimensions']:
                self.DDRDims[item] = _data['program'][0]['iterable_dimensions'][item]
            
            in_key = _data['program'][0]['inputs'][0]['data_path']
            in_key = 'IBUF' in in_key
            if in_key:
                for k,v in _data['program'][0]['inputs'][0]['tiling']['IBUF'].items():
                    self.IBUFtileDims[k] = v
                for k,v in _data['program'][0]['inputs'][1]['tiling']['WBUF'].items():
                    self.WBUFtileDims[k] = v    
                for k,v in _data['program'][0]['inputs'][2]['tiling']['BBUF'].items():
                    self.BBUFtileDims[k] = v
            out_key = _data['program'][0]['outputs'][0]['data_path']
            out_key_1 = 'OBUF' in out_key
            if out_key_1:   
                for k,v in _data['program'][0]['outputs'][0]['tiling']['OBUF'].items():
                    self.OBUFtileDims[k] = v          
                    
    def parse_arch_cfg(self):
        _archCfgPath = self.findFile(self.testPath, '*arch_cfg.json')
        with open(_archCfgPath, 'r') as f:
            _data = json.load(f)
            self.IBUFbitwidth = _data['DATA_WIDTH']
            self.OBUFbitwidth = _data['ACC_WIDTH']
            self.WBUFbitwidth = _data['WGT_WIDTH']
            self.BBUFbitwidth = _data['BIAS_WIDTH']
            self.arrayN = _data['ARRAY_N']
            self.arrayM = _data['ARRAY_M']
            
    
    def parse_instruction_file(self) -> None:
        _instrPath = self.findFile(self.testPath, '*string_final.txt')
        with open(_instrPath, 'r') as f:
            for line in f:
                ## To find number of tiles
                if "SA_LOOP_CFG 0" in line:
                    _loop = line.split(',')
                    _loopIter = int(_loop[2].strip('\n')) + 1
                    _loop = int(_loop[1].strip())
                    if _loop < 7:
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
                    ## To find number of systolic compute iterations
                    if _loop > 6 and _loop < 14:
                        self.sysComputeLoops = self.sysComputeLoops * _loopIter
                    if _loop == 2 and _loopIter > 1:
                        self.obuf_ld = 1 
                    ## OBUF
                    if _loop > 23 and _loop < 28:
                        self.obufLdReqsPerTile *= _loopIter
                    if _loop > 28:
                        self.obufStReqsPerTile *= _loopIter
                    ## IBUF
                    if _loop > 13 and _loop < 18:
                        self.ibufReqsPerTile *= _loopIter
                    ## WBUF
                    if _loop > 22 and _loop < 24:
                        self.wbufReqsPerTile *= _loopIter
                    ## BBUF
                    if _loop > 27 and _loop < 29:
                        self.bbufReqsPerTile *= _loopIter
        
       
    def reqPerTile(self):
        self.ibufSizePerReq = int((self.IBUFTileSize/self.ibufReqsPerTile) / self.arrayN)
        self.wbufSizePerReq = int((self.WBUFTileSize/self.wbufReqsPerTile) / (self.arrayN * self.arrayM))
        self.bbufSizePerReq = int((self.BBUFTileSize/self.bbufReqsPerTile) / self.arrayM)
        self.obufSizePerReq = int((self.OBUFTileSize/self.obufStReqsPerTile) / self.arrayM)

    def tileSize(self):
        self.IBUFTileSize = self.computeTileSize(self.IBUFtileDims, self.IBUFbitwidth/8)
        self.WBUFTileSize = self.computeTileSize(self.WBUFtileDims, self.WBUFbitwidth/8)
        self.BBUFTileSize = self.computeTileSize(self.BBUFtileDims, self.BBUFbitwidth/8)
        self.OBUFTileSize = self.computeTileSize(self.OBUFtileDims, self.OBUFbitwidth/8)
    
    def computeTileSize(self, _tileDims, bitwidth):
        _tsize = 1
        for k,v in _tileDims.items():
            _tsize *= v
        _tsize *= bitwidth
        return _tsize
      

    def parse_files(self):
        self.parse_json_file()
        self.parse_instruction_file()
        self.parse_arch_cfg()
        self.tileSize()
        self.reqPerTile()
    
    def print_stats(self):
        
        print ("testPath"," = ", self.testPath)
        print ("arrayN"," = ", self.arrayN) 
        print ("arrayM"," = ", self.arrayM)
        print ("OBUF Ld/ IC Tiled", " = ", self.obuf_ld)
        print ("IBUFTileSize"," = ", self.IBUFTileSize)
        print ("OBUFTileSize"," = ", self.OBUFTileSize)
        print ("WBUFTileSize"," = ", self.WBUFTileSize)
        print ("BBUFTileSize"," = ", self.BBUFTileSize)
        print ("numComputeTiles"," = ", self.numComputeTiles)
        print ("IBUFnumTiles"," = ", self.IBUFnumTiles)
        print ("OBUFnumTiles"," = ", self.OBUFnumTiles)
        print ("WBUFnumTiles"," = ", self.WBUFnumTiles)
        print ("BBUFnumTiles"," = ", self.BBUFnumTiles)
        print ("DDRDims"," = ", self.DDRDims) 
        print ("IBUFtileDims"," = ", self.IBUFtileDims)
        print ("OBUFtileDims"," = ", self.OBUFtileDims)
        print ("WBUFtileDims"," = ", self.WBUFtileDims)
        print ("BBUFtileDims"," = ", self.BBUFtileDims)
        print ("tileDims"," = ", self.tileDims)
        print ("ibufReqsPerTile"," = ", self.ibufReqsPerTile)
        print ("obufLdReqsPerTile"," = ", self.obufLdReqsPerTile)
        print ("obufStReqsPerTile"," = ", self.obufStReqsPerTile)
        print ("wbufReqsPerTile"," = ", self.wbufReqsPerTile)
        print ("bbufReqsPerTile"," = ", self.bbufReqsPerTile)
        print ("sysComputeLoops"," = ", self.sysComputeLoops)
        print ("ibufSizePerReq"," = ", self.ibufSizePerReq)
        print ("wbufSizePerReq"," = ", self.wbufSizePerReq)
        print ("bbufSizePerReq"," = ", self.bbufSizePerReq)
        print ("obufSizePerReq"," = ", self.obufSizePerReq)

testPath = sys.argv[1]
parserObj = parser(testPath)
parserObj.parse_files()
parserObj.print_stats()
