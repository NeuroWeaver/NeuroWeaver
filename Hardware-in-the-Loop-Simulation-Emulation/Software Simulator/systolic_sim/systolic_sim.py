from math import ceil
from systolic_sim.buffer import *
from systolic_sim.compute import *
from systolic_sim.computeGemm import *
from systolic_sim.decoder import *
from systolic_sim.decoderGemm import *
from systolic_sim.utils import *
from systolic_sim.stats import *
import sys

class systolic_sim:

    def __init__(self, configPath, testPath, ddrBandwidth = 38000000000, fused = False, layerType = 'systolic', isGemmlayer = False) -> None:
        self.testPath = testPath
        self.configPath = configPath
        if isGemmlayer:
            self.decoder = decoderGemm(self.configPath,self.testPath, ddrBandwidth, layerType)
        else:
            self.decoder = decoder(self.configPath,self.testPath, ddrBandwidth, layerType)

        ## todo: move this inside stats init? -> This line is needed right after decoder instantiation as Python is interpreted
        self.decoderCycles = self.decoder.cycle()
        if isGemmlayer:
            self.compute = computeGemm(self.decoder)
        else:
            self.compute = compute(self.decoder)
        self.ibuf = ibuf(self.decoder, self.compute) 
        self.wbuf = wbuf(self.decoder, self.compute)
        self.bbuf = bbuf(self.decoder, self.compute)
        self.obuf = obuf(self.decoder, self.compute)
        self.stats = stats(self.decoder)
        ## params for cycles
        self.ibufCycles = []
        self.ibufStallCycles = 0
        self.computeCycles = []
        self.perTagTotalCycles = {}
        self.perTagCycles = []
        self.totalCycles = []
        self.fusedLayer = fused
        self.layerType = layerType
    
    def prefixSum(self,ele, arr):
        if len(arr) == 0:
            arr.append(ele)
        else:
            arr.append(arr[len(arr) - 1] + ele)
        return arr

    def computeTile(self, _arr1DIndex, _prevArr1DIndex, _iterCount):
        _computeCycles = 0
        if _iterCount == -1:
            _ibufLoadCycles = self.ibuf.load(_arr1DIndex) 
            _totalCyclesThisIter = _ibufLoadCycles
            self.stats.inputLoadCycles = _ibufLoadCycles
            #print ("Here 0 _totalCyclesThisIter", _totalCyclesThisIter)
        elif _iterCount == 0:
            _ibufLoadCycles = self.ibuf.load(_arr1DIndex+1)
            _computeCycles = self.compute.getComputeCycles()
            self.stats.perTileComputeCycle = _computeCycles
            _totalCyclesThisIter = max(_computeCycles, _ibufLoadCycles)
            #print ("Here 1 _totalCyclesThisIter", _totalCyclesThisIter, 'compute = ', _computeCycles)
        elif _iterCount == self.decoder.numComputeTiles - 1:
            _computeCycles = self.compute.getComputeCycles()
            _obufStoreCycles = self.obuf.store(_prevArr1DIndex)
            _totalCyclesThisIter =  max(_computeCycles, _obufStoreCycles)
            #print ("Here 3 _totalCyclesThisIter", _totalCyclesThisIter)
        elif _iterCount == self.decoder.numComputeTiles:
            _obufStoreCycles = self.obuf.store(_prevArr1DIndex)
            #print ("_obufStoreCycles = ", _obufStoreCycles)
            _totalCyclesThisIter = _obufStoreCycles
            #print ("Here 4 _totalCyclesThisIter", _totalCyclesThisIter)
            self.stats.outputStoreCycles = _obufStoreCycles
        else:
            _ibufLoadCycles = self.ibuf.load(_arr1DIndex+1)
            _computeCycles = self.compute.getComputeCycles()
            _obufStoreCycles = self.obuf.store(_prevArr1DIndex)
            _totalCyclesThisIter = max(_computeCycles, _ibufLoadCycles + _obufStoreCycles)
            #print ("Here 2 _totalCyclesThisIter", _totalCyclesThisIter)
        
        self.perTagTotalCycles[self.obuf.storeTag] =_totalCyclesThisIter
        self.stats.perTileCycles.append(_totalCyclesThisIter)
        self.stats.totalCycles += ceil(_totalCyclesThisIter)
        self.stats.computeCycles += _computeCycles
        #print ("Total Accum Time = ", self.stats.totalCycles, "\n")
        
        self.updateTags(_prevArr1DIndex,_arr1DIndex)

    def updateTags(self, _prevArr1DIndex, _arr1DIndex):
        ## Since, depending on next tile, we will update the tag
        self.ibuf.updateLoadTag(_arr1DIndex)
        self.compute.updateTags(_arr1DIndex) 
        self.obuf.updateStoreTag(_prevArr1DIndex)

    def getUtilization(self):
        self.stats.perTileIbufUtil = self.ibuf.bankUtilization
        self.stats.perTileObufUtil = self.obuf.bankUtilization
        self.stats.perTileWbufUtil = self.wbuf.bankUtilization
        self.stats.perTileBbufUtil = self.bbuf.bankUtilization
        self.stats.perTileComputeUtils = self.compute.getUtilization()
    
    def getEnergy(self):
        self.stats.perTileEnergy = self.compute.getEnergy()
        self.stats.ibufTotalEnergy = self.ibuf.totalEnergy
        self.stats.obufTotalEnergy = self.obuf.totalEnergy
        self.stats.wbufTotalEnergy = self.wbuf.totalEnergy
        self.stats.bbufTotalEnergy = self.bbuf.totalEnergy
        self.stats.totalEnergy = self.stats.perTileEnergy + self.stats.ibufTotalEnergy + self.stats.obufTotalEnergy + \
                                    self.stats.wbufTotalEnergy + self.stats.bbufTotalEnergy

    def cycleConv(self):
        _iterCount = 0
        _prevArr1DIndex = 0
        self.computeTile(0,_prevArr1DIndex, -1)
        # compute iters
        for oc in range(self.decoder.tileDims['OC']):
            for n in range(self.decoder.tileDims['N']):
                for ic in range(self.decoder.tileDims['IC']):
                    for kh in range(self.decoder.tileDims['KH']):
                        for kw in range(self.decoder.tileDims['KW']):
                            for oh in range(self.decoder.tileDims['OH']):
                                for ow in range(self.decoder.tileDims['OW']): ## Because we add ibuf cycles intially
                                    _arr1DIndex = get1DIndex(oc, ic, oh, ow, self.decoder.tileDims['IC'], self.decoder.tileDims['OH'], self.decoder.tileDims['OW'])
                                    self.computeTile(_arr1DIndex, _prevArr1DIndex, _iterCount)
                                    if self.fusedLayer is True:
                                        _ibufLoadCycles = self.ibuf.load(_arr1DIndex) 
                                        _wbufLoadCycles = self.wbuf.load(_arr1DIndex) 
                                        self.stats.inputLoadCycles = _ibufLoadCycles
                                        self.stats.weightLoadCycles = _wbufLoadCycles
                                        _computeCycles = self.compute.getComputeCycles()
                                        self.stats.perTileComputeCycle = _computeCycles
                                        _obufStoreCycles = self.obuf.store(_prevArr1DIndex)
                                        self.stats.outputStoreCycles = _obufStoreCycles
                                        ## We just need per tile stats
                                        break
                                    
                                    #self.stats.totalCycles += _cyclesThisIter
                                    #self.stats.perTileCycles.append[_cyclesThisIter]
                                    _iterCount += 1
                                    _prevArr1DIndex = _arr1DIndex

        self.computeTile(0, _prevArr1DIndex, self.decoder.numComputeTiles)
        #One time addition on decoder overhead
        self.stats.totalCycles += self.decoderCycles 
        self.getUtilization()
        self.getEnergy()
    
    def cycleGemm(self):
        _iterCount = 0
        _prevArr1DIndex = 0
        self.computeTile(0,_prevArr1DIndex, -1)
        # compute iters
        #print (self.decoder.tileDims)
        for b in range(self.decoder.tileDims['B']):
            for c in range(self.decoder.tileDims['C']):
                for m in range(self.decoder.tileDims['M']):
                    for n in range(self.decoder.tileDims['N']):
                        for p in range(self.decoder.tileDims['P']):
                       
                            _arr1DIndex = get5Dto1DIndex(p, n, m, c, b, self.decoder.tileDims['N'], self.decoder.tileDims['M'], \
                                self.decoder.tileDims['C'], self.decoder.tileDims['B'])
                            self.computeTile(_arr1DIndex, _prevArr1DIndex, _iterCount)
                            #print (self.fusedLayer)
                            if self.fusedLayer is True:
                                _ibufLoadCycles = self.ibuf.load(_arr1DIndex) 
                                _wbufLoadCycles = self.wbuf.load(_arr1DIndex)
                                self.stats.inputLoadCycles = _ibufLoadCycles
                                self.stats.weightLoadCycles = _wbufLoadCycles
                                #print ("weight = ", _wbufLoadCycles)
                                _computeCycles = self.compute.getComputeCycles()
                                self.stats.perTileComputeCycle = _computeCycles
                                _obufStoreCycles = self.obuf.store(_prevArr1DIndex)
                                self.stats.outputStoreCycles = _obufStoreCycles
                                ## We just need per tile stats
                                break
                                    
                            #self.stats.totalCycles += _cyclesThisIter
                            #self.stats.perTileCycles.append[_cyclesThisIter]
                            _iterCount += 1
                            _prevArr1DIndex = _arr1DIndex

        self.computeTile(0, _prevArr1DIndex, self.decoder.numComputeTiles)
        #One time addition on decoder overhead
        self.stats.totalCycles += self.decoderCycles 
        self.getUtilization()
        self.getEnergy()
    
    def cycle(self):
        if self.decoder.isGemmlayer:
            self.cycleGemm()
        else:
            self.cycleConv()
        
    def printStats(self):
        self.stats.printStats()
    def getStats(self):
        return self.stats.getStat()

class main():
    def __init__(self, testDir) -> None:        
        sysSim = systolic_sim(testDir)
        sysSim.cycle()
        self.stat, self.perCycle = sysSim.getStats()

if __name__ == "__main__":
    assert(len(sys.argv) == 2), 'Usage python3 systolic_sim.py <test_directory_path>'
    obj = main(argv[1])
    print (obj.stat, '\n')
    print (obj.perCycle)
    