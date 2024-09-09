
import json
import numpy as np
import sys


def extract_bits(value: int, num_bits: int, pos: int):
    return ((((1 << num_bits) - 1) << pos) & value) >> pos

    
def write_file(arr, ofp):
    for v in arr:
        ofp.write(str(v))
        ofp.write("\n")



if len(sys.argv) < 1:
    print("Usage: input_32bit_file, output_file_name")

data_file = sys.argv[1]



output_file = sys.argv[2]
ofp = open(output_file,"w")
o_array = []
with open(data_file) as f:
    for l in f:
        dec_val = int(l)
        for d in range(4):
            o_array.append(extract_bits(dec_val, 8, d*8))

write_file(o_array, ofp)