import os
import time

from sklearn.linear_model import LogisticRegression

from queue import Queue

from util import write_to, read_protobuf
from qfdfg_pb2 import Component, Flow, Graph
from parser import EngineSystemUtil

from engines.engine import Engine


class SklearnEngine(Engine):

    def __init__(self):
        super(SklearnEngine, self).__init__('sklearn')

    def open(self):
        pass

    def read(self):
        # TODO check self.output_data is set
        return self.output_data

    def write(self, *args):
        self.data = args[0]

    def compute(self, capability: str, metadata):
        if capability == 'logistic_regression':
            in_x = self.data[0]
            in_y = self.data[1]
            self.output_data = self.logistic_regression(in_x, in_y)

    def close(self):
        pass

    def logistic_regression(self, in_x, in_y, weight=None, learning_rate=None):
        clf = LogisticRegression(random_state=0).fit(in_x, in_y)
        return [clf.predict(in_x)]
