from collections import defaultdict
import numpy as np


params_depth = 16384
inputs_depth = 128 
outputs_depth = 128
bias_depth = 128

buffers = {"parameters":params_depth, "inputs":inputs_depth, "outputs":outputs_depth, "bias":bias_depth}
memories = defaultdict(list)

def generate_random_numbers(num, bits):
    
    global n_max
    global n_min
    n_max = 2 ** (bits - 1) - 1
    n_min = -1 - n_max
    a1 = np.random.randint(n_min, n_max, num)
    a =  np.array(a1, dtype='int8')
    b = np.random.randint(0, 8, num)
    data = []
    for ind, i in enumerate(b):
        ##if i == 0:
        ##    data.append(n_max)
        ##elif i == 1:
        ##    data.append(n_min)
        ##elif i == 2:
        ##    data.append(a[ind] & 0xffff)
        ##elif i == 3:
        ##    data.append(-1 * (a[ind] & 0xffff))
        ##elif i % 2 == 0:
        ##    data.append(a[ind])
        ##else:
        ##    data.append(-1 * a[ind])
        
        data.append(a[ind])
    
    return data



def initialize_memories(mem=None):
     for k, v in buffers.items():
        data = generate_random_numbers(v,7)
        memories[k] = data


def dump_memories():
    # python only does arithmetic shift. Hence, need mask to remove sign extention while performing OR
    data1_mask = 255                        #11111111
    data2_mask = 65280                      #1111111100000000
    data3_mask = 16711680                   #111111110000000000000000
    data4_mask = 4278190080                 #11111111000000000000000000000000
    for i in memories.keys():
        wdata = ''
        data1, data2, data3, data4 = 0,0,0,0
        cntr = 0
        with open(i + '.txt', 'w') as f:
            for data in memories[i]:
                cntr += 1
                if (cntr % 4 == 1):
                    data1 |= data
                    data1 &= data1_mask
                    #print("Data1 = ", data)
                if (cntr % 4 == 2):
                    data2 |= data
                    data2 = data2 << 8
                    data2 &= data2_mask
                    #print("Data2 = ", data)
                if (cntr % 4 == 3):
                    data3 |= data
                    data3 = data3 << 16
                    data3 &= data3_mask
                    #print("Data3 = ", data)
                if (cntr % 4 == 0):
                    data4 |= data
                    data4 = data4 << 24
                    data4 &= data4_mask
                    #print("Data4 = ", data)
                    #print ("data4 << 24 | data3 << 16 | data2 << 8 | data1", data4, data3, data2, data1)
                    #print ("data4 << 24", data4 << 24)
                    #print ("data3 << 16", data3 << 16)
                    #print ("data2 << 8", data2 << 8)
                    
                    wdata = data4 | data3 | data2 | data1
                    f.write(str(wdata) + '\n')
                    wdata = ''
                    data1, data2, data3, data4 = 0,0,0,0
                    

def compute_output():
    #print("Input Size = ", len(memories['inputs'])   )    # , memories['inputs'])
    #print("Parameters Size = ",len(memories['parameters']))    # , memories['parameters'])
    #print("Bias Size = ",len(memories['bias'])      )    # , memories['bias'])

    input_np = np.array(memories['inputs'])   
    weights_np = np.array(memories['parameters'])
    bias_np = np.array(memories['bias'])      
    weights_np = np.reshape(weights_np, (-1, 128))

    #print("Input Shape = ",input_np.shape)    # , memories['inputs'])
    #print("Weight Shape = ",weights_np.shape)    # , memories['parameters'])
    #print("Bias Shape = ",bias_np.shape)    # , memories['bias'])

    res = np.matmul(input_np, weights_np)
    res += res + bias_np
    
    #print("Result Shape = ", res.shape)    # , memories['bias'])

    #A = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    #A = np.array(A)
    #print ("\n\nWeights Stored in DDR =", A.shape)
    #print (A)

    #A = np.reshape(A, (-1, 4))
    #print ("\n\nWeights Shape as per compiler=", A.shape)
    #print (A)
    fp_res = open('results.txt','w')
    for val in res.tolist():
        fp_res.write(str(val) + '\n')


initialize_memories()
dump_memories()
compute_output()



