from email.policy import default
import string
from functools import partial
import multiprocessing as mp
from genesysCompute import *
from genesysDecoder import *
from genesysDecoderGEMM import *
from genesysStats import *
from systolic_sim.utils import *
from pathlib import Path
CWD = Path(f"{__file__}").parent
CALLPATH = Path(f"{os.getcwd()}")
import argparse

import sys

# sys.path.insert(0, "/home/rohan/genesysSim/")

class GeneSys:

    def run(self, decoder, gStats, testPath, layerType, mode):
       
        self.stats = None
        genesys = genesysCompute(decoder, gStats, testPath)
        if 'systolic' in layerType:
            systolic_inst = genesys.systolic_sim(mode)
            #print (f"Simulating Layer: {decoder.layerName}")
        elif 'simd' in layerType:
            simd_inst = genesys.simd_sim(mode)
            #print (f"Simulating Layer: {decoder.layerName}")
        elif 'fused' in layerType:
            genesys_inst = genesys.genesys_sim(layerType, mode)
            #print (f"Simulating Layer: {decoder.layerName}")
        else:
            raise ValueError(f"Invalid Layer\n")


results = []

def getLayerType(_testPath):
    layer = {} 
    _instrPath = findFile(_testPath, '*string_final.txt')
    with open(_instrPath, 'r') as f:
        for line in f:
            if "SYSTOLIC_ARRAY" in line:
                layer['systolic'] = True
            if "SIMD" in line:
                layer['simd'] = True
    if len(layer) == 2:
        return 'fused'
    elif len(layer) == 1:
        return list(layer.keys())[0]
    else:    
        raise ValueError("Could not find layer type")

def print_stats(x):
    if 'fused' in x['Compiler']['layerType']:
        tot_cycles = x['Genesys']['totCycles']
        compute_2_total_cycles = x['Genesys']['computeCycles2tot_cycles']
    elif 'systolic' in x['Compiler']['layerType']:
        tot_cycles = x['Systolic']['systotalCycles']
        compute_2_total_cycles = x['Systolic']['syscomputeCycle']/x['Systolic']['systotalCycles']
    elif 'simd' in x['Compiler']['layerType']:
        tot_cycles = x['Simd']['simdtotalCycles']
        compute_2_total_cycles = 'NA'
    else:
        raise ValueError("Could not find layer type")
    Freq = x['Arch']['freq']
    Layer_Name = x['Compiler']['layerName']
    Layer_Type = x['Compiler']['layerType']
    Arch =x ['Arch']['arrayN']
    Total_Cycles = tot_cycles
    Total_Time = x['Genesys']['totTime(us)']
    Compute2TotalCycles = compute_2_total_cycles
    
    #print (f"{x['Compiler']['layerName']:30} | {x['Compiler']['layerType']:4} |\
    #       {x['Arch']['arrayN']:4} | {tot_cycles:4} | {x['Genesys']['totTime']:4} | {compute_2_total_cycles:4} ")
    print('{:30s} {:15s} {:8s} {:10s} {:15s} {:15s} {:25s}'.format(Layer_Name, Layer_Type, str(Arch), str(Freq), str(Total_Cycles), str(Total_Time), str(Compute2TotalCycles)))
  
def run_tests(configPath, testPath, mode):
    global results
    x = ''
    #print (f"Layer_Name{x:30s} |  Layer_Type{x:4s} | Arch{x:4s} | Total_Cycles{x:4s} | Total_Time{x:4s} | Compute2TotalCycles{x:4s} ")
    #print('\n{:30s} {:15s} {:8s} {:10s} {:15s} {:15s} {:25s}'.format('Layer_Name', 'Layer_Type', 'Arch', 'Freq(Mhz)', 'Total_Cycles', 'Total_Time(us)', 'Compute2TotalCycles'))
    if not os.path.exists(testPath):
        raise RuntimeError(f"Path for {testPath} does not exist!")
    for _, dirs, _ in os.walk(testPath):
        total_tests = len(dirs)
        cnt = 0
        for d in dirs:
            cnt += 1
            _testPath = os.path.join(testPath,d)
            if 'data' in _testPath:
                continue
            if 'layer' in _testPath:
                _len = get_instr_size(_testPath)
                if _len < 20:
                    continue
                layerType = getLayerType(_testPath)
                if 'fused' in layerType:
                    extract_simd_instr(_testPath)
                #print (f'Test Name: {d}   |   Layer Type: {layerType}')
                print (f'\n ***** {cnt}/{total_tests} - Test Name: {d} ******, Layer Type = {layerType}')
                gStats = Genesys_Stats()
                isGemm = isGemmLayer(_testPath)
                if isGemm == True:
                    decoder = GenesysDecoderGEMM(configPath, _testPath, gStats, layerType)
                else:
                    decoder = GenesysDecoder(configPath, _testPath, gStats, layerType)
                decoder.cycle()
                genesys_obj = GeneSys()
                genesys_obj.run(decoder, gStats, _testPath, layerType, mode)
                results.append(gStats.genesys_stats)

def isGemmLayer(_testpath):
    _fPath = findFile(_testpath, '*json.json')
   
    with open(_fPath) as fp:
        _data = json.load(fp)
        if "matmul" in _data['program'][0]['operation'] or "gemm" in _data['program'][0]['operation']:
           return True
    return False

def get_instr_size(_testpath):
    _fPath = findFile(_testpath, '*_string_final.txt')
    # print (_fPath)
    with open(_fPath) as fp:
        instrList = fp.read().splitlines()
    return len(instrList)

      
def extract_simd_instr(_testPath):
    lookup = 'SYNC_INST SIMD, START'
    lnum = 0
    _fn_new = ''
    _bfn_new = ''
    for fname in os.listdir(_testPath):
        if fname.endswith("_string_final.txt"):
            _fn = os.path.join(_testPath,fname)
            _fn_new = _fn.split('.txt')[0]
            _fn_new = _fn_new + '_SIMD.txt'
            with open(_fn) as myFile:
                stringList = myFile.read().splitlines()
                for num, line in enumerate(stringList, 0):
                    if lookup in line:
                        lnum = num
           
        if fname.endswith("_binary.txt"):
            _bfn = os.path.join(_testPath,fname)
            _bfn_new = _bfn.split('.txt')[0]
            _bfn_new = _bfn_new + '_SIMD.txt'
            with open(_bfn) as myFile1:
                binaryList = myFile1.read().splitlines()
        
        if fname.endswith("_decimal.txt"):
            _dfn = os.path.join(_testPath,fname)
            _dfn_new = _dfn.split('.txt')[0]
            _dfn_new = _dfn_new + '_SIMD.txt'
            with open(_dfn) as myFile2:
                decimalList = myFile2.read().splitlines()
            
    simdf1 = open(_fn_new, 'w')
    simdf2 = open(_bfn_new, 'w')
    simdf3 = open(_dfn_new, 'w')
    stringList_new = stringList[lnum:]
    binaryList_new = binaryList[lnum:]
    decimalList_new = decimalList[lnum:]
    
    for item in stringList_new:
        simdf1.write("%s\n" % item)
    for item in binaryList_new:
        simdf2.write("%s\n" % item)
    for item in decimalList_new:
        simdf3.write("%s\n" % item)
    
def extractHeadings(result):
    metric_dict = {}
    highLevelp = list(result.keys())
    compilerp = list(result['Compiler'].keys())
    archp = list(result['Arch'].keys())
    genesysp = list(result['Genesys'].keys())
    systolicp = list(result['Systolic'].keys())
    simdp = list(result['Simd'].keys())
    energyd = list(result['Energy'].keys())

    metric_dict[highLevelp[0]] = compilerp
    metric_dict[highLevelp[1]] = archp
    metric_dict[highLevelp[2]] = genesysp
    metric_dict[highLevelp[3]] = systolicp
    metric_dict[highLevelp[4]] = simdp
    metric_dict[highLevelp[5]] = energyd


    row0 = [highLevelp[0]]
    row1 = [''] * (len(compilerp) - 1)
    row2 = [highLevelp[1]]
    row3 = [''] * (len(archp) - 1)
    row4 = [highLevelp[2]]
    row5 = [''] * (len(genesysp) - 1)
    row6 = [highLevelp[3]]
    row7 = [''] * (len(systolicp) - 1)
    row8 = [highLevelp[4]]
    row9 = [''] * (len(simdp) - 1)     
    row10 = [highLevelp[5]]
    row11 = [''] * (len(energyd) - 1)     

    row10 = row0 + row1 + row2 + row3 + row4 + row5 + row6 + row7 + row8 + row9 + row10 + row11
    # row10 = row0 + row1 + row2 + row3 + row4 + row5 + row6 + row7 + row8 + row9
    row11 = compilerp + archp + genesysp + systolicp + simdp + energyd
    # row11 = compilerp + archp + genesysp + systolicp + simdp
    
    return metric_dict, row10, row11


def extractRow(metric_dict, result):
    row = []    
    for k,v in metric_dict.items():
        for val in metric_dict[k]:
            #print (f"{k} [ {val} ]")
            row.append(result[k][val])
            #print (f"{result[k][val]}")

    return row

def generateCSV(resultsList, logFile):
    f = open(logFile, 'w')
    writer = csv.writer(f)
    metric_dict, highLevelp_expand, metrics = extractHeadings(resultsList[0])
    writer.writerow(highLevelp_expand)
    writer.writerow(metrics)

    for i in range(len(resultsList)):
        row = extractRow(metric_dict, resultsList[i])
        writer.writerow(row)

    f.close()

def extract_csv_stats(results):
    csv_stats = []
    metric_dict, highLevelp_expand, metrics = extractHeadings(results[0])
    csv_stats.append(highLevelp_expand)
    csv_stats.append(metrics)
    for i in range(len(results)):
        row = extractRow(metric_dict, results[i])
        csv_stats.append(row)
    return csv_stats

def main(configPath, testPath, logFile=None, mode='perf'):
    global results

    if not logFile:
        logFile = f"{CALLPATH}/test/{Path(testPath).name}.csv"
    run_tests(configPath, testPath, mode)
    generateCSV(results, logFile)

def run_single_test(config, mode, test_info):
    cnt = 0
    results = []
    for d in os.scandir(test_info['path']):
        if not d.is_dir() or "layer" not in d.name:
            continue
        cnt += 1
        layer_path = d.path
        if get_instr_size(layer_path) < 20:
            continue
        layer_type = getLayerType(layer_path)
        if 'fused' in layer_type:
            extract_simd_instr(layer_path)
        gen_stats = Genesys_Stats()

        if isGemmLayer(layer_path) == True:
            decoder = GenesysDecoderGEMM(config, layer_path, gen_stats, layer_type)
        else:
            decoder = GenesysDecoder(config, layer_path, gen_stats, layer_type)
        decoder.cycle()
        genesys_obj = GeneSys()
        genesys_obj.run(decoder, gen_stats, layer_path, layer_type, mode)
        results.append(gen_stats.genesys_stats)

    if len(results) > 1:
        return extract_csv_stats(results)
    else:
        return []

def run_multi_tests(test_root, config_path, mode, debug_mode=False):

    if not os.path.exists(test_root):
        raise RuntimeError(f"Path for {test_root} does not exist!")

    test_info = []
    for dir in os.scandir(test_root):
        if dir.is_dir():
            for f in os.scandir(dir.path):
                if f.is_file() and Path(f.path).suffix == ".json":
                    info_blob = {"name": dir.name, "path": dir.path}
                    test_info.append(info_blob)
                    break
    #

    if debug_mode:
        print(f"Performing simulations in debug mode for {[ib['name'] for ib in test_info]}")
        all_results = []
        for test_blob in test_info:
            results = run_single_test(config_path, mode, test_blob)
            all_results.append(results)
    else:
        print(f"Performing multi-threaded simulations for {[ib['name'] for ib in test_info]}")
        test_pool = mp.Pool()
        all_results = test_pool.map(partial(run_single_test, config_path, mode), test_info)

    result_dir = f"{test_root}/sim_results"
    if os.path.exists(result_dir):
        idx = 0
        while os.path.exists(f"{test_root}/sim_results{idx}"):
            idx += 1
        result_dir = f"{test_root}/sim_results{idx}"
    print(f"Storing results in {result_dir}")
    try:
        os.makedirs(result_dir)
    except OSError as e:
        raise RuntimeError(f"Creation of directory {result_dir} failed:\n {e}")


    for i, tdir in enumerate(test_info):
        test_results = all_results[i]
        log_file = f"{result_dir}/{tdir['name']}.csv"
        with open(log_file, 'w') as f:
            writer = csv.writer(f)
            for row in test_results:
                writer.writerow(row)

if __name__ == "__main__":
    if sys.stdin and sys.stdin.isatty():
        parser = argparse.ArgumentParser(description="Simulate benchmarks")
        parser.add_argument('config',type=str, help="path to config.")
        parser.add_argument('test_path', type=str, help="path to tests.")
        parser.add_argument('--mode', type=str, help="Simulation mode.", default="perf")
        parser.add_argument('--log_path', type=str, help="Logfile name.", default=None)
        parser.add_argument('--multi_test', help="Run multiple tests or a single.", action="store_true")
        # config_path = sys.argv[1]
        # test_path = sys.argv[2]
        # mode = sys.argv[3] if len(sys.argv) >= 5 else 'perf'
        args = parser.parse_args()
        #test_path = f"{CALLPATH}/{args.test_path}"
        test_path = args.test_path
        config_path = f"{CALLPATH}/{args.config}"
        if args.log_path is not None:
            log_path = f"{CALLPATH}/{args.log_path}"
        else:
            log_path = None
        mode = args.mode
        run_multi = args.multi_test

        if run_multi:
            run_multi_tests(test_path, config_path, mode, debug_mode=False)
        else:
            main(config_path, test_path, logFile=log_path, mode=mode)
    else:
        config_path = f"{CWD}/../configs/"
        test_path = f"{CWD}/../testdir/testbench_dir/"
        mode = 'perf'
        run_multi_tests(test_path, config_path, mode, debug_mode=False)

