import os


def fft(input_data):
    os.lseek()
    os.write()

def ifft(input_data):
    os.lseek()
    os.write()

def write(capability, args):
    if capability == 'fft':
        fft(args.input_data)
    elif capability == 'ifft':
        ifft(args.input_data)

def read():
    os.lseek()
    os.read()
