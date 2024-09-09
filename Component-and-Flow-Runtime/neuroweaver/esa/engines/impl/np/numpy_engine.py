import os
import time

import numpy as np

from queue import Queue

from util import write_to, read_protobuf
from qfdfg_pb2 import Component, Flow, Graph
from parser import EngineSystemUtil

from engines.engine import Engine


class NumpyEngine(Engine):

    def __init__(self):
        super(NumpyEngine, self).__init__('numpy')

    def open(self):
        pass

    def read(self):
        # TODO check self.output_data is set
        return self.output_data

    def write(self, *args):
        self.data = args[0]

    def compute(self, capability: str, metadata):
        if capability == 'fft':
            in_array = self.data[0]
            self.output_data = self.fft(in_array)

    def close(self):
        pass

    def fft(self, in_array):
        return [np.fft.fft(in_array)]
