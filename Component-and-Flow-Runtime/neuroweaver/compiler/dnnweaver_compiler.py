"""Wrapper for DnnWeaver compiler. This module is called during Yin-Yang compilation pass."""
import logging
import pickle

import numpy as np

from dnnweaver2.tensorOps.cnn import conv2D, maxPool
from dnnweaver2.graph import Graph
from dnnweaver2 import get_tensor
from dnnweaver2.scalar.dtypes import FQDtype, FixedPoint
from dnnweaver2.fpga.fpgamanager import FPGAManager

import dnnweaver2.compiler
import dnnweaver2.simulator.accelerator


class DnnweaverCompiler(object):
    # Lookup table for capability --> Dnnweaver IR node
    dnnweaver_node_table = {
        'conv2d': conv2D
    }

    def __init__(self):
        # Initialize DnnWeaver's FPGA Compiler and Accelerator Object
        fpga_spec = dnnweaver2.compiler.FPGASpec(num_ddr=1, size_ddr=1024, bandwidth_per_ddr=512)
        self.fpga_compiler = dnnweaver2.compiler.GraphCompiler(fpga_spec)
        sram ={
            'ibuf': 16*32*512,
            'wbuf': 16*32*32*512,
            'obuf': 64*32*512,
            'bbuf': 16*32*512
        }
        self.acc_obj = dnnweaver2.simulator.accelerator.Accelerator(N=32,M=32,prec=16,mem_if_width=256,frequency=100e6,sram=sram)

    def compile(self, capability):
        # Generate DnnWeaver Graph (IR) for the given capability
        graph = Graph('Conv-Test: 16-bit', dataset='random', log_level=logging.INFO)
        if capability == 'conv2d':
            self._generate_conv2d_node(graph)
        elif capability == 'max_pool':
            self._generate_max_pool_node(graph)

        inst_array = self.fpga_compiler.compile(graph=graph, acc_obj=self.acc_obj)

        with open('dnn_graph.pckl', 'wb') as f:
            pickle.dump(graph, f)

        return inst_array


    def _generate_conv2d_node(self, graph):
        batch_size = 1
        with graph.as_default():
            with graph.name_scope('inputs'):
                i = get_tensor(shape=(batch_size,32,32,3), name='data', dtype=FQDtype.FXP16, trainable=False)
            with graph.name_scope('conv0'):
                w = get_tensor(shape=(128, 3, 3, 3),
                                     name='weights',
                                     dtype=FixedPoint(16,12))
                b = get_tensor(shape=(128),
                                    name='biases',
                                    dtype=FixedPoint(32,20))
                conv = conv2D(i, w, b, pad='SAME', dtype=FixedPoint(16,8))


    def _gneerate_max_pool_node(self, graph):
        pass


def main():
    pass


if __name__ == '__main__':
    pass
