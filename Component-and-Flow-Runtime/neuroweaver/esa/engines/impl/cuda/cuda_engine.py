import threading
import logging
import os
import argparse
import time
from queue import Queue

from util import write_to, read_protobuf
from qfdfg_pb2 import Component, Flow, Graph
from parser import EngineSystemUtil

from engines.engine import Engine

import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
from pycuda import compiler
import numpy as np


kernel_code_template = """
 __global__ void doublify(float *a)
  {
    int idx = threadIdx.x + threadIdx.y*4;
    a[idx] *= 2;
  }

  __global__ void MatrixMulKernel(float *a, float *b, float *c)
{
    int tx = threadIdx.x;
    int ty = threadIdx.y;

    // Pvalue is used to store the element of the matrix
    // that is computed by the thread
    float Pvalue = 0;

    // Each thread loads one row of M and one column of N,
    //   to produce one element of P.
    for (int k = 0; k < %(MATRIX_SIZE)s; ++k) {
        float Aelement = a[ty * %(MATRIX_SIZE)s + k];
        float Belement = b[k * %(MATRIX_SIZE)s + tx];
        Pvalue += Aelement * Belement;
    }

    // Write the matrix to device memory;
    // each thread writes one element
    c[ty * %(MATRIX_SIZE)s + tx] = Pvalue;
}
  """

MATRIX_SIZE = 8
kernel_code = kernel_code_template % {
    'MATRIX_SIZE': MATRIX_SIZE
    }
mod = compiler.SourceModule(kernel_code)


class CUDAEngine(Engine):

    def __init__(self):
        super(CUDAEngine, self).__init__('cuda')
        self.addrHash = {}
        self.data = []

    def open(self):
        pass

    def write(self, *args):
        # args is always a tuple with one element for some reason
        data = args[0]
        host_numpy_array = data[0]
        host_numpy_array = host_numpy_array.astype(np.float32)
        gpu_addr = cuda.mem_alloc(host_numpy_array.nbytes)
        cuda.memcpy_htod(gpu_addr, host_numpy_array)
        self.addrHash[gpu_addr] = host_numpy_array
        self.data.append(gpu_addr)

    def read(self):
        gpu_addr = self.output_data
        if gpu_addr not in self.addrHash:
            raise "This addr not allocated earlier"
        host_numpy_array = np.empty_like(self.addrHash[gpu_addr])
        cuda.memcpy_dtoh(host_numpy_array, gpu_addr)
        return [host_numpy_array]

    def compute(self, capability, metadata):
        func = mod.get_function(capability)
        method_input = self.data
        if capability == "doublify":
            func(method_input[0], block=(MATRIX_SIZE, MATRIX_SIZE, 1))
            self.output_data = method_input[0]
        else:
            func(method_input[0], method_input[1], method_input[2], block=(MATRIX_SIZE,MATRIX_SIZE,1))
            self.output_data = method_input[2]

    def close(self):
        for addr in self.addrHash:
            del addr


if __name__ == '__main__':
    g = CUDAEngine()
    a = np.ones((MATRIX_SIZE,MATRIX_SIZE))
    g.write(a)
    b = np.ones((MATRIX_SIZE,MATRIX_SIZE))
    g.write(b)
    c = np.ones((MATRIX_SIZE,MATRIX_SIZE))
    g.write(c)
    print("Matrices ", a, b)
    g.compute("MatrixMulKernel", None)
    result = g.read()
    print("Multiplication result ", result)
