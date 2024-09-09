"""XLVM Engine Manager
"""
import threading
import logging
import os
import argparse
import time
from queue import Queue
import importlib

from qfdfg.util import write_to, read_protobuf
from qfdfg.qfdfg_pb2 import Component, Flow, Graph
from compiler.parser import EngineSystemUtil

from esa.engines.engine import Engine
from esa.engines.impl.tf.tensorflow_engine import TensorflowEngine

from definitions import ENGINE_SET_PBFILE


class EngineTable(object):
    def __init__(self):
        """
        Data structure for engine name, file descriptor, etc.
        """
        self.engines = []


class EngineManager(object):
    def __init__(self, engine_set):
        """Initializes Engine Manager.
        """
        self.ready_pool = []
        # TODO remove literal string
        self.engine_system = EngineSystemUtil(engine_set)
        self.logname = "[Engine Manager] "

    def start(self):
        #print("Starting Engine Manager!")
        pass

    def open(self, engine_name: str, engine_wrapper_classname: str, capability_name: str, qfdfg_pb: str = None):
        # print(self.logname)
        # print(f"open({engine_name}, {engine_wrapper_classname}, {capability_name})...")
        if engine_name == "default":
           engine_class = getattr(importlib.import_module("esa.engines.impl.default.default_engine"), engine_wrapper_classname)
           if qfdfg_pb is not None:
                engine = engine_class(qfdfg_pb)
           else:
                engine = engine_class()
           print()
           return engine

        # TODO put a wrapper for EngineSpecification
        # currently EngineSpecification object is returned
        #engine = self.engine_system.get_engine_by_name(engine_name)
        engine = self.engine_system.get_engine_by_name(engine_name)
        capability_info = self.engine_system.get_capability_info(engine, capability_name)
        engine_wrapper_filepath = capability_info.impl.filepath[1:-1]
        print(engine_wrapper_filepath)
        path = 'esa.engines.' + engine_wrapper_filepath[2:]

        module_name = path.replace('/', '.')[:-3]
        class_name = engine_wrapper_classname
        engine_class = getattr(importlib.import_module(module_name), class_name)
        engine = engine_class()
        print()
        return engine

    def read(self, engine):
        return engine.read()

    def write(self, engine, *args):
        #print(f"write({engine}, args)...\n")
        engine.write(*args)

    def compute(self, engine, capability: str, metadata=None):
        print(self.logname)
        print("compute()\n")
        #print(f"compute({engine}, {capability}, {metadata})...\n")
        engine.compute(capability, metadata)

    def close(self):
        pass

    def engine_available(self, engine_name: str) -> bool:
        return True

    def engine_in_use(self, engine_name: str) -> bool:
        pass


def main(args):
    engine_manager = EngineManager(args.engine_set)
    tf_engine = engine_manager.open('tensorflow', 'TensorflowEngine', 'matmul')

    from engines.impl.cuda.cuda_engine import CUDAEngine, MATRIX_SIZE
    cuda_engine = CUDAEngine()

    import numpy as np
    a = np.ones((MATRIX_SIZE,MATRIX_SIZE))
    b = np.ones((MATRIX_SIZE,MATRIX_SIZE))
    c = np.ones((MATRIX_SIZE,MATRIX_SIZE))
    engine_manager.write(cuda_engine, a)
    engine_manager.write(cuda_engine, b)
    engine_manager.write(cuda_engine, c)
    # engine_manager.compute(cuda_engine, "MatrixMulKernel", None)
    engine_manager.compute(cuda_engine, "doublify", None)
    data = engine_manager.read(cuda_engine)
    print(data)

    # import tensorflow as tf
    # a = tf.constant([1,2,3,4,5,6], shape=[2,3])
    # b = tf.constant([7,8,9,10,11,12], shape=[3,2])
    # a = [[1, 2], [3, 4]]
    # b = [[5, 6], [7, 8]]

    # engine_manager.write(tf_engine, a, b)
    # engine_manager.compute(tf_engine, 'matmul')
    # data = engine_manager.read(tf_engine)

    # print(data)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='''XLVM EngineManager.
        Engine Manager for XLVM Runtime.''')
    argparser.add_argument('-e', '--engine_set',
                           default=ENGINE_SET_PBFILE,
                           help='Engine system file (.pb). Default: esa/engine_system.pb')
    args = argparser.parse_args()

    main(args)
