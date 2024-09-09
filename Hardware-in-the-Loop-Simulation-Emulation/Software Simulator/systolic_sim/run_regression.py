from collections import defaultdict
import os
import sys
import string
import csv
import numpy as np
import systolic_sim
import pandas

csv8x8 = defaultdict(int)
csv16x16 = defaultdict(int)
csv32x32 = defaultdict(int)

def fpga_stats():
    fn = ['8x8csv.csv', '16x16csv.csv', '32x32csv.csv']
    global csv8x8  
    global csv16x16  
    global csv32x32  

    with open(fn[0], 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if 'test name' in row[0]:
                pass
            else:
                csv8x8[row[0].lower()] = row[1] 
    with open(fn[1], 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if 'test name' in row[0]:
                pass
            else:
                csv16x16[row[0].lower()] = row[1] 
    with open(fn[2], 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if 'test name' in row[0]:
                pass
            else:
                csv32x32[row[0].lower()] = row[1] 

def main():
    global csv8x8  
    global csv16x16  
    global csv32x32  

    results = [["layerName", "DDRTiling", "IBUFTiling", "WBUFTiling", "BBUFTiling", \
               "OBUFTiling", "NumTiles", "stride", "pad", "arrayN", "arrayM", "memBandwidth", \
               "memLatency", "ibufDepth", "obufDepth", "wbufDepth", "bbufDepth", \
               "freq", "totalCycles", "computeCycle", "MemWaitCycle", \
                "totalTime", "perTileIbufUtil", "perTileObufUtil", \
                "perTileWbufUtil", "perTileBbufUtil", "perTileComputeUtils", "compute2total%"]]
        
    perCycle = ['Per Tile Cycle']
    assert(len(sys.argv) == 4), 'Usage python3 run_regression.py <regression_directory_path> output_file_name sys_config'
    regDir = sys.argv[1]
    cmd = "python3 systolic_sim.py"
    for _, dirs, _ in os.walk(regDir):
        for d in dirs:
            sysInst = systolic_sim.main(os.path.join(regDir,d))
            results.append(sysInst.stat)  
            perCycle.append(sysInst.perCycle)  
    
    #print (np.asarray(results).shape)
    #resultsDF = pandas.DataFrame(results, columns=results[0])
    #perCycleDF = pandas.DataFrame(perCycle)
    
   
    #print (perCycle)

    fpga_stats()

    #for d in range(len(results[1:])):
    #    print(results[d+1][0])

    switch = int(sys.argv[3]) # 0 for 8x8, 1 for 16x16, 2 for 32x32
    if switch == 0:
        refDict = csv8x8
    elif switch == 1:
        refDict = csv16x16
    else:
        refDict = csv32x32

    #print (refDict)

    newRes = []
    for i in range(len(results)):
        if i == 0:
            newData = results[i]
            newData.append("FPGA Cycles")
            newData.append("Diff wrt FPGA")
            newRes.append(newData)
        else:
            newData = results[i]
            fpga_ref = int(refDict[results[i][0]])
            if results[i][18] == 0:
                compute2tot = 'na'
            else:
                compute2tot = (results[i][19] * 100.0 )/results[i][18]
            newData.append(compute2tot)
            newData.append(fpga_ref)
            newData.append(((results[i][18] - fpga_ref) * 100)/results[i][18])
            newRes.append(newData)
    
  
    outputfile = sys.argv[2]
    f = open(outputfile, 'w')
    writer = csv.writer(f)
    for row in newRes:
        writer.writerow(row)
    f.close()
    
if __name__ == "__main__":
    main()


