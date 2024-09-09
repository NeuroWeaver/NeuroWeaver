import math
from systolic_sim.decoder import *

class compute(object):
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
        self.ih = self.decoder.IBUFtileDims['IH']
        self.iw = self.decoder.IBUFtileDims['IW']
        self.ic = self.decoder.IBUFtileDims['IC']
        self.kh = self.decoder.WBUFtileDims['KH']
        self.kw = self.decoder.WBUFtileDims['KW']
        # todo: change this to use VMEM until the json is fixed
        #self.oc = self.decoder.OBUFtileDims['OC']
        #self.oh = self.decoder.OBUFtileDims['OH']
        #self.ow = self.decoder.OBUFtileDims['OW']
        self.oc = 0 
        self.oh = 0 
        self.ow = 0 
        #print ('here = ', self.decoder.VMEMtileDims, self.decoder.OBUFtileDims)
        if len(self.decoder.VMEMtileDims) > 0:
            for k,v in self.decoder.VMEMtileDims.items():
                if 'OC' in k:
                    self.oc = self.decoder.VMEMtileDims[k]            
                elif 'OH' in k:
                    self.oh = self.decoder.VMEMtileDims[k]                            
                elif 'OW' in k:
                    self.ow = self.decoder.VMEMtileDims[k]            
        elif len(self.decoder.OBUFtileDims) > 0:
            for k,v in self.decoder.OBUFtileDims.items():
                if 'OC' in k:
                    self.oc = self.decoder.OBUFtileDims[k]            
                elif 'OH' in k:
                    self.oh = self.decoder.OBUFtileDims[k]                            
                elif 'OW' in k:
                    self.ow = self.decoder.OBUFtileDims[k]            
        
        # self.oc = self.decoder.VMEMtileDims['OC'] if len(self.decoder.VMEMtileDims) > 0 else \
        #     self.decoder.OBUFtileDims['OC'] if len(self.decoder.OBUFtileDims) > 0 else 0
        # self.oh = self.decoder.VMEMtileDims['OH'] if len(self.decoder.VMEMtileDims) > 0 else \
        #     self.decoder.OBUFtileDims['OH'] if len(self.decoder.OBUFtileDims) > 0 else 0
        # self.ow = self.decoder.VMEMtileDims['OW'] if len(self.decoder.VMEMtileDims) > 0 else \
        #     self.decoder.OBUFtileDims['OW'] if len(self.decoder.OBUFtileDims) > 0 else 0
                
        self.strd = self.decoder.strd
        self.sysArrayRows = self.decoder.arrayN
        self.sysArrayCols = self.decoder.arrayM

        #print ("ITile Dims = ", self.decoder.IBUFtileDims)
        #print ("WTile Dims = ", self.decoder.WBUFtileDims)
        #print ("BTile Dims = ", self.decoder.BBUFtileDims)
        #print ("OTile Dims = ", self.decoder.OBUFtileDims)
        
    def getComputeCycles(self):
        
        #oh = math.floor((self.ih - self.kh + self.strd)/ self.strd)
        #ow = math.floor((self.iw - self.kw + self.strd)/ self.strd)

        oh = self.oh
        ow = self.ow
        n = self.decoder.DDRDims['N']
        #print ("\n**********\n")
        #print (f'n = {n} , oc = {self.oc}, ic = {self.ic},  kh = {self.kh},  kw = {self.kw},  oh = {self.oh},  ow = {self.ow}')
        #print (f' ih = {self.ih},  iw = {self.iw},  sysArrayRows = {self.sysArrayRows},  sysArrayCols = {self.sysArrayCols}  ')

        _compute_cycles =  (n * oh * ow) * math.ceil(self.kh * self.kw * self.ic / self.sysArrayRows) * \
                                            math.ceil(self.oc / self.sysArrayCols)
        
        _pipeline_delay_cycles = self.sysArrayRows + self.sysArrayCols

        self.perTileComputeCycles = _compute_cycles + _pipeline_delay_cycles

        self.totalComputeCycles += self.perTileComputeCycles
        
        #print ("Per Tile Compute cycles  = ", self.perTileComputeCycles)
        
        return self.perTileComputeCycles

    def getNumMACs(self):
        return (self.oh * self.ow * self.oc * self.kh * self.kw * self.ic)

    def getUtilization(self):
        array_util = ((self.kw * self.kh * self.ic) / (math.ceil(self.kw*self.kh*self.ic/self.sysArrayRows) \
                        * self.sysArrayRows)) * (self.oc / (math.ceil(self.oc/self.sysArrayCols) * self.sysArrayCols)) * 100

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
