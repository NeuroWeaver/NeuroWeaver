import os
from systolic_sim.utils import *
from math import *

class buffer_energy:
    '''
        Inputs: 
            Takes in cacti instance, and gets per access energy
            Takes in buffer instance, to get the banks, depth, data width etc.
            Takes in compute_loops_iters and reuse pattern of buffer
        Outputs:
            Total Num accesses
            Per access energy
            Per tile energy
            total energy
            Area
    '''
    def __init__(self, sram_obj, dram_cost, numComputeLoops, reuseList, banks, bankDepth, dataWidth, \
                 tileSize, bufLoc = 'systolic', numSIMDLdTile=1, numSIMDStTile = 1, numSIMDComputeTiles = 1, simdTileLdSize = 0, simdTileStSize = 0) -> None:
        self.sram_obj = sram_obj
        self.dram_cost = dram_cost
        self.numComputeLoops = numComputeLoops
        self.reuseList = reuseList
        self.banks = banks
        self.bankDepth = bankDepth
        self.dataWidth = dataWidth
        if 'simd' in bufLoc: 
            self.tileLdSize = simdTileLdSize
            self.tileStSize = simdTileStSize
            self.numLdTiles = numSIMDLdTile
            self.numStTiles = numSIMDStTile
            self.numComputeTiles = numSIMDComputeTiles
        else:
            self.tileLdSize = tileSize
            self.tileStSize = tileSize
            # DEBUGGGGGGGG
            # MIGHT NOT BE CORRECT FOR SYSTOLIC
            self.numLdTiles = sum(self.reuseList)
            self.numStTiles = sum(self.reuseList)
            self.numComputeTiles = sum(self.reuseList)
        
    def get_energy_costs(self):
        sram_bits = self.dataWidth
        tot_sram_bank = self.banks
        tot_sram_size = tot_sram_bank * self.bankDepth * sram_bits * 8
        num_sram_word = ceil_a_by_b(tot_sram_size, tot_sram_bank * sram_bits)
        sram_bank_size = num_sram_word * sram_bits
        assert sram_bank_size * tot_sram_bank == tot_sram_size
      
        cfg_dict = {'size (bytes)': sram_bank_size /8., 'block size (bytes)': sram_bits/8., 'read-write port': 0}
        #cfg_dict = {'size (bytes)': 1024., 'block size (bytes)': 4., 'read-write port': 0}
        sram_data = self.sram_obj.get_data_clean(cfg_dict)
        # print(sram_data['access_time_ns']/sram_bits)
        self.sram_read_energy = float(sram_data['read_energy_nJ']) / sram_bits
        self.sram_write_energy = float(sram_data['write_energy_nJ']) / sram_bits
        self.sram_leak_power = float(sram_data['leak_power_mW']) * tot_sram_bank
        self.sram_area = float(sram_data['area_mm^2']) * tot_sram_bank
        return self.sram_read_energy, self.sram_write_energy, self.sram_leak_power, self.sram_area

    def compute_read_energy(self):
        perTileNumReads = self.numComputeLoops * self.banks * self.dataWidth
        perTileReadEnergy = perTileNumReads * self.sram_read_energy
        return perTileNumReads, perTileReadEnergy
    
    def compute_read_energy_v2(self, numAccess):
        perTileNumReads = numAccess * self.dataWidth * self.banks
        perTileReadEnergy = perTileNumReads * self.sram_read_energy
        return perTileNumReads, perTileReadEnergy
    
    def compute_read_energy_vmem(self, simdDDRStTile, simdComputeTile, numComputeReads, numStReads):
        computeReads = simdComputeTile * numComputeReads * self.dataWidth  # read is in bit
        stReads = simdDDRStTile * numStReads * self.dataWidth
        totalNumReads = computeReads + stReads
        totalReadEnergy = totalNumReads * self.sram_read_energy

        # print("----VMEM read----")
        # print("Compute Read Tiles: ", simdComputeTile)
        # print("Compute Read per Tile: ", numComputeReads)
        # print("stRead Tiles: ", simdDDRStTile)
        # print("stRead per Tile: ", numStReads)
        
        return totalNumReads, totalReadEnergy
    
    def compute_write_energy(self):
        perTileNumWrite = self.numComputeLoops * self.banks * self.dataWidth
        perTileWriteEnergy = perTileNumWrite * self.sram_write_energy
        return perTileNumWrite, perTileWriteEnergy
        
    def compute_write_energy_v2(self, numAccess):
        perTileNumWrite = numAccess * self.dataWidth * self.banks
        perTileWriteEnergy = perTileNumWrite * self.sram_write_energy
        return perTileNumWrite, perTileWriteEnergy
    
    def compute_write_energy_vmem(self, simdDDRLdTile, simdComputeTile, numComputeWrites, numLdWrites):
        computeWrite = simdComputeTile * numComputeWrites * self.dataWidth
        ldWrite = simdDDRLdTile * numLdWrites * self.dataWidth
        totalNumWrite = computeWrite + ldWrite
        totalWriteEnergy = totalNumWrite * self.sram_write_energy

        # print("----VMEM write----")
        # print("Compute Write Tiles: ", simdComputeTile)
        # print("Compute Write per Tile: ", numComputeWrites)
        # print("load Write Tiles : ", simdDDRLdTile)
        # print("load Write per Tile : ", numLdWrites)

        return totalNumWrite, totalWriteEnergy
    
    ## This won't work for OBUF if it has to load partial sums because the reuse list might be different
    ## todo: account for case when IC is tiled
    def dram_read_energy(self):
        # print("----DDR----")
        # print("DRAM Read Num Tile ", self.numLdTiles)
        # print("DRAM Read Tile Size ", self.tileLdSize)

        totalDataSizeBits = self.tileLdSize * self.numLdTiles * self.dataWidth
        totalDDRReadEnergy = totalDataSizeBits * self.dram_cost
        return self.numLdTiles, totalDataSizeBits, totalDDRReadEnergy

    def dram_write_energy(self):
        # print("----DDR----")
        # print("DRAM Write Num Tile ", self.numStTiles)
        # print("DRAM Write Tile Size ", self.tileStSize)

        totalDataSizeBits = self.tileStSize * self.numStTiles * self.dataWidth # tileStSize = total number of data to be stored
        totalDDRWriteEnergy = totalDataSizeBits * self.dram_cost
        return self.numStTiles, totalDataSizeBits, totalDDRWriteEnergy
        
    

