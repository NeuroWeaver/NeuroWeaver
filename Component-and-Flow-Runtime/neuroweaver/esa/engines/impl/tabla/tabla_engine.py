from engines.engine import Engine

import math
import sys
sys.path.append('/home/joon/tabla_fpga/tabla_driver/tabla_fpga_tests')
from dnn_fpga import dnn_fpga


def run_fpga(weight_array, input_array, cnt, weightaddr, weightsize, inputaddr, inputsize,
outputaddr, rddataoffset):
    updated_weights = dnn_fpga.initialize_yolo_graph(weight_array, input_array, cnt,  weightaddr,
    weightsize, inputaddr, inputsize, outputaddr, rddataoffset)
    return updated_weights


class TablaEngine(Engine):

    def __init__(self):
        super(TablaEngine, self).__init__('tabla')

    def open(self):
        pass

    def read(self):
        return self.output_data

    def write(self, *args):
        self.data = args[0]

    def compute(self, capability: str, metadata):
        if capability == 'linear_regression':
            import numpy as np
            self.data.append(np.random.rand(2))
            input_data = self.data[0]
            weights = self.data[1]
            self.output_data = self.linear_regression(input_data, weights)

    def close(self):
        pass

    def linear_regression(self, input_data, weights):
        cnt = [2048, 1322]
        weightaddr = 0
        weightsize = math.ceil(cnt[0]/16)
        print ("output div = ", weightsize)
        weightsize = 56
        inputaddr = cnt[0]
        inputsize = math.ceil(cnt[1]/16)
        outputaddr = cnt[0] + cnt[1]
        rddataoffset = 16
        updated_weights = run_fpga(weights, input_data, cnt,  weightaddr, weightsize, inputaddr, inputsize, outputaddr, rddataoffset)

        return [updated_weights]
