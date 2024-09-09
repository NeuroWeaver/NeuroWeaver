import sys
sys.path.insert(0, '/Users/joon/ohai.src/qfdfg')
sys.path.insert(0, '/Users/joon/ohai.src/compiler')
import threading
import logging
import os
import argparse
import time
from queue import Queue

from qfdfg.util import write_to, read_protobuf
from qfdfg.qfdfg_pb2 import Component, Flow, Graph
from compiler.parser import EngineSystemUtil


class Engine(object):
    def __init__(self, name):
        self.name = name

    def open(self):
        pass

    def read(self):
        pass

    def write(self):
        pass

    def compute(self, capability: str):
        pass

    def close(self):
        pass
