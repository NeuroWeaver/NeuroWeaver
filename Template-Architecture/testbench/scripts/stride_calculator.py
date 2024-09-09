import numpy as np
from collections import defaultdict

def conv_forward(input,weights,bias,stride,pad):
    global N,IH,IW,IC,OH,OW,OC,KH,KW
    (N, IH, IW, IC) = input.shape
    (KH,KW,IC,OC) = weights.shape
    OH = int((IH - KH + 2*pad)/stride+1)
    OW = int((IW - KW + 2*pad)/stride+1)
    Z = np.zeros((N,OH,OW,OC))
    inputs_pad = zero_pad(input,pad)
    print ("stride, pad = ",stride, pad, "\n")
    print ("N, IC, IH, IW = ", N, IC, IH, IW, "\n")
    print ("KH, KW = ", KH, KW, "\n")
    print ("OC, OH, OW = ", OC, OH, OW, "\n\n")
    

    OW_dict = {"ibuf": defaultdict(lambda: []), "obuf": defaultdict(lambda: []), "wbuf": defaultdict(lambda: []), "bbuf": defaultdict(lambda: [])}
    OH_dict = {"ibuf": defaultdict(lambda: []), "obuf": defaultdict(lambda: []), "wbuf": defaultdict(lambda: []), "bbuf": defaultdict(lambda: [])}
    OC_dict = {"ibuf": defaultdict(lambda: []), "obuf": defaultdict(lambda: []), "wbuf": defaultdict(lambda: []), "bbuf": defaultdict(lambda: [])}
    IC_dict = {"ibuf": defaultdict(lambda: []), "obuf": defaultdict(lambda: []), "wbuf": defaultdict(lambda: []), "bbuf": defaultdict(lambda: [])}
    N_dict =  {"ibuf": defaultdict(lambda: []), "obuf": defaultdict(lambda: []), "wbuf": defaultdict(lambda: []), "bbuf": defaultdict(lambda: [])}
    KW_dict = {"ibuf": defaultdict(lambda: []), "obuf": defaultdict(lambda: []), "wbuf": defaultdict(lambda: []), "bbuf": defaultdict(lambda: [])}
    KH_dict = {"ibuf": defaultdict(lambda: []), "obuf": defaultdict(lambda: []), "wbuf": defaultdict(lambda: []), "bbuf": defaultdict(lambda: [])}
    
    print ("inputs = ", input.shape)
    print ("weights = ", weights.shape)
    print ("Outputs = ", Z.shape)
    for k in range(OC):
        for n in range(N):
            for c in range(IC):
                for r in range(KH):
                    for s in range(KW):
                        for p in range(OH):
                            for q in range(OW):
                                h = p*stride -pad + r
                                w = q*stride - pad + s
                                
                                ##print ("Z[N=",n ,"OC=",k ,"OH=" ,p ,"OW=" ,q , " += input[N=",n ,"IC=" ,c ,"h=" ,h ,"w=" ,w , "] * ", "weights[OC=",k ,"IC=" ,c ,"KH=" ,r ,"KW=" ,s , "]")
                                Z[n,p,q,k] += inputs_pad[n][h][w][c] * weights[r][s][c][k]
                                if k == 0 and n == 0 and c == 0 and r == 0 and s == 0 and p == 0:
                                    compute_stride(OW_dict["ibuf"][q], n,h,w,c, 0)
                                    compute_stride(OW_dict["obuf"][q], n,p,q,k, 1)
                                    compute_stride(OW_dict["wbuf"][q], r,s,c,k, 2)
                                    #compute_stride(OW_dict["bbuf"][q], n,h,w,c, 3)
                                if k == 0 and n == 0 and c == 0 and r == 0 and s == 0 and q == 0:
                                    compute_stride(OH_dict["ibuf"][p], n,h,w,c, 0)
                                    compute_stride(OH_dict["obuf"][p], n,p,q,k, 1)
                                    compute_stride(OH_dict["wbuf"][p], r,s,c,k, 2)
                                if k == 0 and n == 0 and c == 0 and r == 0 and p == 0 and q == 0:
                                    compute_stride(KW_dict["ibuf"][s], n,h,w,c, 0)
                                    compute_stride(KW_dict["obuf"][s], n,p,q,k, 1)
                                    compute_stride(KW_dict["wbuf"][s], r,s,c,k, 2)
                                if k == 0 and n == 0 and c == 0 and s == 0 and p == 0 and q == 0:
                                    compute_stride(KH_dict["ibuf"][r], n,h,w,c, 0)
                                    compute_stride(KH_dict["obuf"][r], n,p,q,k, 1)
                                    compute_stride(KH_dict["wbuf"][r], r,s,c,k, 2)
                                if k == 0 and n == 0 and r == 0 and s == 0 and p == 0 and q == 0:
                                    compute_stride(IC_dict["ibuf"][c], n,h,w,c, 0)
                                    compute_stride(IC_dict["obuf"][c], n,p,q,k, 1)
                                    compute_stride(IC_dict["wbuf"][c], r,s,c,k, 2)
                                if k == 0 and c == 0 and r == 0 and s == 0 and p == 0 and q == 0:
                                    compute_stride(N_dict["ibuf"][n], n,h,w,c, 0)
                                    compute_stride(N_dict["obuf"][n], n,p,q,k, 1)
                                    compute_stride(N_dict["wbuf"][n], r,s,c,k, 2)
                                if n == 0 and c == 0 and r == 0 and s == 0 and p == 0 and q == 0:
                                    compute_stride(OC_dict["ibuf"][n], n,h,w,c, 0)
                                    compute_stride(OC_dict["obuf"][n], n,p,q,k, 1)
                                    compute_stride(OC_dict["wbuf"][n], r,s,c,k, 2)

                                
    print ("\nOW_dict[ibuf] \n", OW_dict["ibuf"])
    print ("*************************************")
    print ("\nOW_dict[obuf] \n", OW_dict["obuf"])
    print ("*************************************")
    print ("\nOW_dict[wbuf] \n", OW_dict["wbuf"])
    print ("*******************************************************************************")
    
    print ("\nOH_dict[ibuf] \n", OH_dict["ibuf"])
    print ("*************************************")
    print ("\nOH_dict[obuf] \n", OH_dict["obuf"])
    print ("*************************************")
    print ("\nOH_dict[wbuf] \n", OW_dict["wbuf"])
    print ("*******************************************************************************")
    
    print ("\nKW_dict[ibuf] \n", KW_dict["ibuf"])
    print ("*************************************")
    print ("\nKW_dict[obuf] \n", KW_dict["obuf"])
    print ("*************************************")
    print ("\nKW_dict[wbuf] \n", KW_dict["wbuf"])
    print ("*******************************************************************************")
    
    print ("\nKH_dict[ibuf] \n", KH_dict["ibuf"])
    print ("*************************************")
    print ("\nKH_dict[obuf] \n", KH_dict["obuf"])
    print ("*************************************")
    print ("\nKH_dict[wbuf] \n", KH_dict["wbuf"])
    print ("*******************************************************************************")
    
    print ("\nIC_dict[ibuf] \n", IC_dict["ibuf"])
    print ("*************************************")
    print ("\nIC_dict[obuf] \n", IC_dict["obuf"])
    print ("*************************************")
    print ("\nIC_dict[wbuf] \n", IC_dict["wbuf"])
    print ("*******************************************************************************")
    
    print ("\nN_dict[ibuf] \n", N_dict["ibuf"])
    print ("*************************************")
    print ("\nN_dict[obuf] \n", N_dict["obuf"])
    print ("*************************************")
    print ("\nN_dict[wbuf] \n", N_dict["wbuf"])
    print ("*******************************************************************************")

        
    print ("\nOC_dict[ibuf] \n", OC_dict["ibuf"])
    print ("*************************************")
    print ("\nOC_dict[obuf] \n", OC_dict["obuf"])
    print ("*************************************")
    print ("\nOC_dict[wbuf] \n", OC_dict["wbuf"])
    print ("*******************************************************************************")
    
    return Z    

def zero_pad(X,pad):
  x_pad = np.pad(X,((0,0),(pad,pad),(pad,pad),(0,0)),mode='constant',constant_values=(0,0))
  return x_pad

def compute_stride(dim_array, dim3,dim2,dim1,dim0,buf):
    if buf == 0:
        input_1D_idx = (dim3*IH*IW*(IC)) + (dim2*IW*(IC)) + (dim1*(IC)) + dim0
        dim_array.append(int(input_1D_idx/IC))
    elif buf == 1:
        output_1D_idx = (dim3*OH*OW*(OC)) + (dim2*OW*(OC)) + (dim1*(OC)) + dim0
        dim_array.append(int(output_1D_idx/OC))
    elif buf == 2:
        weight_1D_idx = (dim3*KW*IC*OC) + (dim2*IC*OC) + (dim1*OC) + dim0
        dim_array.append(int(weight_1D_idx/(IC*OC)))


input = np.random.rand(2,5,5,3)
weights = np.random.rand(3,3,3,2)
bias = np.random.rand(2)
stride = 1
pad = 0
conv_forward(input,weights,bias,stride, pad)