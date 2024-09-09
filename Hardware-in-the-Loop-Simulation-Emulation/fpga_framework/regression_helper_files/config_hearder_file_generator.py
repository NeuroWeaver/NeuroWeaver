import os

dir_list = os.listdir('/home/rohan/genesys-merged-repo/testcases/')
path = "/home/rohan/genesys-merged-repo/testcases/"
f = open("regression_config.h", "w")

instr_fn = "resnet50_1_conv_decimal.txt"
bias_fn = "bias.txt"
weights_fn = "weights_shuffled.txt"
inputs_fn = "input_shuffled.txt"
outputs_fn = "output.txt"

instr_def = "std::string instruction_file  = "   
output_def = "std::string output_file       = " 
input_def = "std::string input_file        = " 
weight_def = "std::string weight_file       = "  
bias_def = "std::string bias_file         = "  



for i in range(len(dir_list)):
    if i == 0:
        define = '#ifdef '+ dir_list[i]
    else:
        define = '#elif '+ dir_list[i]

    finstr = instr_def + "\'" + path + dir_list[i] + '/' +  instr_fn + "\';"
    fbias = bias_def + "\'" + path + dir_list[i] + '/' + bias_fn + "\';" 
    fweights = weight_def + "\'" + path + dir_list[i] + '/' + weights_fn + "\';"
    finputs = input_def + "\'" + path + dir_list[i] + '/' + inputs_fn + "\';"
    foutputs = output_def + "\'" + path + dir_list[i] + '/' + outputs_fn + "\';"
    f.write("/**************/")
    f.write("\n")
    f.write(define)
    f.write("\n")
    f.write(finstr)
    f.write("\n")
    f.write(finputs)
    f.write("\n")
    f.write(fbias)
    f.write("\n")
    f.write(fweights)
    f.write("\n")
    f.write(foutputs)
    f.write("\n")
    

define = '#else '
finstr = instr_def + "\'" + path + dir_list[0] + '/' +  instr_fn + "\';"
fbias = bias_def + "\'" + path + dir_list[0] + '/' + bias_fn + "\';" 
fweights = weight_def + "\'" + path + dir_list[0] + '/' + weights_fn + "\';"
finputs = input_def + "\'" + path + dir_list[0] + '/' + inputs_fn + "\';"
foutputs = output_def + "\'" + path + dir_list[0] + '/' + outputs_fn + "\';"
f.write("/**************/")
f.write("\n")
f.write(define)
f.write("\n")
f.write(finstr)
f.write("\n")
f.write(finputs)
f.write("\n")
f.write(fbias)
f.write("\n")
f.write(fweights)
f.write("\n")
f.write(foutputs)
f.write("\n")
f.write('#endif')

f.close()