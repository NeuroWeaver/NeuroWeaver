import csv
import os
from sys import *

class stats:
    def __init__(self, config) -> None:
        # compiler params
        self.layerName = config.layerName
        self.DDRTiling = config.DDRDims
        self.IBUFTiling = config.IBUFtileDims
        self.WBUFTiling = config.WBUFtileDims
        self.BBUFTiling = config.BBUFtileDims
        self.OBUFTiling = config.OBUFtileDims
        self.numTiles = config.numComputeTiles
        self.stride =  0 if config.isGemmlayer else config.strd
        self.pad = 0 if config.isGemmlayer else config.pad
        
        # hardware params
        self.arrayN = config.arrayN
        self.arrayM = config.arrayM
        self.memBandwidth = config.IBUFinfBandwidth
        self.memLatency = config.infLatency
        self.ibufDepth = config.IBUFBankDepth
        self.obufDepth = config.OBUFBankDepth
        self.wbufDepth = config.WBUFBankDepth
        self.bbufDepth = config.BBUFBankDepth
        self.freq = config.freq
        
        # total overall stats
        self.totalCycles = 0
        self.computeCycles = 0
        self.perTileComputeCycle = 0
        self.totalTime = 0
        self.perTileCycles = []
        self.inputLoadCycles = 0
        self.weightLoadCycles = 0
        self.outputStoreCycles = 0
        
        # utilization stats
        self.maxIbufLoadCycles = 0
        self.maxWbufLoadCycles = 0
        self.maxBbufLoadCycles = 0
        self.maxObufStoreCycles = 0
        self.perTileIbufUtil = 0
        self.perTileObufUtil = 0
        self.perTileWbufUtil = 0
        self.perTileBbufUtil = 0
        self.perTileComputeUtils = 0
        
        # Energy
        self.totalEnergy = 0
        self.perTileEnergy = 0
        

        '''
        self.log = [['layerName', 'freq', 'totalCycles', 'memBandwidth', 'memLatency', 'arrayN', 'arrayM', \
                    'ibufDepth', 'obufDepth', 'wbufDepth', 'bbufDepth', 'maxTileComputeCyles', \
                    'totalEnergy', 'totalTime', 'maxIbufLoadCycles', 'maxWbufLoadCycles', 'maxBbufLoadCycles', \
                    'maxObufStoreCycles', 'perTileIbufUtil', 'perTileObufUtil', 'perTileWbufUtil', \
                    'perTileBbufUtil', 'perTileEnergy', 'perTileComputeUtils']]
        '''
        #self.log = [[['layerName', 'totalCycles', 'memBandwidth (GB/s)', 'memLatency (s)', 'arrayN', 'arrayM', \
        #            'ibufDepth', 'totalTime (s)', 'perTileIbufUtil (%)', 'perTileObufUtil (%)', 'perTileWbufUtil (%)', \
        #            'perTileBbufUtil (%)', 'perTileComputeUtils (%)'], 'perTileCycles']]
            
        self.log = []

    def convertCyclesToTime(self):
        return self.totalCycles/self.freq

    def writeCSV(self):
        outputPath = './' + self.layerName
        f = open(outputPath, 'w')
        writer = csv.writer(f)
        for row in self.log:
            writer.writerow(row)
        f.close()

    def getStat(self):
        '''
        _ = self.log.append([self.layerName, self.freq, self.totalCycles, self.memBandwidth, self.memLatency, \
                self.arrayN, self.arrayM, self.ibufDepth, self.obufDepth, self.wbufDepth, \
                self.bbufDepth, self.maxTileComputeCyles, self.totalEnergy, \
                self.totalTime, self.maxIbufLoadCycles, self.maxWbufLoadCycles, self.maxBbufLoadCycles, \
                self.maxObufStoreCycles, self.perTileIbufUtil, self.perTileObufUtil, self.perTileWbufUtil, \
                self.perTileBbufUtil, self.perTileEnergy, self.perTileComputeUtils])
        '''
        self.totalTime = self.totalCycles * (1.0/self.freq)       
        #_ = self.log.append()
            
        #temp = [self.layerName, self.totalCycles, self.memBandwidth, self.memLatency, \
        #        self.arrayN, self.arrayM, self.ibufDepth, self.totalTime, self.perTileIbufUtil, self.perTileObufUtil, \
        #        self.perTileWbufUtil, self.perTileBbufUtil, self.perTileComputeUtils]
        

#        temp =  [self.layerName, self.DDRTiling, self.IBUFTiling, self.WBUFTiling,\
#                 self.BBUFTiling, self.OBUFTiling, self.numTiles, self.stride, self.pad, self.arrayN, \
#                 self.arrayM, self.memBandwidth, self.memLatency, self.ibufDepth, \
#                 self.obufDepth, self.wbufDepth, self.bbufDepth, self.freq, self.totalCycles,\
#                 self.computeCycles, (self.totalCycles - self.computeCycles), \
#                 self.perTileComputeCycle, self.inputLoadCycles, self.outputStoreCycles, \
#                 self.totalTime, self.perTileIbufUtil, self.perTileObufUtil, \
#                 self.perTileWbufUtil, self.perTileBbufUtil, self.perTileComputeUtils]
 

        temp =  [self.totalCycles,\
                 self.computeCycles, \
                 self.perTileComputeCycle, self.inputLoadCycles, self.outputStoreCycles, \
                 self.perTileIbufUtil, self.perTileObufUtil, \
                 self.perTileWbufUtil, self.perTileBbufUtil, self.perTileComputeUtils, self.weightLoadCycles]

        return temp, self.perTileCycles

    def printStats(self):
        self.getStat()
        print (f"\n\t ***** Simulator Output *****")
        for i in range(len(self.log[0])):
            print (f"{self.log[0][i]:{30}} = {self.log[1    ][i]:{10}}")
