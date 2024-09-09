import logging
import pickle

import numpy as np

from esa.engines.engine import Engine

from dnnweaver2.tensorOps.cnn import conv2D, maxPool
from dnnweaver2.graph import Graph
from dnnweaver2 import get_tensor
from dnnweaver2.scalar.dtypes import FQDtype, FixedPoint
from dnnweaver2.fpga.fpgamanager import FPGAManager

import dnnweaver2.compiler
import dnnweaver2.simulator.accelerator


class DnnweaverEngine(Engine):

    def __init__(self):
        super(DnnweaverEngine, self).__init__('dnnweaver')
        self.fpga_manager = FPGAManager(pci_cl_ctrl_device="/dev/xdma0_user", c2h_dma_device="/dev/xdma0_c2h_0", h2c_dma_device="/dev/xdma0_h2c_0")

        graph_file = './compiler/dnn_graph.pckl'
        with open(graph_file, 'rb') as f:
            graph = pickle.load(f)

        inst_file = './compiler/inst.bin'
        inst_array = np.loadtxt(inst_file, dtype=np.int64)

        self.fpga_manager.initialize_graph_tensors(graph)
        #graph.load_params_from_pickle(weight_pickle)
        self.fpga_manager.write('pci_cl_data', 0, inst_array)
        self.fpga_manager.initialize_graph(graph, 32, 32)

    def open(self):
        pass

    def read(self):
        return self.output_data

    def write(self, *args):
        self.data = args[0]

    def compute(self, capability: str, metadata):
        if capability == 'conv2d':
            t_in = self.data[0]
            weights = self.data[1]
            biases = self.data[2]
            self.output_data = self.conv2d(t_in, weights, biases)
        elif capability == 'max_pool':
            t_in = self.data[0]
            self.output_data = self.max_pool(t_in)
        elif capability == 'batch_norm':
            pass

    def close(self):
        pass


    def conv2d(self, t_in, weights, biases):
        # batch_size = 1
        # graph = Graph('Conv-Test: 16-bit', dataset='random', log_level=logging.INFO)
        # with graph.as_default():
        #     with graph.name_scope('inputs'):
        #         i = get_tensor(shape=(batch_size,32,32,3), name='data', dtype=FQDtype.FXP16, trainable=False)
        #     with graph.name_scope('conv0'):
        #         w = get_tensor(shape=(128, 3, 3, 3),
        #                              name='weights',
        #                              dtype=FixedPoint(16,12))
        #         b = get_tensor(shape=(128),
        #                             name='biases',
        #                             dtype=FixedPoint(32,20))
        #         conv = conv2D(i, w, b, pad='SAME', dtype=FixedPoint(16,8))

        # fpga_spec = dnnweaver2.compiler.FPGASpec(num_ddr=1, size_ddr=1024, bandwidth_per_ddr=512)
        # fpga_compiler = dnnweaver2.compiler.GraphCompiler(fpga_spec)
        # sram ={
        #     'ibuf': 16*32*512,
        #     'wbuf': 16*32*32*512,
        #     'obuf': 64*32*512,
        #     'bbuf': 16*32*512
        # }
        # acc_obj = dnnweaver2.simulator.accelerator.Accelerator(N=32,M=32,prec=16,mem_if_width=256,frequency=100e6,sram=sram)
        # inst_array = fpga_compiler.compile(graph=graph, acc_obj=acc_obj)


        self.fpga_manager.send_input_nparr(t_in)
        self.fpga_manager.start()
        self.fpga_manager.wait_fpga_execution()
        out_tensors = self.fpga_manager.recv_output_nparr()

        return [out_tensors, weights, biases]

    def max_pool(self, t_in):
        batch_size = 1
        graph = Graph('Max Pool-Test: 16-bit', dataset='random', log_level=logging.INFO)
        with graph.as_default():
            with graph.name_scope('inputs'):
                i = get_tensor(shape=(batch_size,32,32,128), name='data', dtype=FQDtype.FXP16, trainable=False)
            with graph.name_scope('pool'):
                pool = maxPool(i, pooling_kernel=(1,2,2,1), stride=(1,2,2,1), pad='VALID')

        fpga_spec = dnnweaver2.compiler.FPGASpec(num_ddr=1, size_ddr=1024, bandwidth_per_ddr=512)
        fpga_compiler = dnnweaver2.compiler.GraphCompiler(fpga_spec)
        sram ={
            'ibuf': 16*32*512,
            'wbuf': 16*32*32*512,
            'obuf': 64*32*512,
            'bbuf': 16*32*512
        }
        acc_obj = dnnweaver2.simulator.accelerator.Accelerator(N=32,M=32,prec=16,mem_if_width=256,frequency=100e6,sram=sram)
        inst_array = fpga_compiler.compile(graph=graph, acc_obj=acc_obj)

        fpga_manager = FPGAManager(pci_cl_ctrl_device="/dev/xdma0_user", c2h_dma_device="/dev/xdma0_c2h_0", h2c_dma_device="/dev/xdma0_h2c_0")
        fpga_manager.initialize_graph_tensors(graph)
        #graph.load_params_from_pickle(weight_pickle)
        fpga_manager.write('pci_cl_data', 0, inst_array)
        fpga_manager.initialize_graph(graph, 32, 32)


        fpga_manager.send_input_nparr(t_in)
        fpga_manager.start()
        fpga_manager.wait_fpga_execution()
        out_tensors = fpga_manager.recv_output_nparr()

        return [out_tensors]



    def batch_norm(self):
        pass

    def add_bias(self):
        pass

    def flatten(self):
        pass

    def matmul(self):
        pass

    def add(self):
        pass

    def leaky_relu(self):
        pass

    def yolo2_tiny(self):
        pass
