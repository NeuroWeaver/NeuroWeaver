from cacti_sweep import *
from collections import defaultdict
from energy_model.buffer_energy import buffer_energy

class sram_energy:
    def __init__(self, dram_cost, sysNumComputeLoops, tech_node = 45, ibuf = None, obuf = None, wbuf = None, bbuf = None, vmem = None, \
                 simdComputeTile=0, simdDDRLdTiles=0, simdDDRStTile = 0, simdStoreNameSpace='vmem1') -> None:
        self.dram_cost = dram_cost
        self.sysNumComputeLoops = sysNumComputeLoops
        #self.numTiles = numTiles
        self.ibuf = ibuf
        self.obuf = obuf
        self.wbuf = wbuf
        self.bbuf = bbuf
        self.vmem = vmem
        self.simdComputeTile = simdComputeTile
        self.simdDDRLdTiles = simdDDRLdTiles
        self.simdDDRStTile = simdDDRStTile
        self.simdStoreNameSpace = simdStoreNameSpace.lower()
        tech_node = tech_node
        sram_opt_dict = {'technology (u)': tech_node*1.e-3}
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../sram')
        self.sram_obj = CactiSweep(
                bin_file=os.path.join(dir_path, 'cacti/cacti'),
                csv_file=os.path.join(dir_path, 'cacti_sweep.csv'),
                default_json=os.path.join(dir_path, 'default.json'),
                default_dict=sram_opt_dict)
        self.sramStats = defaultdict(str)
        self.init_stats()

    def init_stats(self):
        self.sramStats['ibuf'] = {}
        self.sramStats['ibuf']['numTiles'] = None
        self.sramStats['ibuf']['readEnergy'] = None
        self.sramStats['ibuf']['writeEnergy'] = None
        self.sramStats['ibuf']['leakPower'] = None
        self.sramStats['ibuf']['area'] = None
        self.sramStats['ibuf']['perTileNumReads'] = None
        self.sramStats['ibuf']['perTileReadEnergy'] = None
        self.sramStats['ibuf']['totalDataSizeBits'] = None
        self.sramStats['ibuf']['totalDDRReadEnergy'] = None

        self.sramStats['wbuf'] = {}
        self.sramStats['wbuf']['numTiles'] = None
        self.sramStats['wbuf']['readEnergy'] = None
        self.sramStats['wbuf']['writeEnergy'] = None
        self.sramStats['wbuf']['leakPower'] = None
        self.sramStats['wbuf']['area'] = None
        self.sramStats['wbuf']['perTileNumReads'] = None
        self.sramStats['wbuf']['perTileReadEnergy'] = None
        self.sramStats['wbuf']['totalDataSizeBits'] = None
        self.sramStats['wbuf']['totalDDRReadEnergy'] = None
        
        self.sramStats['bbuf'] = {}
        self.sramStats['bbuf']['numTiles'] = None
        self.sramStats['bbuf']['readEnergy'] = None
        self.sramStats['bbuf']['writeEnergy'] = None
        self.sramStats['bbuf']['leakPower'] = None
        self.sramStats['bbuf']['area'] = None
        self.sramStats['bbuf']['perTileNumReads'] = None
        self.sramStats['bbuf']['perTileReadEnergy'] = None
        self.sramStats['bbuf']['totalDataSizeBits'] = None
        self.sramStats['bbuf']['totalDDRReadEnergy'] = None

        self.sramStats['obuf'] = {}
        self.sramStats['obuf']['numTiles'] = None
        self.sramStats['obuf']['readEnergy'] = None
        self.sramStats['obuf']['writeEnergy'] = None
        self.sramStats['obuf']['leakPower'] = None
        self.sramStats['obuf']['area'] = None
        self.sramStats['obuf']['perTileSysNumReads'] = 0
        self.sramStats['obuf']['perTileSysReadEnergy'] = 0
        self.sramStats['obuf']['perTileNumWrite'] = None
        self.sramStats['obuf']['perTileWriteEnergy'] = None
        self.sramStats['obuf']['totalDataSizeBits'] = None
        self.sramStats['obuf']['totalDDRWriteEnergy'] = None
        self.sramStats['obuf']['perTileSIMDNumReads'] = 0
        self.sramStats['obuf']['perTileSIMDReadEnergy'] = 0
        self.sramStats['obuf']['perTileNumReads'] = None
        self.sramStats['obuf']['perTileReadEnergy'] = None

        self.sramStats['vmem1'] = {}
        self.sramStats['vmem1']['numTiles'] = None
        self.sramStats['vmem1']['readEnergy'] = None
        self.sramStats['vmem1']['writeEnergy'] = None
        self.sramStats['vmem1']['leakPower'] = None
        self.sramStats['vmem1']['area'] = None
        self.sramStats['vmem1']['totalNumReads'] = None
        self.sramStats['vmem1']['totalReadEnergy'] = None
        self.sramStats['vmem1']['totalNumWrites'] = None
        self.sramStats['vmem1']['totalWriteEnergy'] = None
        self.sramStats['vmem1']['totalReadDataSizeBits'] = None
        self.sramStats['vmem1']['totalDDRReadEnergy'] = None
        self.sramStats['vmem1']['totalWriteDataSizeBits'] = None
        self.sramStats['vmem1']['totalDDRWriteEnergy'] = None

        self.sramStats['vmem2'] = {}
        self.sramStats['vmem2']['numTiles'] = None
        self.sramStats['vmem2']['readEnergy'] = None
        self.sramStats['vmem2']['writeEnergy'] = None
        self.sramStats['vmem2']['leakPower'] = None
        self.sramStats['vmem2']['area'] = None
        self.sramStats['vmem2']['totalNumReads'] = None
        self.sramStats['vmem2']['totalReadEnergy'] = None
        self.sramStats['vmem2']['totalNumWrites'] = None
        self.sramStats['vmem2']['totalWriteEnergy'] = None
        self.sramStats['vmem2']['totalReadDataSizeBits'] = None
        self.sramStats['vmem2']['totalDDRReadEnergy'] = None
        self.sramStats['vmem2']['totalWriteDataSizeBits'] = None
        self.sramStats['vmem2']['totalDDRWriteEnergy'] = None

    def get_ibuf_energy(self):
        ibufStats = {}
        ibufReuseList = self.ibuf['reuseList']
        ibufBanks = self.ibuf['banks']
        ibufBankDepth = self.ibuf['bankDepth']
        ibufDataWidth = self.ibuf['dataWidth']
        ibufTileSize = self.ibuf['tileSize']
        ibufEnergyModel  = buffer_energy(self.sram_obj, self.dram_cost, self.sysNumComputeLoops, ibufReuseList, \
                            ibufBanks, ibufBankDepth, ibufDataWidth, ibufTileSize)
        print("i")
        self.sramStats['ibuf']['readEnergy'], self.sramStats['ibuf']['writeEnergy'], self.sramStats['ibuf']['leakPower'], \
                            self.sramStats['ibuf']['area'] = ibufEnergyModel.get_energy_costs()
        self.sramStats['ibuf']['perTileNumReads'], self.sramStats['ibuf']['perTileReadEnergy'] = ibufEnergyModel.compute_read_energy()
        self.sramStats['ibuf']['numTiles'], self.sramStats['ibuf']['totalDataSizeBits'], self.sramStats['ibuf']['totalDDRReadEnergy'] = ibufEnergyModel.dram_read_energy()
        
        
    def get_obuf_energy(self, layerType, numSIMDReads):
        #obufStats = {}
        obufReuseList = self.obuf['reuseList']
        obufBanks = self.obuf['banks']
        obufBankDepth = self.obuf['bankDepth']
        obufDataWidth = self.obuf['dataWidth']
        obufTileSize = self.obuf['tileSize']
        obufEnergyModel  = buffer_energy(self.sram_obj, self.dram_cost, self.sysNumComputeLoops, obufReuseList, \
                            obufBanks, obufBankDepth, obufDataWidth, obufTileSize)
        print("o")
        self.sramStats['obuf']['readEnergy'], self.sramStats['obuf']['writeEnergy'], self.sramStats['obuf']['leakPower'], \
                            self.sramStats['obuf']['area'] = obufEnergyModel.get_energy_costs()
        if 'systolic' in layerType:
            self.sramStats['obuf']['perTileSysNumReads'], self.sramStats['obuf']['perTileSysReadEnergy'] = obufEnergyModel.compute_read_energy()
            self.sramStats['obuf']['perTileNumWrite'], self.sramStats['obuf']['perTileWriteEnergy'] = obufEnergyModel.compute_write_energy()
            self.sramStats['obuf']['numTiles'], self.sramStats['obuf']['totalDataSizeBits'], self.sramStats['obuf']['totalDDRWriteEnergy'] = obufEnergyModel.dram_write_energy()
            self.sramStats['obuf']['perTileSIMDNumReads'], self.sramStats['obuf']['perTileSIMDReadEnergy'] = 0,0
            self.sramStats['obuf']['perTileNumReads'] = self.sramStats['obuf']['perTileSysNumReads'] + self.sramStats['obuf']['perTileSIMDNumReads']
            self.sramStats['obuf']['perTileReadEnergy'] = self.sramStats['obuf']['perTileSysReadEnergy'] + self.sramStats['obuf']['perTileSIMDReadEnergy']

        elif 'fused' in layerType:
            self.sramStats['obuf']['perTileSysNumReads'], self.sramStats['obuf']['perTileSysReadEnergy'] = obufEnergyModel.compute_read_energy()
            self.sramStats['obuf']['perTileNumWrite'], self.sramStats['obuf']['perTileWriteEnergy'] = obufEnergyModel.compute_write_energy()
            self.sramStats['obuf']['perTileSIMDNumReads'], self.sramStats['obuf']['perTileSIMDReadEnergy'] = obufEnergyModel.compute_read_energy_v2(numSIMDReads)
            self.sramStats['obuf']['perTileNumReads'] = self.sramStats['obuf']['perTileSysNumReads'] + self.sramStats['obuf']['perTileSIMDNumReads']
            self.sramStats['obuf']['perTileReadEnergy'] = self.sramStats['obuf']['perTileSysReadEnergy'] + self.sramStats['obuf']['perTileSIMDReadEnergy']
            
        else:
            self.sramStats['obuf']['perTileSysNumReads'], self.sramStats['obuf']['perTileSysReadEnergy'] = 0,0
            self.sramStats['obuf']['perTileNumWrite'], self.sramStats['obuf']['perTileWriteEnergy'] = 0,0
            self.sramStats['obuf']['perTileSIMDNumReads'], self.sramStats['obuf']['perTileSIMDReadEnergy'] = obufEnergyModel.compute_read_energy_v2(numSIMDReads)
            self.sramStats['obuf']['perTileNumReads'] = self.sramStats['obuf']['perTileSysNumReads'] + self.sramStats['obuf']['perTileSIMDNumReads']
            self.sramStats['obuf']['perTileReadEnergy'] = self.sramStats['obuf']['perTileSysReadEnergy'] + self.sramStats['obuf']['perTileSIMDReadEnergy']         
               
    def get_wbuf_energy(self):
        wbufReuseList = self.wbuf['reuseList']
        wbufBanks = self.wbuf['banks']
        wbufBankDepth = self.wbuf['bankDepth']
        wbufDataWidth = self.wbuf['dataWidth']
        wbufTileSize = self.wbuf['tileSize']
        wbufEnergyModel  = buffer_energy(self.sram_obj, self.dram_cost, self.sysNumComputeLoops, wbufReuseList, \
                            wbufBanks, wbufBankDepth, wbufDataWidth, wbufTileSize)
        print("w")
        self.sramStats['wbuf']['readEnergy'], self.sramStats['wbuf']['writeEnergy'], self.sramStats['wbuf']['leakPower'], \
                            self.sramStats['wbuf']['area'] = wbufEnergyModel.get_energy_costs()
        
        self.sramStats['wbuf']['perTileNumReads'], self.sramStats['wbuf']['perTileReadEnergy'] = wbufEnergyModel.compute_read_energy()
        self.sramStats['wbuf']['numTiles'], self.sramStats['wbuf']['totalDataSizeBits'], self.sramStats['wbuf']['totalDDRReadEnergy'] = wbufEnergyModel.dram_read_energy()
        
    def get_bbuf_energy(self):
        bbufReuseList = self.bbuf['reuseList']
        bbufBanks = self.bbuf['banks']
        bbufBankDepth = self.bbuf['bankDepth']
        bbufDataWidth = self.bbuf['dataWidth']
        bbufTileSize = self.bbuf['tileSize']
        bbufEnergyModel  = buffer_energy(self.sram_obj, self.dram_cost, self.sysNumComputeLoops, bbufReuseList, \
                            bbufBanks, bbufBankDepth, bbufDataWidth, bbufTileSize)
        print("b")
        self.sramStats['bbuf']['readEnergy'], self.sramStats['bbuf']['writeEnergy'], self.sramStats['bbuf']['leakPower'], \
                            self.sramStats['bbuf']['area'] = bbufEnergyModel.get_energy_costs()

        self.sramStats['bbuf']['perTileNumReads'], self.sramStats['bbuf']['perTileReadEnergy'] = bbufEnergyModel.compute_read_energy()
        self.sramStats['bbuf']['numTiles'], self.sramStats['bbuf']['totalDataSizeBits'], self.sramStats['bbuf']['totalDDRReadEnergy'] = bbufEnergyModel.dram_read_energy()
       
    
    def get_vmem_energy(self, bufAccess, simdResult, vmem = 'vmem1'):
        if vmem == "vmem1":
            ldTileSize = simdResult['ddrLoadTileSizeVmem1']
            ldTileCycles = simdResult['ddrLoadCycleVmem1']
            simdDDRLdTile = self.simdDDRLdTiles['vmem1']
        else:
            ldTileSize = simdResult['ddrLoadTileSizeVmem2']
            ldTileCycles = simdResult['ddrLoadCycleVmem2']
            simdDDRLdTile = self.simdDDRLdTiles['vmem2']

        stTileSize = simdResult['storeTileSize']
        numComputeReads = bufAccess[f"{vmem}_computeRead"]
        numComputeWrites = bufAccess[f"{vmem}_computeWrite"]

        numLdWrites = bufAccess[f"{vmem}_ldWrite"] / 2   # Test run shows that the per tile st reads get counted twice
        numStReads = bufAccess[f"{vmem}_stRead"] / 2    # Test run shows that the per tile st reads get counted twice
        
        vmemReuseList = {}
        vmemBanks = self.vmem['banks']
        vmemBankDepth = self.vmem['bankDepth']
        vmemDataWidth = self.vmem['dataWidth']
        vmemTileSize = self.vmem['tileSize']

        # print(f"----------------------------- {vmem} BUFFER STATS -----------------------------")
        
        vmemEnergyModel  = buffer_energy(self.sram_obj, self.dram_cost, self.sysNumComputeLoops, vmemReuseList, \
                            vmemBanks, vmemBankDepth, vmemDataWidth, vmemTileSize, 'simd', simdDDRLdTile, self.simdDDRStTile, self.simdComputeTile, ldTileSize, stTileSize)
        print("v")
        self.sramStats[vmem]['readEnergy'], self.sramStats[vmem]['writeEnergy'], self.sramStats[vmem]['leakPower'], \
                            self.sramStats[vmem]['area'] = vmemEnergyModel.get_energy_costs()

        ### VMEM onchip numbers
        #print(vmem, self.simdDDRStTile, self.simdComputeTile, numComputeReads, numStReads)
        self.sramStats[vmem]['totalNumReads'], self.sramStats[vmem]['totalReadEnergy'] = vmemEnergyModel.compute_read_energy_vmem(self.simdDDRStTile, self.simdComputeTile, numComputeReads, numStReads)
        #print(vmem, self.simdDDRStTile, self.simdComputeTile, numComputeWrites, numLdWrites)
        self.sramStats[vmem]['totalNumWrites'], self.sramStats[vmem]['totalWriteEnergy'] = vmemEnergyModel.compute_write_energy_vmem(self.simdDDRStTile, self.simdComputeTile, numComputeWrites, numLdWrites)

        ### DDR Numbers 
        if ldTileCycles > 0:
            self.sramStats[vmem]['numTiles'], self.sramStats[vmem]['totalReadDataSizeBits'], self.sramStats[vmem]['totalDDRReadEnergy'] = vmemEnergyModel.dram_read_energy()
        
        if vmem == self.simdStoreNameSpace:            
            self.sramStats[vmem]['numTiles'], self.sramStats[vmem]['totalWriteDataSizeBits'], self.sramStats[vmem]['totalDDRWriteEnergy'] = vmemEnergyModel.dram_write_energy()
