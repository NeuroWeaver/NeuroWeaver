import os
import getopt, sys
import re
from os.path import exists
import os.path
from os import path
import json
from subprocess import call
argumentList = sys.argv[1:]
# Options
options = "d:c:" 
# Long options
long_options = ["dir", "config"]
arguments, values = getopt.getopt(argumentList,options, long_options)

directory=""
config=""
for currentArgument, currentValue in arguments:
    if currentArgument in ("-d" , "--dir"):
        directory = currentValue
    elif currentArgument in ("-c", "--config"):
        config = currentValue

#directory = "/home/lavanya/testcases/resnet50_32x32_tests/"

test_list = []

f = open("host/regression_config_SA.h", "x")

first=1
last=""

for root, dirs, files in os.walk(directory):
    for dirname in dirs:
        for root1, dirs1, files1 in os.walk(root+"/"+dirname):
            for filename in files1:
                if "decimal.txt" in filename:
                    if (first):
                        f.write("#ifdef "+re.sub("-", "_", dirname.upper())+"\n")
                    else :
                        f.write("#elif "+re.sub("-", "_", dirname.upper())+"\n")
                    test_list.append(re.sub("-", "_", dirname.upper())) 

                    f.write("     std::string instruction_file  = \""+root1+"/"+filename+"\";"+"\n")
                    if (first):
                        last=last+"     std::string instruction_file  = \""+root1+"/"+filename+"\";"+"\n"
                
                    f_buf_filename = re.sub("decimal.txt", "json.json", filename)
                    f_buf = open(root1+'/'+f_buf_filename)
                    data_buf = json.load(f_buf)

                    f_dat = open(root1+'/data/data_locations.json')
                    data = json.load(f_dat)
                    path_list = [0,0,0,0,0,0] 

                    for i in data_buf["program"][0]["inputs"] :
                        unique_name = i["unique_name"]
                        if (len(i["data_path"])>1):
                            buffer = i["data_path"][1]
                        else:
                            buffer = "IBUF"

                        
                        if (buffer == "IBUF"):
                            path = root1+"/data/"+unique_name+"/"+unique_name+"_shuffled.txt"
                            path_list[0] = 1
                            f.write("     std::string input_file  = \""+path+"\";"+"\n")
                            if (first):
                                last=last+"   std::string input_file  = \""+path+"\";"+"\n"
                        
                        elif (buffer == "WBUF"):
                            path = root1+"/data/"+unique_name+"/"+unique_name+"_shuffled.txt" 
                            path_list[1] = 1
                            f.write("     std::string weight_file  = \""+path+"\";"+"\n")
                            if (first):
                                last=last+"   std::string weight_file  = \""+path+"\";"+"\n"
                        
                        elif (buffer == "BBUF"):
                            path = root1+"/data/"+unique_name+".txt"
                            path_list[2] = 1
                            f.write("     std::string bias_file  = \""+path+"\";"+"\n")
                            if (first):
                                last=last+"   std::string bias_file  = \""+path+"\";"+"\n"
                        
                        elif (buffer == "VMEM1"):
                            path = root1+"/data/"+unique_name+".txt"
                            path_list[3] = 1
                            f.write("     std::string simd_input_file1  = \""+path+"\";"+"\n")
                            if (first):
                                last=last+"   std::string simd_input_file1  = \""+path+"\";"+"\n"
                        
                        elif (buffer == "VMEM2"):
                            path = root1+"/data/"+unique_name+".txt"
                            path_list[4] = 1
                            f.write("     std::string simd_input_file2  = \""+path+"\";"+"\n")
                            if (first):
                                last=last+"   std::string simd_input_file2  = \""+path+"\";"+"\n"

                    for i in data_buf["program"][0]["outputs"] :
                        unique_name = i["unique_name"]
                        if (len(i["data_path"])>1):
                            buffer = i["data_path"][-2]
                        else:
                            buffer = "OBUF"

                            # if (buffer == "OBUF"):
                        path = root1+"/data/"+unique_name+".txt"
                        path_list[5] = 1
                        f.write("     std::string output_file  = \""+path+"\";"+"\n")
                        if (first):
                            last=last+"   std::string output_file  = \""+path+"\";"+"\n"
                    
                    if (path_list[0] == 0):
                        f.write("     std::string input_file  = \"\";"+"\n")
                        if (first):
                            last=last+"   std::string input_file  = \"\";"+"\n"

                    if (path_list[1] == 0):
                        f.write("     std::string weight_file  = \"\";"+"\n")
                        if (first):
                            last=last+"   std::string weight_file  = \"\";"+"\n"

                    if (path_list[2] == 0):
                        f.write("     std::string bias_file  = \"\";"+"\n")
                        if (first):
                            last=last+"   std::string bias_file  = \"\";"+"\n"

                    if (path_list[3] == 0):
                        f.write("     std::string simd_input_file1  = \"\";"+"\n")
                        if (first):
                            last=last+"   std::string simd_input_file1  = \"\";"+"\n"

                    if (path_list[4] == 0):
                        f.write("     std::string simd_input_file2  = \"\";"+"\n")
                        if (first):
                            last=last+"   std::string simd_input_file2  = \"\";"+"\n" 
                    
                    if (path_list[5] == 0):
                        f.write("     std::string output_file  = \"\";"+"\n")
                        if (first):
                            last=last+"   std::string output_file  = \"\";"+"\n" 

                    first=0

                    f.write("/**************/\n")
                    first=0
            
            break

f.write("#else\n")
f.write(last)
f.write("#endif\n")

f.close()

directory = os.getcwd()
target_dir = ''
log_dir = 'emu_logs'
csv_file='metrics.csv'
platform = 'xilinx_u280_xdma_201920_1'

def start():
    global target_dir
    print ("Compiling Regression Tests for Systolic Array") 
    target_dir = "bin_SA_16x16"
    target_path = directory + "/" + target_dir
    print ("Creating executable at ")
    print (target_path)
    clean()
    os.mkdir(target_path)
    compile_regression_list()
    run_regression()
    generate_csv()

def compile_regression_list():
    global test_list
    print ("test_list is ")
    print (test_list)
    for test_name in test_list:
        cmd = 'make build_sw TARGET_DIR=' + target_dir + ' TEST_NAME=' + test_name
        print (cmd)
        os.system(cmd)

def run_regression():
    log_fn = "_log.txt"
 #   setup_cmd = 'export XCL_EMULATION_MODE=hw_emu'
 #   os.environ['XCL_EMULATION_MODE'] = 'hw_emu'
 #   print(setup_cmd)
 #   em_config_cmd = 'emconfigutil --platform '+platform
 #   os.system(em_config_cmd)
 #   em_cp_cmd = 'cp emconfig.json '+target_dir+'/'
 #   os.system(em_cp_cmd)
    os.mkdir(log_dir)
 #   print(em_config_cmd)
    for i in range(len(test_list)):
        reprog_cmd = './vadd krnl_vadd.xclbin'
        os.system(reprog_cmd)
        cmd = target_dir+'/'+test_list[i]+' > '+log_dir+'/'+test_list[i]+log_fn
        os.system(cmd)


def generate_csv():
    file_out = open(log_dir+"/"+csv_file,"a")
    file_out.write("TESTCASE,INPUT_TRANSFER_TIME (sec),INPUT_TRANSFER_CYCLES,EXECUTION_TIME (sec),EXECUTION_CYCLES,OUTPUT_TRANSFER_TIME (sec),OUTPUT_TRANSFER_CYCLES,RESULT\n")
    for root, dirs, files in os.walk(log_dir):
        for filename in files:
            if ((".txt" in filename) and ~("swp" in filename)):
                print(root+"/"+filename)
                logfl = open(root+"/"+filename,"r")
                entry = ""
                entry = entry+filename

                for line in logfl:
                    if ("TEST PASSED" in line):
                        entry = entry+",TEST PASSED"
                    elif ("TEST FAILED" in line):
                        entry = entry+",TEST FAILED"
                    elif ("Input Transfer Time" in line):
                        val = line.split(':')[-1]
                        val = val.split('\n')[0]
                        entry = entry+","+val
                    elif ("Input Transfer Cycles" in line):
                        val = line.split(':')[-1]
                        val = val.split('\n')[0]
                        entry = entry+","+val
                    elif ("Execution Time" in line):
                        val = line.split(':')[-1]
                        val = val.split('\n')[0]
                        entry = entry+","+val
                    elif ("Execution Cycles" in line):
                        val = line.split(':')[-1]
                        val = val.split('\n')[0]
                        entry = entry+","+val
                    elif ("Output Transfer Time" in line):
                        val = line.split(':')[-1]
                        val = val.split('\n')[0]
                        entry = entry+","+val
                    elif ("Output Transfer Cycles" in line):
                        val = line.split(':')[-1]
                        val = val.split('\n')[0]
                        entry = entry+","+val
                logfl.close()
                file_out.write(entry+"\n")
        file_out.close()




    
    for test_name in test_list:
        cmd = 'make build_sw TARGET_DIR=' + target_dir + ' TEST_NAME=' + test_name
        print (cmd)
        os.system(cmd)


def clean():
    msg = 'Deleting '+target_dir+' '+log_dir
    print(msg)
    clean_cmd = 'rm -rf '+target_dir+' '+log_dir
    os.system(clean_cmd)
    print(clean_cmd)

if __name__ == "__main__":
    start()



# print(test_list)
                        
                        

