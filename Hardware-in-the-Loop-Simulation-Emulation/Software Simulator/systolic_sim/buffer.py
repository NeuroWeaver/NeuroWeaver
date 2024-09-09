from collections import defaultdict
import math


class buffer():
    """
        Base Class to Model an on-chip buffer
    """
    def __init__(self, compute, infLatency, bankDepth, numBanks, bitwidth, perAccessReadEnergy, perAccessWriteEnergy, \
                tileDims, numTiles, bufName, numComputeTiles, latency, freq, infwidth = 512, infBandwidth = 3e9, numTags = 2, tileSize = None) -> None:
        self.bitsinByte = 8
        self.intLatency = latency
        # class objects
        self.compute = compute
        # buffer params
        self.bufName = bufName
        self.infwidth = infwidth
        self.infBandwidth = infBandwidth
        self.infLatency = infLatency
        self.freq = freq
        self.bankDepth = bankDepth
        self.numBanks = numBanks
        self.bitwidth = bitwidth
        self.numTags = numTags
        self.computeTag = True
        self.loadTag = True
        self.nextLoadTag = False
        #print (self.loadTag, self.nextLoadTag )
        self.storeTag = True
        self.nextStoreTag = False
        self.tagReady = [0 for i in range(self.numTags)]
        self.tagReuse = [0 for i in range(self.numTags)]
        self.tagBusy = [0 for i in range(self.numTags)]
        self.perAccessReadEnergy = perAccessReadEnergy
        self.perAccessWriteEnergy = perAccessWriteEnergy
        

        # tile params
        #self.DDRDims = DDRDims
        self.tileDims = tileDims
        if tileSize is None:
            self.tileSize = self.computeTileSize()
        else:
            self.tileSize = tileSize
            self.IbuftileSize = self.computeTileSize()
        self.numTiles = numTiles
        self.numComputeTiles = numComputeTiles

        # Stats
        
        if tileSize is None:
            self.bankUtilization = self.getBankUtilization(self.tileSize)
        else:
            self.bankUtilization = self.getBankUtilization(self.IbuftileSize)
        
        self.perTileCycles = self.getperTileCycles()
        self.totalCycle = 0
        self.numSystolicReadsPerTile = self.tileSize/(self.bitwidth/self.bitsinByte)    ## Equal to number of elements in the tile
        self.numSystolicWritesPerTile = self.tileSize/(self.bitwidth/self.bitsinByte)
        self.numDDRReadsPerTile = self.tileSize/self.infwidth
        self.numDDRWritesPerTile = self.tileSize/self.infwidth
        self.perTileDDRReadEnergy = self.getperTileDDRReadEnergy()
        self.perTileDDRWriteEnergy = self.getperTileDDRWriteEnergy()
        self.perTileDDREnergy = self.getperTileDDREnergy()
        self.totalDDREnergy = self.numTiles * self.perTileDDREnergy # ideally (numLoadTiles +  numStoreTiles) * self.perTileDDREnergy
        self.perTileSystolicReadEnergy = self.getperTileSystolicReadEnergy()
        self.perTileSystolicWriteEnergy = self.getperTileSystolicWriteEnergy()
        self.perTileSystolicEnergy = self.getperTileSystolicEnergy()
        self.totalSystolicEnergy = self.numComputeTiles * self.perTileSystolicEnergy
        self.totalEnergy = self.totalDDREnergy + self.totalSystolicEnergy

    def computeTileSize(self):
        _tsize = 1
        for k,v in self.tileDims.items():
            _tsize *= v
        _tsize *= (self.bitwidth/self.bitsinByte) if len(self.tileDims) != 0 else 0
        return _tsize  # in bytes

    def getperTileCycles(self):
        ## todo: add ML model to introduce uncertaity
        #print (f"lat: {self.intLatency}, tileSize = {self.tileSize}, bw =  {self.infBandwidth})")
        #print (f"lat: {self.intLatency}, div = {self.tileSize/self.infBandwidth})")
        #print ("In buffer = ", self.tileSize, self.infBandwidth, math.ceil((self.tileSize/self.infBandwidth)/(self.freq * 1e-9)))
        return math.ceil((self.tileSize/self.infBandwidth)/(self.freq * 1e-9))

    def getperTileDDRReadEnergy(self):
        ## todo: Check if we need to multiple by numBanks, we do I guess because each DDR read is sent to each bank?
        return ( self.numDDRReadsPerTile * self.perAccessReadEnergy * self.numBanks)

    def getperTileDDRWriteEnergy(self):
        return ( self.numDDRWritesPerTile * self.perAccessWriteEnergy * self.numBanks)
    
    def getperTileDDREnergy(self):
        return (self.perTileDDRReadEnergy + self.perTileDDRWriteEnergy)
    
    def getperTileSystolicReadEnergy(self):
        return (self.numSystolicReadsPerTile * self.perAccessReadEnergy * self.numBanks)

    def getperTileSystolicWriteEnergy(self):
        return (self.numSystolicWritesPerTile * self.perAccessWriteEnergy *  self.numBanks)

    def getperTileSystolicEnergy(self):
        return (self.perTileSystolicReadEnergy + self.perTileSystolicWriteEnergy)

    # todo: Is this okay or change this to account for stall?
    def cycle(self):
        return self.perTileCycles

    def getBankUtilization(self, _tileSize = 1024):
            #print ("Here ", _tileSize, self.numBanks, self.bankDepth, (((_tileSize*1.0/self.numBanks))/self.bankDepth) * 100)
            return (((_tileSize*1.0/self.numBanks))/self.bankDepth) * 100
    

## Load/Store method takes 0 cycles if there is a reuse else it takes time, therefore it has buffer specific implementation

class ibuf(buffer):
    def __init__(self, decoder, compute, bufName = 'IBUF') -> None:
        super().__init__(compute, decoder.infLatency, decoder.IBUFBankDepth, decoder.IBUFNumBanks, decoder.IBUFbitwidth, \
            decoder.IBUFperAccessReadEnergy, decoder.IBUFperAccessWriteEnergy, decoder.IBUFtileDims, \
                decoder.IBUFnumTiles, bufName , decoder.numComputeTiles, decoder.infLatency, decoder.freq, decoder.IBUFinfwidth, decoder.IBUFinfBandwidth, decoder.numTags, decoder.totalInputBufSize)
        self.bufName = bufName
        self.decoder = decoder

    def updatedCycle(self, _tileSize):
        return(_tileSize/self.infBandwidth)
        
    def load(self, arr1DIndex):
        _totMemLatency = 0
        # to count how many times we are adding 
        cnt = 0
        #print ("initially time = ", _totMemLatency)

        if self.decoder.ibufReuse[arr1DIndex] == 0:
            self.nextLoadTag = not self.loadTag
            #print ("At IBUF 0 : ", not self.loadTag)
            #print ("At IBUF 1: ", self.loadTag, self.nextLoadTag)
            #print (f"ibuf tile size = {self.decoder.IBUFTileSize}")
            assert (self.nextLoadTag != self.compute.ibufComputeTag), "Load and Compute Tag cannot be same for IBUF!'"
            _totMemLatency +=  self.updatedCycle(self.decoder.IBUFTileSize)
            #print (f"ibuf: tile size {self.decoder.IBUFTileSize} time =  {_totMemLatency}")
        else: 
            _totMemLatency += 0
        
        if self.decoder.wbufReuse[arr1DIndex] == 0:
            self.nextLoadTag = not self.loadTag
            #print (f"wbuf tile size = {self.decoder.WBUFTileSize}")

            assert (self.nextLoadTag != self.compute.wbufComputeTag), "Load and Compute Tag cannot be same for WBUF!'"
            _totMemLatency +=  self.updatedCycle(self.decoder.WBUFTileSize)
            #print (f"wbuf: tile size {self.decoder.WBUFTileSize} time =  {_totMemLatency}")

        
        else: 
            _totMemLatency += 0
        
        if self.decoder.bbufReuse[arr1DIndex] == 0:
            self.nextLoadTag = not self.loadTag
            #print (f"bbuf tile size = {self.decoder.BBUFTileSize}")

            assert (self.nextLoadTag != self.compute.bbufComputeTag), "Load and Compute Tag cannot be same for BBUF!'"
            _totMemLatency +=  self.updatedCycle(self.decoder.BBUFTileSize)
            #print (f"bbuf: tile size {self.decoder.BBUFTileSize} time =  {_totMemLatency}")

        
        else: 
            _totMemLatency += 0
        ## todo: change this so that we can use it for any frequency. Right now its for 200MHz
        _totMemLatency = (_totMemLatency*1.0)/5e-9
        #print (f"_totMemLatency = {_totMemLatency}\n")
        
        #print ("total Cycles = ", _totMemLatency, '\n')

        return math.ceil(_totMemLatency + self.intLatency)
        
    
    def updateLoadTag(self, arr1DIndex):
        if self.decoder.ibufReuse[arr1DIndex] == 0:
            self.loadTag = not self.nextLoadTag

class obuf(buffer):
    def __init__(self, decoder, compute, bufName = 'OBUF') -> None:
        super().__init__(compute, decoder.infLatency, decoder.OBUFBankDepth, decoder.OBUFNumBanks, decoder.OBUFbitwidth, \
            decoder.OBUFperAccessReadEnergy, decoder.OBUFperAccessWriteEnergy, decoder.OBUFtileDims, \
                decoder.OBUFnumTiles, bufName , decoder.numComputeTiles, decoder.infLatency, decoder.freq, decoder.OBUFinfwidth, decoder.OBUFinfBandwidth, decoder.numTags)
        self.bufName = bufName
        self.decoder = decoder


    def load(self, arr1DIndex):
        
        if self.decoder.obufReuse[arr1DIndex] == 0:
            self.nextLoadTag = not self.loadTag
            assert (self.nextLoadTag != self.compute.obufComputeTag), "Load and Compute Tag cannot be same for f{self.bufName}!"
            return self.cycle()
        else: 
            return 0
    def store(self, arr1DIndex):
       
        if self.decoder.obufReuse[arr1DIndex] == 0:
            self.nextStoreTag = not self.storeTag
            assert (self.nextStoreTag != self.compute.obufComputeTag), "Store and Compute Tag cannot be same for f{self.bufName}!"
            #print (f"here obuf {self.cycle()} + {self.infLatency}")
            #return (self.cycle() + self.infLatency)
            return self.cycle() + + self.intLatency ## We do not add the latency as we account for the ibuf
        else: 
            #print (f"here obuf ")
            return 0
    
    def updateStoreTag(self, arr1DIndex):
        if self.decoder.obufReuse[arr1DIndex] == 0:
            self.storeTag = not self.nextStoreTag
             

class wbuf(buffer):
    def __init__(self, decoder, compute, bufName = 'WBUF') -> None:
        super().__init__(compute, decoder.infLatency, decoder.WBUFBankDepth, decoder.WBUFNumBanks, decoder.WBUFbitwidth, \
            decoder.WBUFperAccessReadEnergy, decoder.WBUFperAccessWriteEnergy, decoder.WBUFtileDims, \
                decoder.WBUFnumTiles, bufName , decoder.numComputeTiles, decoder.infLatency, decoder.freq, decoder.WBUFinfwidth, decoder.WBUFinfBandwidth, decoder.numTags)
        self.bufName = bufName
        self.decoder = decoder

    def load(self, arr1DIndex):
        if self.decoder.wbufReuse[arr1DIndex] == 0:
            self.nextLoadTag = not self.loadTag
            assert (self.nextLoadTag != self.compute.wbufComputeTag), "Load and Compute Tag cannot be same for f{self.bufName}!"
            #print ("here ======", self.cycle(), self.decoder.WBUFtileDims)
            return self.cycle() + + self.intLatency
        else: 
            return 0
    
    def updateLoadTag(self, arr1DIndex):
        if self.decoder.wbufReuse[arr1DIndex] == 0:
            self.loadTag = not self.nextLoadTag

class bbuf(buffer):
    def __init__(self, decoder, compute, bufName = 'BBUF') -> None:
        super().__init__(compute, decoder.infLatency, decoder.BBUFBankDepth, decoder.BBUFNumBanks, decoder.BBUFbitwidth, \
            decoder.BBUFperAccessReadEnergy, decoder.BBUFperAccessWriteEnergy, decoder.BBUFtileDims, \
                decoder.BBUFnumTiles, bufName , decoder.numComputeTiles, decoder.infLatency, decoder.freq, decoder.BBUFinfwidth, decoder.BBUFinfBandwidth, decoder.numTags)
        self.bufName = bufName
        self.decoder = decoder

    def load(self, arr1DIndex):
        if self.decoder.bbufReuse[arr1DIndex] == 0:
            self.nextLoadTag = not self.loadTag
            assert (self.nextLoadTag != self.compute.bbufComputeTag), "Load and Compute Tag cannot be same for f{self.bufName}!"
            return self.cycle() + + self.intLatency
        else: 
            return 0

    def updateLoadTag(self, arr1DIndex):
        if self.decoder.bbufReuse[arr1DIndex] == 0:
            self.loadTag = not self.nextLoadTag
