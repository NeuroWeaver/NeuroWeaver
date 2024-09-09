import numpy as np
import sys

weights_file = sys.argv[1]
wfp = open(weights_file, "r")
pe_coordinates = [63,0]
weights_1D = []

with open(weights_file) as f:
    for line in f:
        weights_1D.append(int(line))


weights = np.random.rand(3,3,64,64)
(KH,KW,IC,OC) = weights.shape

def weight_4d_to_1d_PE():
    weight_addr = 0
    global KH,KW,IC,OC, pe_coordinates, weights_1D
    w_kh = KH
    w_kw = KW
    w_ic = pe_coordinates[0]
    w_oc = pe_coordinates[1]
    print ("DDR Index       Buffer Address      Element")
    for i in range(w_kh):
        for j in range(w_kw):
            weight_1D_idx = (i*KW*IC*OC) + (j*IC*OC) + (w_ic*OC) + w_oc
            
            print (weight_1D_idx, "\t\t\t",weight_addr,"\t\t",weights_1D[weight_1D_idx],"\n")
            weight_addr += 1
            

PE_column = 0
kernel_w = 0
kernel_h = 0

def weight_4d_to_1d_AXI():
    global KH,KW,IC,OC, weights_1D, PE_column,kernel_h,kernel_w
    w_kh = kernel_h
    w_kw = kernel_w
    w_ic = IC
    w_oc = PE_column
    print ("DDR Index       Buffer Address      Element")
    for i in range(IC):
        weight_1D_idx = (w_kh*KW*IC*OC) + (w_kw*IC*OC) + (i*OC) + w_oc
        print (weight_1D_idx, "\t\t\t",0,"\t\t",weights_1D[weight_1D_idx])



#####################################################
input_file = sys.argv[2]
ibuf_bank = 63
input_1D = []


inputs = np.random.rand(1,33,17,64)

(N,IH,IW,IC) = inputs.shape

with open(input_file) as fp:
        for line in fp:
            input_1D.append(int(line))


def inputs_4d_to_1d_PE():
    input_addr = 0
    global N,IH,IW,IC,ibuf_bank, input_1D
    i_n = N
    i_ih = IH 
    i_iw = IW
    i_ic = ibuf_bank
    print (i_n, i_ih, i_iw, i_ic)
    print ("DDR Index       IBuf Address      Element")
    for i in range(i_n):
        for j in range(i_ih):
            for k in range(i_iw):
                input_1D_idx = (i*IH*IW*IC) + (j*IW*IC) + (k*IC) + i_ic
                print (input_1D_idx, "\t\t\t",input_addr,"\t\t",input_1D[input_1D_idx],"\n")
                input_addr += 1

def custom_output():
    A = np.arange(0, 64, 1)
    B = np.arange(0, 64, 1)
    C = np.arange(64, 128, 1)
    D = np.arange(64, 128, 1)
    E = np.arange(0, 64, 1)
    F = np.arange(0, 64, 1)

    #A = np.full((64,),1)
    #B = np.full((64,),2)
    #C = np.full((64,),1)
    #D = np.full((64,),2)
    #E = np.full((64,),1)
    #F = np.full((64,),2)

    print ("A = ", A, "\n", "C = ", C, "\n")

    par1 = (A * B)
    par2 = (C * D)
    par3 = (E * F)
    par1_sum = 0
    par2_sum = 0
    par3_sum = 0
     
    for i in range(len(par1)):
        par1_sum +=  par1[i]
        par2_sum +=  par2[i]
        par3_sum +=  par3[i]
    

    print ("Partial sums = ", par1_sum, "\t", par2_sum, "\t",  par3_sum, "\t")
    out =  (par1_sum + par2_sum + par3_sum) + (par2_sum + par1_sum + par2_sum) + (par1_sum + par2_sum + par3_sum)
       
    print ("Pixel = ", out)



def weight_4d_to_shuffled_1d():
    weight_addr = 0
    required_OC = 0
    global KH,KW,IC,OC, pe_coordinates, weights_1D
    w_kh = KH
    w_kw = KW
    w_ic = IC
    w_oc = OC
    print ("DDR Index       Buffer Address      Element")
    for i in range(w_kh):
        for j in range(w_kw):
            for k in range(w_ic):
                for l in range(w_oc):
                    weight_1D_idx = (i*KW*IC*OC) + (j*IC*OC) + (k* (OC-l-1)) + l
                    #print (weight_1D_idx, "\t\t\t",weight_addr,"\t\t",weights_1D[weight_1D_idx],"\n")
                    if (k == 63 and l == 0):
                        print (weight_1D_idx, "\t\t\t",weight_addr,"\t\t",weights_1D[weight_1D_idx],"\n")
                    
                    weight_addr += 1
                    






if sys.argv[3] == '0':
    weight_4d_to_1d_PE()
elif sys.argv[3] == '1':
    weight_4d_to_1d_AXI()
elif sys.argv[3] == '2':
    custom_output()
elif sys.argv[3] == '3':
    weight_4d_to_shuffled_1d()
else:
    inputs_4d_to_1d_PE()