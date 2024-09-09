import math
from systolic_sim.decoder import *

class computeGemm(object):
    """
    This class models a systolic array computation
    """
    def __init__(self, decoder):
        self.decoder = decoder
        # per tile params
        self.perTileComputeCycles =  0
        self.totalComputeCycles = 0
        # buffer params
        self.ibufComputeTag = True
        self.obufComputeTag = True
        self.wbufComputeTag = True
        self.bbufComputeTag = True
        self.getDecoderParams()
        # Energy -> This statement is dependent on the previous as Python is interpreted
        self.numMACs = self.getNumMACs()

    def getDecoderParams(self):
        # tile params
        self.b = self.decoder.IBUFtileDims['B'] if self.decoder.gemm4d == True else 1
        self.c = self.decoder.IBUFtileDims['C'] if self.decoder.gemm4d == True else 1
        self.m = self.decoder.IBUFtileDims['M']
        self.n = self.decoder.WBUFtileDims['N']
        self.p = self.decoder.WBUFtileDims['P']
        # todo: change this to use VMEM until the json is fixed
        #self.p = self.decoder.OBUFtileDims['OC']
        # = self.decoder.OBUFtileDims['OH']
        #self.m = self.decoder.OBUFtileDims['OW']

        self.sysArrayRows = self.decoder.arrayN
        self.sysArrayCols = self.decoder.arrayM
        
    def getComputeCycles(self):
        
        _compute_cycles = self.c * (self.b * self.m) * math.ceil(self.n / self.sysArrayRows) * \
                                            math.ceil(self.p / self.sysArrayCols)
        
        _pipeline_delay_cycles = self.sysArrayRows + self.sysArrayCols

        self.perTileComputeCycles = _compute_cycles + _pipeline_delay_cycles

        self.totalComputeCycles += self.perTileComputeCycles
        
        #print ("Per Tile Compute cycles  = ", self.perTileComputeCycles)
        return self.perTileComputeCycles

    def getNumMACs(self):
        return (self.c * self.m * self.p  * self.n)

    def getUtilization(self):
        array_util = ( self.n / (math.ceil(self.n/self.sysArrayRows) \
                        * self.sysArrayRows)) * (self.p / (math.ceil(self.p/self.sysArrayCols) * self.sysArrayCols)) * 100
        return array_util

    def getEnergy(self):
        return self.decoder.energyPerMAC * self.numMACs
    
    def updateTags(self, arr1DIndex):
        if self.decoder.ibufReuse[arr1DIndex] == 0:
            self.ibufComputeTag = ~self.ibufComputeTag
        if self.decoder.wbufReuse[arr1DIndex] == 0:
            self.wbufComputeTag = ~self.wbufComputeTag
        if self.decoder.bbufReuse[arr1DIndex] == 0:
            self.bbufComputeTag = ~self.bbufComputeTag
        if self.decoder.wbufReuse[arr1DIndex] == 0:
            self.obufComputeTag = ~self.obufComputeTag
