import os
import math
from genesysDecoder import *
from systolic_sim.utils import *
from systolic_sim.systolic_sim import *
from sram.cacti_sweep import CactiSweep
from simd_sim.simulator.pipeline import *
from simd_sim.simulator.config_parser import *

class genesysCompute:
    def __init__(self, decoder, stats, testDir) -> None:
        self.decoder = decoder
        self.gStats = stats
        ## Stats
        self.metric = None
        self.totCycles = 0
        self.results = None
        self.systolicResult = None
        self.simdResult = None
        self.genesysResult = None
        self.layerType = self.decoder.layerType
        self.testDir = testDir
        self.sysComputeCycles = 0
        self.sysLoadCycles = 0
        self.weightLoadCycles = 0
        self.sysStoreCycles = 0
        self.simdComputeCycles = 0
        self.simdLoadCycles = 0
        self.simdStoreCycles = 0
        self.perTileCycles = []
        self.totLoadCycles = 0
        self.totSysComputeCycles = 0
        self.totSimdComputeCycles = 0
        self.totStoreCycles = 0
        self.totSIMDCycles = 0
        self.simdBufAccesses = {}
       
    def systolic_sim(self, mode):
        print (" ------- In Systolic Sim")
        fused = True if "fused" in self.decoder.layerType else False
        sysSim = systolic_sim(self.decoder.configPath, self.decoder.testPath, \
            ddrBandwidth = self.decoder.infBandwidth, fused = fused,layerType = self.decoder.layerType, isGemmlayer = self.decoder.isGemmlayer)
        sysSim.cycle()
        self.systolicResult = sysSim.getStats()
        self.sysComputeCycles = self.systolicResult[0][2]
        self.sysLoadCycles = self.systolicResult[0][3]
        self.sysStoreCycles = self.systolicResult[0][4]

        self.gStats.genesys_stats['Genesys'] = defaultdict(int)
        self.gStats.genesys_stats['Systolic'] = defaultdict(int)
        self.gStats.genesys_stats['Simd'] = defaultdict(int)
        self.gStats.genesys_stats['Genesys']['totCycles'] = self.systolicResult[0][0] 
        self.gStats.genesys_stats['Genesys']['totTime(us)'] = self.systolicResult[0][0] * (1.0/self.decoder.freq)
        self.gStats.genesys_stats['Genesys']['load2tot_cycles'] = 0
        self.gStats.genesys_stats['Genesys']['sysCompute2tot_cycles'] = 0
        self.gStats.genesys_stats['Genesys']['simd2tot_cycles'] = 0
        self.gStats.genesys_stats['Genesys']['memWaitCycles'] = 0
        self.gStats.genesys_stats['Genesys']['memWaitCycles2tot_cycles'] = 0
        self.gStats.genesys_stats['Genesys']['computeCycles2tot_cycles'] = 0

        self.gStats.genesys_stats['Simd']['simdtotalCycles'] = 0
        self.gStats.genesys_stats['Simd']['simdComputeCyclesPerTile'] = 0
        self.gStats.genesys_stats['Simd']['simdLoadCycles'] = 0
        self.gStats.genesys_stats['Simd']['simdStoreCycles'] = 0
        self.gStats.genesys_stats['Simd']['NumComputeTiles'] = 0
        self.gStats.genesys_stats['Simd']['VMEM1LoadTiles'] = 0
        self.gStats.genesys_stats['Simd']['VMEM2LoadTiles'] = 0
        self.gStats.genesys_stats['Simd']['StoreTiles'] =0
        self.gStats.genesys_stats['Simd']['StoreTilesNameSpace'] = 0
        self.gStats.genesys_stats['Simd']['perTileVMEM1Util'] = 0
        self.gStats.genesys_stats['Simd']['perTileVMEM2Util'] = 0
        ##
        self.gStats.genesys_stats['Systolic']['systotalCycles'] = self.systolicResult[0][0] 
        #self.gStats.genesys_stats['Systolic']['syscomputeCycle'] = self.systolicResult[0][1]
        self.gStats.genesys_stats['Systolic']['sysComputeCyclesPerTile'] = self.systolicResult[0][2]
        self.gStats.genesys_stats['Systolic']['sysLoadCyclesPerTile'] = self.systolicResult[0][3]
        self.gStats.genesys_stats['Systolic']['sysStoreCyclesPerTile'] = self.systolicResult[0][4]
        self.gStats.genesys_stats['Systolic']['perTileIbufUtil'] = self.systolicResult[0][5]
        self.gStats.genesys_stats['Systolic']['perTileObufUtil'] = self.systolicResult[0][6]
        self.gStats.genesys_stats['Systolic']['perTileWbufUtil'] = self.systolicResult[0][7]
        self.gStats.genesys_stats['Systolic']['perTileBbufUtil'] = self.systolicResult[0][8]
        self.gStats.genesys_stats['Systolic']['perTileComputeUtils'] = self.systolicResult[0][9]
        if 'energy' in mode:
            print ('here energy')
            self.get_energy()
        #print ("systotalCycles = ", self.systolicResult[0][0])
        #print ("sysComputeCyclesPerTile = ", self.systolicResult[0][2])
        #print ("sysLoadCyclesPerTile = ", self.systolicResult[0][3])
        #print ("sysStoreCyclesPerTile = ", self.systolicResult[0][4])


    def simd_sim(self, mode):
        print (" ------- In SIMD Sim")
        _sim_config_path = os.path.join(self.decoder.configPath, 'simd_config.json')
        config = ConfigParser(self.decoder.testPath, self.decoder.layerName, ddrBandwidth = self.decoder.infBandwidth, sim_config_path=_sim_config_path).parse()
        pipeline = Pipeline(config)
        self.simdResult, self.simdBufAccesses = pipeline.run(inst_file_path=config["instructions_path"])
        self.simdComputeCycles = self.simdResult['perTileCycles']
        self.simdLoadCycles = self.simdResult['LoadCycles']
        self.simdStoreCycles = self.simdResult['StoreCycles']
        self.gStats.genesys_stats['Compiler']['NumTiles'] = self.simdResult['numTiles']
        ## Not required stats
        self.gStats.genesys_stats['Genesys'] = defaultdict(int)
        ## Rohan: Some approximation given if we have 2 loads then the load with lesser tile is
        ## generally for biases which takes very less cycles given they have small dimensions. Hence taking max below
        self.gStats.genesys_stats['Genesys']['totCycles'] = ((self.simdComputeCycles + self.simdStoreCycles) * self.decoder.numSIMDComputeTiles) + \
                                                            self.simdLoadCycles * max(self.decoder.numSIMDLoadTiles['VMEM1'],self.decoder.numSIMDLoadTiles['VMEM2'])
        self.gStats.genesys_stats['Genesys']['totTime(us)'] = self.gStats.genesys_stats['Genesys']['totCycles'] * (1.0/self.decoder.freq)
        self.gStats.genesys_stats['Genesys']['load2tot_cycles'] = 0
        self.gStats.genesys_stats['Genesys']['sysCompute2tot_cycles'] = 0
        self.gStats.genesys_stats['Genesys']['simd2tot_cycles'] = 0
        self.gStats.genesys_stats['Genesys']['memWaitCycles'] = 0
        self.gStats.genesys_stats['Genesys']['memWaitCycles2tot_cycles'] = 0
        self.gStats.genesys_stats['Genesys']['computeCycles2tot_cycles'] = 0
        self.gStats.genesys_stats['Systolic'] = defaultdict(int)
        self.gStats.genesys_stats['Systolic']['systotalCycles'] = 0
        #self.gStats.genesys_stats['Systolic']['syscomputeCycle'] = 0
        self.gStats.genesys_stats['Systolic']['sysComputeCyclesPerTile'] = 0
        self.gStats.genesys_stats['Systolic']['sysLoadCyclesPerTile'] = 0
        self.gStats.genesys_stats['Systolic']['sysStoreCyclesPerTile'] = 0
        self.gStats.genesys_stats['Systolic']['perTileIbufUtil'] = 0
        self.gStats.genesys_stats['Systolic']['perTileObufUtil'] = 0
        self.gStats.genesys_stats['Systolic']['perTileWbufUtil'] = 0
        self.gStats.genesys_stats['Systolic']['perTileBbufUtil'] = 0
        self.gStats.genesys_stats['Systolic']['perTileComputeUtils'] = 0
        ##
        self.gStats.genesys_stats['Simd'] = defaultdict(int)
        self.gStats.genesys_stats['Simd']['simdtotalCycles'] = self.gStats.genesys_stats['Genesys']['totCycles']
        
        self.gStats.genesys_stats['Simd']['simdComputeCyclesPerTile'] = self.simdResult['perTileCycles'] 
        self.gStats.genesys_stats['Simd']['simdLoadCycles'] = self.simdResult['LoadCycles']
        self.gStats.genesys_stats['Simd']['simdStoreCycles'] = self.simdResult['StoreCycles'] 
        self.gStats.genesys_stats['Simd']['NumComputeTiles'] = self.decoder.numSIMDComputeTiles
        self.gStats.genesys_stats['Simd']['VMEM1LoadTiles'] = self.decoder.numSIMDLoadTiles['VMEM1']
        self.gStats.genesys_stats['Simd']['VMEM2LoadTiles'] = self.decoder.numSIMDLoadTiles['VMEM2']
        self.gStats.genesys_stats['Simd']['StoreTiles'] = self.decoder.numSIMDComputeTiles
        self.gStats.genesys_stats['Simd']['StoreTilesNameSpace'] = self.decoder.SIMDStoreNameSpace
        #self.gStats.genesys_stats['Simd']['perTileVMEM1Util'] = self.simdResult['perTileVMEM1Util'] 
        #self.gStats.genesys_stats['Simd']['perTileVMEM2Util'] = self.simdResult['perTileVMEM2Util'] 
        self.gStats.genesys_stats['Simd']['perTileVMEM1Util'] = 0
        self.gStats.genesys_stats['Simd']['perTileVMEM2Util'] = 0 
        if 'energy' in mode:
            print ('here energy')
            self.get_energy()
        
    
    def genesys_sim(self, layerType, mode):
        print (" ------- In Systolic Sim")
        #print ("layerType = ", layerType)
        fused = True if "fused" in self.decoder.layerType else False
        #print ("fused = ", fused)
        sysSim = systolic_sim(self.decoder.configPath, self.decoder.testPath, ddrBandwidth = self.decoder.infBandwidth//2, \
            fused = fused, layerType = self.decoder.layerType, isGemmlayer = self.decoder.isGemmlayer)
        sysSim.cycle()
        self.systolicResult = sysSim.getStats()
        self.sysComputeCycles = self.systolicResult[0][2]
        self.sysLoadCycles = self.systolicResult[0][3]
        self.weightLoadCycles = self.systolicResult[0][10]
        self.sysStoreCycles = self.systolicResult[0][4]
        _sim_config_path = os.path.join(self.decoder.configPath, 'simd_config.json')
        print (" ------- In SIMD Sim")
        config = ConfigParser(self.decoder.testPath, self.decoder.layerName, ddrBandwidth = self.decoder.infBandwidth//2, sim_config_path=_sim_config_path, layerType = layerType).parse()
        pipeline = Pipeline(config)
        self.simdResult, self.simdBufAccesses = pipeline.run(inst_file_path=config["instructions_path"])
        self.simdComputeCycles = self.simdResult['perTileCycles'] ## for SIMD, we decided to go with this which has 6 scaling factor
        self.simdLoadCycles = self.simdResult['LoadCycles']
        self.simdStoreCycles = self.simdResult['StoreCycles']
        print (" ------- In Genesys Sim")

        self.cycle()

        self.gStats.genesys_stats['Genesys'] = defaultdict(int)
        self.gStats.genesys_stats['Genesys']['totCycles'] = self.totCycles
        self.gStats.genesys_stats['Genesys']['totTime(us)'] = self.totCycles * (1.0/self.decoder.freq)
        self.gStats.genesys_stats['Genesys']['load2tot_cycles'] = self.totLoadCycles/self.totCycles
        self.gStats.genesys_stats['Genesys']['sysCompute2tot_cycles'] = self.totSysComputeCycles/self.totCycles
        self.gStats.genesys_stats['Genesys']['simd2tot_cycles'] = (self.totSimdComputeCycles + self.totStoreCycles) /self.totCycles
        _totalComputeCycles = max(self.totSysComputeCycles, self.totSimdComputeCycles +  self.totStoreCycles)
        self.gStats.genesys_stats['Genesys']['memWaitCycles'] = max(0, self.totCycles - _totalComputeCycles)
        self.gStats.genesys_stats['Genesys']['memWaitCycles2tot_cycles'] = max(0, self.totCycles - _totalComputeCycles)/self.totCycles
        self.gStats.genesys_stats['Genesys']['computeCycles2tot_cycles'] = 1 - self.gStats.genesys_stats['Genesys']['memWaitCycles2tot_cycles']
        self.gStats.genesys_stats['Systolic'] = defaultdict(int)
        self.gStats.genesys_stats['Systolic']['systotalCycles'] = self.totSysComputeCycles
        #self.gStats.genesys_stats['Systolic']['systotalCycles'] = self.systolicResult[0][0] * self.decoder.numComputeTiles
        #self.gStats.genesys_stats['Systolic']['syscomputeCycle'] = self.systolicResult[0][1]
        self.gStats.genesys_stats['Systolic']['sysComputeCyclesPerTile'] = self.systolicResult[0][2]
        self.gStats.genesys_stats['Systolic']['sysLoadCyclesPerTile'] = self.systolicResult[0][3]
        self.gStats.genesys_stats['Systolic']['sysStoreCyclesPerTile'] = self.systolicResult[0][4]
        self.gStats.genesys_stats['Systolic']['perTileIbufUtil'] = self.systolicResult[0][5]
        self.gStats.genesys_stats['Systolic']['perTileObufUtil'] = self.systolicResult[0][6]
        self.gStats.genesys_stats['Systolic']['perTileWbufUtil'] = self.systolicResult[0][7]
        self.gStats.genesys_stats['Systolic']['perTileBbufUtil'] = self.systolicResult[0][8]
        self.gStats.genesys_stats['Systolic']['perTileComputeUtils'] = self.systolicResult[0][9]
        self.gStats.genesys_stats['Simd'] = defaultdict(int)
        ## SIMD outputs just 1 cycle since it uses load loops to detect number of tiles
        ## for genesys sim, multiple the per tile cycle with num_tiles here itself.
        ## for SIMD, it is fine and gives the correct cycles
        #print (f"here = {self.simdResult['cycle']} + {self.simdResult['StoreCycles']} * {self.decoder.numComputeTiles}")
        
        #self.gStats.genesys_stats['Simd']['simdtotalCycles'] = (self.simdResult['LoadCycles'] + self.simdResult['perTileCycles'] + self.simdResult['StoreCycles']) * self.decoder.numComputeTiles
        #self.gStats.genesys_stats['Simd']['simdtotalCycles'] = ((self.simdComputeCycles + self.simdStoreCycles) * self.decoder.numSIMDComputeTiles) + \
        #                                                    self.simdLoadCycles * max(self.decoder.numSIMDLoadTiles['VMEM1'],self.decoder.numSIMDLoadTiles['VMEM2'])
        #self.gStats.genesys_stats['Simd']['simdtotalCycles'] = ((self.simdComputeCycles + self.simdStoreCycles) * self.decoder.numSIMDComputeTiles) + \
        #                                                    self.simdLoadCycles * max(self.decoder.numSIMDLoadTiles['VMEM1'],self.decoder.numSIMDLoadTiles['VMEM2'])
        
        #self.gStats.genesys_stats['Simd']['simdtotalCycles'] = (self.simdResult['perTileCycles'] + self.simdResult['StoreCycles']) * self.decoder.numComputeTiles
        self.gStats.genesys_stats['Simd']['simdtotalCycles'] = self.totSIMDCycles
        self.gStats.genesys_stats['Simd']['simdComputeCyclesPerTile'] = self.simdResult['perTileCycles'] 
        self.gStats.genesys_stats['Simd']['simdLoadCycles'] = self.simdResult['LoadCycles']
        self.gStats.genesys_stats['Simd']['simdStoreCycles'] = self.simdResult['StoreCycles'] 
        self.gStats.genesys_stats['Simd']['NumComputeTiles'] = self.decoder.numSIMDComputeTiles
        self.gStats.genesys_stats['Simd']['VMEM1LoadTiles'] = self.decoder.numSIMDLoadTiles['VMEM1']
        self.gStats.genesys_stats['Simd']['VMEM2LoadTiles'] = self.decoder.numSIMDLoadTiles['VMEM2']
        self.gStats.genesys_stats['Simd']['StoreTiles'] = self.decoder.numSIMDComputeTiles
        self.gStats.genesys_stats['Simd']['StoreTilesNameSpace'] = self.decoder.SIMDStoreNameSpace 
        ## todo
        #self.gStats.genesys_stats['Simd']['perTileVMEM1Util'] = self.simdResult['perTileVMEM1Util'] 
        #self.gStats.genesys_stats['Simd']['perTileVMEM2Util'] = self.simdResult['perTileVMEM2Util'] 
        self.gStats.genesys_stats['Simd']['perTileVMEM1Util'] = None
        self.gStats.genesys_stats['Simd']['perTileVMEM2Util'] = None
        print ('\n In this functions here mode = ', mode)
        
        if 'energy' in mode:
            print ('here energy')
            self.get_energy()
        # print ("simdtotalCycles = ", self.simdResult['cycle'])
        # print ("simdLoadCyclesPerTile = ", self.simdResult['LoadCycles'] )
        # print ("simdStoreCyclesPerTile = ",  self.simdResult['StoreCycles'])
        # print ("perTileCycles  = ", self.simdResult['perTileCycles'] )
        # print ("tiles = ", self.decoder.numComputeTiles)

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
                                    _iterCount += 1
                                    _prevArr1DIndex = _arr1DIndex

        self.computeTile(0, _prevArr1DIndex, self.decoder.numComputeTiles)
        #One time addition on decoder overhead
        self.totCycles += self.decoder.decoderCycles
        
    def cycleGemm(self):
        _iterCount = 0
        _prevArr1DIndex = 0
        self.computeTile(0,_prevArr1DIndex, -1)
        # compute iters
        for b in range(self.decoder.tileDims['B']):
            for c in range(self.decoder.tileDims['C']):
                for m in range(self.decoder.tileDims['M']):
                    for n in range(self.decoder.tileDims['N']):
                        for p in range(self.decoder.tileDims['P']):
                            _arr1DIndex = get5Dto1DIndex(p, n, m, c, b, self.decoder.tileDims['N'], self.decoder.tileDims['M'], \
                            self.decoder.tileDims['C'], self.decoder.tileDims['B'])
                            #print ("\nIdx = ", _arr1DIndex)
                            self.computeTile(_arr1DIndex, _prevArr1DIndex, _iterCount)
                            _iterCount += 1
                            _prevArr1DIndex = _arr1DIndex

        self.computeTile(self.decoder.numComputeTiles-1, _prevArr1DIndex, self.decoder.numComputeTiles)
        #One time addition on decoder overhead
        self.totCycles += self.decoder.decoderCycles

    def cycle(self):
        if self.decoder.isGemmlayer:
            self.cycleGemm()
        else:
            self.cycleConv()

    ## Approximately add the load for only time when we do not have reuse
    ## If we had 100 tiles and 25 are reused 4 tiles, then we do not need to fetch 75 times.
    ## Given we have constant cycles for Systolic Compute and Systolic Load (this also depends on systolic reuse but ..)
    ## so here we add load for first 25 cycles and for the rest, we assume load cycles is 0
    def getSIMDCycles(self, tilenum):
        if tilenum < max(self.decoder.numSIMDLoadTiles['VMEM1'], self.decoder.numSIMDLoadTiles['VMEM2']):
            _simdload = self.simdLoadCycles
        else:
            _simdload = 0
        
        _simdCycles = _simdload + self.simdComputeCycles + self.simdStoreCycles
        return _simdCycles


    def computeTile(self, _arr1DIndex, _prevArr1DIndex, _iterCount):
        _computeCycles = 0
        _loadCycles = 0
        _sysComputeCycles = 0
        _simdComputeCycles = 0 
        _storeCycles = 0 
        _totSIMDcycles = 0
        #print ('arr = ', _arr1DIndex)
        if _iterCount == -1:
            _ibufLoadCycles = self.sysLoadCycles if self.decoder.ibufReuse[_arr1DIndex] == 0 else 0 
            _wbufLoadCycles = self.weightLoadCycles if self.decoder.wbufReuse[_arr1DIndex] == 0 else 0 
            # rohan: todo fix with a better memory model
            _totalCyclesThisIter = _ibufLoadCycles + _wbufLoadCycles
            _loadCycles = _ibufLoadCycles + _wbufLoadCycles
            #print ("Here 1 _totalCyclesThisIter", _totalCyclesThisIter, _ibufLoadCycles, _wbufLoadCycles, self.sysLoadCycles)
        elif _iterCount == 0:
            _ibufLoadCycles = self.sysLoadCycles if self.decoder.ibufReuse[_arr1DIndex+1] == 0 else 0 
            _wbufLoadCycles = self.weightLoadCycles if self.decoder.wbufReuse[_arr1DIndex+1] == 0 else 0 
            _computeCycles = self.sysComputeCycles
            _totalCyclesThisIter = max(_computeCycles, _ibufLoadCycles + _wbufLoadCycles)
            _loadCycles = _ibufLoadCycles + _wbufLoadCycles
            _sysComputeCycles = _computeCycles
            #print ("Here 2 _totalCyclesThisIter", _totalCyclesThisIter, "ibuf = ", _ibufLoadCycles,  'compute = ', _computeCycles)
        elif _iterCount == self.decoder.numComputeTiles - 1:
            _computeCycles = self.sysComputeCycles
            # todo: add reuse, if any

            _simdStoreCycles = self.getSIMDCycles(_arr1DIndex)
            _totalCyclesThisIter =  max(_computeCycles, _simdStoreCycles)
            _sysComputeCycles = _computeCycles
            _simdComputeCycles = self.simdComputeCycles
            _storeCycles = self.simdStoreCycles
            _totSIMDcycles = _simdStoreCycles

            #print ("Here 4 _totalCyclesThisIter", _totalCyclesThisIter, "_simdStoreCycles", _simdStoreCycles, "_sysComputeCycles", _sysComputeCycles )
        elif _iterCount == self.decoder.numComputeTiles:
            _simdStoreCycles = self.getSIMDCycles(_arr1DIndex)
            #print ("_simdStoreCycles = ", _simdStoreCycles)
            _totalCyclesThisIter = _simdStoreCycles
            #print ("Here 5 _totalCyclesThisIter", _totalCyclesThisIter)
            _simdComputeCycles = self.simdComputeCycles
            _storeCycles = self.simdStoreCycles
            _totSIMDcycles = _simdStoreCycles

        else:
            _ibufLoadCycles = self.sysLoadCycles if self.decoder.ibufReuse[_arr1DIndex + 1] == 0 else 0
            _wbufLoadCycles = self.weightLoadCycles if self.decoder.wbufReuse[_arr1DIndex + 1] == 0 else 0 
            _computeCycles = self.sysComputeCycles
            _simdStoreCycles = self.getSIMDCycles(_arr1DIndex)
            _totalCyclesThisIter = max(_computeCycles, _ibufLoadCycles + _wbufLoadCycles + _simdStoreCycles)
            _loadCycles = _ibufLoadCycles + _wbufLoadCycles
            _sysComputeCycles = _computeCycles
            _simdComputeCycles = self.simdComputeCycles
            _storeCycles = self.simdStoreCycles
            _totSIMDcycles = _simdStoreCycles
            #print ("Here 3 _totalCyclesThisIter", _totalCyclesThisIter, "_simdStoreCycles", _simdStoreCycles, "_wbufLoadCycles",_wbufLoadCycles , "_syscomputeCycles", _computeCycles, "simd compute ", _simdComputeCycles)
        
        self.perTileCycles.append(_totalCyclesThisIter)
        self.totCycles += math.ceil(_totalCyclesThisIter)
        #print ("tile cycles ===== ", math.ceil(_totalCyclesThisIter))
        #print ("total ===== ", self.totCycles)
        self.totLoadCycles += _loadCycles
        self.totSysComputeCycles += _sysComputeCycles
        self.totSimdComputeCycles += _simdComputeCycles
        self.totStoreCycles += _storeCycles
        self.totSIMDCycles += _totSIMDcycles


    def get_energy(self):
        sramModel = self.decoder.init_energy_model()
        print ('here 1 ' , type(self.simdBufAccesses))
        #print ('here 1 ', self.simdBufAccesses)
        if len(self.simdBufAccesses) > 0:
            vmem1 = True if self.simdBufAccesses['vmem1_read'] + self.simdBufAccesses['vmem1_write'] > 0 else False
        if len(self.simdBufAccesses) > 0:
            vmem2 = True if self.simdBufAccesses['vmem2_read'] + self.simdBufAccesses['vmem2_write'] > 0 else False

        
        if 'fused' in self.layerType:
            sramModel.get_ibuf_energy()
            sramModel.get_wbuf_energy()
            sramModel.get_bbuf_energy()
            sramModel.get_obuf_energy(self.layerType, self.simdBufAccesses['obuf'])
            # todo: if we have IC tiled in future, add obuf dram energy
            if vmem1:
                sramModel.get_vmem_energy(self.simdBufAccesses, self.simdResult, 'vmem1')
            if vmem2:
                sramModel.get_vmem_energy(self.simdBufAccesses, self.simdResult, 'vmem2')
            #sramModel.get_imm_energy(self.simdBufAccesses)
            syscomputeEnergy = self.decoder.systolic_energy
            simdcomputeEnergy = self.decoder.simd_energy_cost

        elif 'systolic' in self.layerType:
            sramModel.get_ibuf_energy()
            sramModel.get_wbuf_energy()
            sramModel.get_bbuf_energy()
            sramModel.get_obuf_energy(self.layerType, 0)
            syscomputeEnergy = self.decoder.systolic_energy
            simdcomputeEnergy = 0
            
        elif 'simd' in self.layerType:
            vmem1 = True if self.simdBufAccesses['vmem1_read'] + self.simdBufAccesses['vmem1_write'] > 0 else False
            vmem2 = True if self.simdBufAccesses['vmem2_read'] + self.simdBufAccesses['vmem2_write'] > 0 else False
            if vmem1:
                sramModel.get_vmem_energy(self.simdBufAccesses, self.simdResult, 'vmem1')
            if vmem2:
                sramModel.get_vmem_energy(self.simdBufAccesses, self.simdResult, 'vmem2')
            
            #sramModel.get_imm_energy(self.simdBufAccesses)
            syscomputeEnergy = 0
            simdcomputeEnergy = self.decoder.simd_energy_cost
            sramModel.get_obuf_energy(self.layerType, self.simdBufAccesses['obuf'])

        else:
            raise ValueError("Could not find layer type")
        ## Stats 
        self.compile_energy_stats(sramModel.sramStats)
    
    def compile_energy_stats(self, stats):
        self.gStats.genesys_stats['Energy'] = defaultdict(int)
        
        self.gStats.genesys_stats['Energy']['ibuf_numTile'] =  stats['ibuf']['numTiles']  
        self.gStats.genesys_stats['Energy']['ibuf_readEnergy'] =  stats['ibuf']['readEnergy']  
        #self.gStats.genesys_stats['Energy']['ibuf_writeEnergy'] =  stats['ibuf']['writeEnergy']  
        self.gStats.genesys_stats['Energy']['ibuf_leakPower'] =  stats['ibuf']['leakPower']  
        self.gStats.genesys_stats['Energy']['ibuf_area'] =  stats['ibuf']['area']  
        self.gStats.genesys_stats['Energy']['ibuf_perTileNumReads'] =  stats['ibuf']['perTileNumReads']  
        self.gStats.genesys_stats['Energy']['ibuf_perTileReadEnergy'] =  stats['ibuf']['perTileReadEnergy']  
        self.gStats.genesys_stats['Energy']['ibuf_totalReadEnergy'] = stats['ibuf']['perTileReadEnergy'] * self.decoder.numComputeTiles if \
            stats['ibuf']['perTileReadEnergy'] is not None else 0
        #self.gStats.genesys_stats['Energy']['ibuf_totalDataSizeBits'] =  stats['ibuf']['totalDataSizeBits']  
        self.gStats.genesys_stats['Energy']['ibuf_totalDDRReadEnergy'] =  stats['ibuf']['totalDDRReadEnergy']  
        
        self.gStats.genesys_stats['Energy']['wbuf_numTile'] =  stats['wbuf']['numTiles']  
        self.gStats.genesys_stats['Energy']['wbuf_readEnergy'] =  stats['wbuf']['readEnergy']  
        #self.gStats.genesys_stats['Energy']['wbuf_writeEnergy'] =  stats['wbuf']['writeEnergy']  
        self.gStats.genesys_stats['Energy']['wbuf_leakPower'] =  stats['wbuf']['leakPower']  
        self.gStats.genesys_stats['Energy']['wbuf_area'] =  stats['wbuf']['area']  
        self.gStats.genesys_stats['Energy']['wbuf_perTileNumReads'] =  stats['wbuf']['perTileNumReads']  
        self.gStats.genesys_stats['Energy']['wbuf_perTileReadEnergy'] =  stats['wbuf']['perTileReadEnergy']  
        self.gStats.genesys_stats['Energy']['wbuf_totalReadEnergy'] =  stats['wbuf']['perTileReadEnergy'] * self.decoder.numComputeTiles if\
            stats['wbuf']['perTileReadEnergy'] is not None else 0

        #self.gStats.genesys_stats['Energy']['wbuf_totalDataSizeBits'] =  stats['wbuf']['totalDataSizeBits']  
        self.gStats.genesys_stats['Energy']['wbuf_totalDDRReadEnergy'] =  stats['wbuf']['totalDDRReadEnergy']
        
        self.gStats.genesys_stats['Energy']['bbuf_numTile'] =  stats['bbuf']['numTiles']    
        self.gStats.genesys_stats['Energy']['bbuf_readEnergy'] =  stats['bbuf']['readEnergy']  
        #self.gStats.genesys_stats['Energy']['bbuf_writeEnergy'] =  stats['bbuf']['writeEnergy']  
        self.gStats.genesys_stats['Energy']['bbuf_leakPower'] =  stats['bbuf']['leakPower']  
        self.gStats.genesys_stats['Energy']['bbuf_area'] =  stats['bbuf']['area']  
        self.gStats.genesys_stats['Energy']['bbuf_perTileNumReads'] =  stats['bbuf']['perTileNumReads']  
        self.gStats.genesys_stats['Energy']['bbuf_perTileReadEnergy'] =  stats['bbuf']['perTileReadEnergy']  
        self.gStats.genesys_stats['Energy']['bbuf_totalReadEnergy'] =  stats['bbuf']['perTileReadEnergy']  * self.decoder.numComputeTiles if\
            stats['bbuf']['perTileReadEnergy'] is not None else 0
        #self.gStats.genesys_stats['Energy']['bbuf_totalDataSizeBits'] =  stats['bbuf']['totalDataSizeBits']  
        self.gStats.genesys_stats['Energy']['bbuf_totalDDRReadEnergy'] =  stats['bbuf']['totalDDRReadEnergy']  
        self.gStats.genesys_stats['Energy']['obuf_numTile'] =  stats['obuf']['numTiles']  
        self.gStats.genesys_stats['Energy']['obuf_readEnergy'] =  stats['obuf']['readEnergy']  
        self.gStats.genesys_stats['Energy']['obuf_writeEnergy'] =  stats['obuf']['writeEnergy']  
        self.gStats.genesys_stats['Energy']['obuf_leakPower'] =  stats['obuf']['leakPower']  
        self.gStats.genesys_stats['Energy']['obuf_area'] =  stats['obuf']['area']  
        self.gStats.genesys_stats['Energy']['obuf_perTileSysNumReads'] =  stats['obuf']['perTileSysNumReads']  
        self.gStats.genesys_stats['Energy']['obuf_perTileSysReadEnergy'] =  stats['obuf']['perTileSysReadEnergy']  
        self.gStats.genesys_stats['Energy']['obuf_perTileNumWrite'] =  stats['obuf']['perTileNumWrite']  
        self.gStats.genesys_stats['Energy']['obuf_perTileWriteEnergy'] =  stats['obuf']['perTileWriteEnergy']  
        #self.gStats.genesys_stats['Energy']['obuf_totalDataSizeBits'] =  stats['obuf']['totalDataSizeBits']  
        self.gStats.genesys_stats['Energy']['obuf_perTileSIMDNumReads'] =  stats['obuf']['perTileSIMDNumReads']  
        self.gStats.genesys_stats['Energy']['obuf_perTileSIMDReadEnergy'] =  stats['obuf']['perTileSIMDReadEnergy']  
        self.gStats.genesys_stats['Energy']['obuf_perTileTotalEnergy'] =  stats['obuf']['perTileSysReadEnergy'] + stats['obuf']['perTileWriteEnergy'] +\
                                                                          stats['obuf']['perTileSIMDReadEnergy']
        self.gStats.genesys_stats['Energy']['obuf_totalReadWriteEnergy'] = self.gStats.genesys_stats['Energy']['obuf_perTileTotalEnergy'] * self.decoder.numComputeTiles if\
            self.gStats.genesys_stats['Energy']['obuf_perTileTotalEnergy'] is not None else 0
        #self.gStats.genesys_stats['Energy']['obuf_perTileNumReads'] =  stats['obuf']['perTileNumReads']  
        #self.gStats.genesys_stats['Energy']['obuf_perTileReadEnergy'] =  stats['obuf']['perTileReadEnergy']  
        self.gStats.genesys_stats['Energy']['obuf_totalDDRWriteEnergy'] =  stats['obuf']['totalDDRWriteEnergy']  
        
        self.gStats.genesys_stats['Energy']['vmem1_numTile'] =  stats['vmem1']['numTiles']  
        self.gStats.genesys_stats['Energy']['vmem1_readEnergy'] =  stats['vmem1']['readEnergy']  
        self.gStats.genesys_stats['Energy']['vmem1_writeEnergy'] =  stats['vmem1']['writeEnergy']  
        self.gStats.genesys_stats['Energy']['vmem1_leakPower'] =  stats['vmem1']['leakPower']  
        self.gStats.genesys_stats['Energy']['vmem1_area'] =  stats['vmem1']['area']  
        self.gStats.genesys_stats['Energy']['vmem1_perTileNumReads'] =  stats['vmem1']['perTileNumReads']  
        self.gStats.genesys_stats['Energy']['vmem1_perTileReadEnergy'] =  stats['vmem1']['perTileReadEnergy']  
        self.gStats.genesys_stats['Energy']['vmem1_perTileNumWrites'] =  stats['vmem1']['perTileNumWrites']  
        self.gStats.genesys_stats['Energy']['vmem1_perTileWriteEnergy'] =  stats['vmem1']['perTileWriteEnergy']  
        self.gStats.genesys_stats['Energy']['vmem1_totalReadDataSizeBits'] =  stats['vmem1']['totalReadDataSizeBits']  
        self.gStats.genesys_stats['Energy']['vmem1_totalDDRReadEnergy'] =  stats['vmem1']['totalDDRReadEnergy']  
        self.gStats.genesys_stats['Energy']['vmem1_totalWriteDataSizeBits'] =  stats['vmem1']['totalWriteDataSizeBits']  
        self.gStats.genesys_stats['Energy']['vmem1_totalDDRWriteEnergy'] =  stats['vmem1']['totalDDRWriteEnergy']  
        
        self.gStats.genesys_stats['Energy']['vmem2_numTile'] =  stats['vmem2']['numTiles']  
        self.gStats.genesys_stats['Energy']['vmem2_readEnergy'] =  stats['vmem2']['readEnergy']  
        self.gStats.genesys_stats['Energy']['vmem2_writeEnergy'] =  stats['vmem2']['writeEnergy']  
        self.gStats.genesys_stats['Energy']['vmem2_leakPower'] =  stats['vmem2']['leakPower']  
        self.gStats.genesys_stats['Energy']['vmem2_area'] =  stats['vmem2']['area']  
        self.gStats.genesys_stats['Energy']['vmem2_perTileNumReads'] =  stats['vmem2']['perTileNumReads']  
        self.gStats.genesys_stats['Energy']['vmem2_perTileReadEnergy'] =  stats['vmem2']['perTileReadEnergy']  
        self.gStats.genesys_stats['Energy']['vmem2_perTileNumWrites'] =  stats['vmem2']['perTileNumWrites']  
        self.gStats.genesys_stats['Energy']['vmem2_perTileWriteEnergy'] =  stats['vmem2']['perTileWriteEnergy']  
        self.gStats.genesys_stats['Energy']['vmem2_totalReadDataSizeBits'] =  stats['vmem2']['totalReadDataSizeBits']  
        self.gStats.genesys_stats['Energy']['vmem2_totalDDRReadEnergy'] =  stats['vmem2']['totalDDRReadEnergy']  
        self.gStats.genesys_stats['Energy']['vmem2_totalWriteDataSizeBits'] =  stats['vmem2']['totalWriteDataSizeBits']  
        self.gStats.genesys_stats['Energy']['vmem2_totalDDRWriteEnergy'] =  stats['vmem2']['totalDDRWriteEnergy']  