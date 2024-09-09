import sys
def decimalToBinary(n):
    return bin(n).replace("0b", "")
   
def decimalToBinary1(num):
    s = ''
    for i in range(31,-1,-1):
        cur=(num>>i) & 1 #(right shift operation on num and i and bitwise AND with 1)
        s+=str(cur)
    return s

if __name__ == '__main__':
    rfname = sys.argv[1]
    wfname = sys.argv[2]

    fw = open(wfname, "w")
    
    with open(rfname) as f:
        lines = f.readlines()
    
    for line in lines:
        val = decimalToBinary1(int(line))
        fw.write(val)
        fw.write('\n')
    
    fw.close()
    