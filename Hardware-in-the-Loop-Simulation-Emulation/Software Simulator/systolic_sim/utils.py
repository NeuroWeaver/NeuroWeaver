import os
import glob
import math
import fnmatch

dimMapping = { 0: 'OC', 1: 'N', 2: 'IC', 3: 'KH', 4: 'KW', 5: 'OH', 6: 'OW' }
gemm4dDimMapping = { 0: 'B', 1: 'C', 2: 'M', 3: 'N', 4: 'P' }
gemmDimMapping = {0: 'M', 1: 'N', 2: 'P' }
matmulMapping = {0: 'B', 1: 'M', 2: 'N', 3: 'P' }

testPath = ''
def get1DIndex(a, b, c, d, bSize, cSize, dSize):
    _dim4_index = d + (c * dSize) + (b * cSize * dSize) + (a * bSize * cSize * dSize)
    return _dim4_index

def get5Dto1DIndex(e, a, b, c, d, aSize, bSize, cSize, dSize):
    _dim5_index = d + (c * dSize) + (b * cSize * dSize) + (a * bSize * cSize * dSize) + (e * bSize * cSize * dSize * aSize)
    return _dim5_index

def findFile(dirPath, searchStr):  
    for file in glob.glob(os.path.join(dirPath, searchStr)):
        return file
    return 'Error'

def floor_a_by_b(a, b):
    return int(float(a) / b)

def ceil_a_by_b(a, b):
    return int(math.ceil(float(a) / b))
    
stats = {"layerName":None, "DDRTiling": None, "IBUFTiling": None, \
          "WBUFTiling" : None, "BBUFTiling" : None, "OBUFTiling" : None, \
          "NumTiles" : None, "stride" : None, "pad" : None, \
          "arrayN" : None, "arrayM" : None, "memBandwidth" : None, \
          "memLatency" : None, "ibufDepth" : None, "obufDepth" : None, \
          "wbufDepth" : None, "bbufDepth" : None, "freq" : None, \
          "totalCycles" : None, "computeCycle" : None, "totalTime" : None, \
          "ComputeCyclesPerTile" : None, "LoadCyclesPerTile" : None, \
          "StoreCyclesPerTile" : None, \
          "perTileIbufUtil" : None, "perTileObufUtil" : None, "perTileWbufUtil" : None, \
          "perTileBbufUtil" : None, "perTileComputeUtils" : None, "SIMD Compute Cycles/tile" : None, \
          "SIMD Load Cycles/tile" : None, "SIMD Store Cycles/tile" : None, "compute2total%" : None, \
          "Load_to_Tot" : None, "Systolic_Comp_to_Tot" : None, "SIMD_Comp_to_Tot" : None, \
          "Store_to_Tot" : None, "MemWaitCycle" : None}
