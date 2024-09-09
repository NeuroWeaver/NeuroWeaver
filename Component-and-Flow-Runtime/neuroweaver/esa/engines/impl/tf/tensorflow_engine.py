import threading
import logging
import os
import argparse
import time
from queue import Queue

from qfdfg.util import write_to, read_protobuf
from qfdfg.qfdfg_pb2 import Component, Flow, Graph
from compiler.parser import EngineSystemUtil

from esa.engines.engine import Engine


class TensorflowEngine(Engine):
    def __init__(self):
        super(TensorflowEngine, self).__init__('tensorflow')

        # Dirty
        from qfdfg_pb2 import Component, Flow, Graph
        from util import write_to, read_protobuf
        self.graph = Graph()
        read_protobuf('/usr/src/app/compiler/qfdfg.pb', self.graph)

    def open(self):
        pass

    def read(self):
        # TODO check self.output_data is set
        return self.output_data

    def write(self, *args):
        self.data = args[0]

    def compute(self, capability: str, metadata):
        if capability == 'fft':
            t_in = self.data[0]
            self.output_data = self.fft(t_in)
        elif capability == 'matmul':
            t_in1 = self.data[0]
            t_in2 = self.data[1]
            self.output_data = self.matmul(t_in1, t_in2)
        elif capability == 'conv2d':
            t_in = self.data[0]
            weights = self.data[1]
            biases = self.data[2]
            self.output_data = self.conv2d(t_in, weights, biases)
        elif capability == 'max_pool':
            t_in = self.data[0]
            self.output_data = self.max_pool(t_in)

    def close(self):
        pass

    def fft(self, t_in):
        import tensorflow as tf

        tf.debugging.set_log_device_placement(True)
        #with tf.device('/device:XLA_GPU:0'):
        t = tf.convert_to_tensor(t_in, dtype=tf.complex64)
        out_tensors = tf.signal.fft2d(t)

        sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
        out_tensors = sess.run(out_tensors)
        # print(out_tensors)

        component = None
        for comp in self.graph.components:
            if comp.name == 'fft':
                component = comp
        outs = ','.join(component.output_names)
        print('In fft tf engine:')
        print(f'{out_tensors}')
        print(f'{outs} = {out_tensors}')

        # import re, ast
        # placeholder = re.sub('\s+', '', str(out_tensors))
        # print(f'{outs} = {placeholder}')
        # exec(f'{outs} = {placeholder}', globals())

        #exec(f'{outs} = {out_tensors}', globals())
        import pickle
        with open('out_tensors', 'wb') as f:
            pickle.dump(out_tensors, f)
        exec(f'with open("out_tensors", "rb") as f:\n\t{outs} = pickle.load(f)')

        return [out_tensors]


    def matmul(self, t_in1, t_in2):
        import tensorflow.compat.v1 as tf
        tf.disable_v2_behavior()

        t_out = tf.matmul(t_in1, t_in2)
        init = tf.initialize_all_variables()
        with tf.Session() as sess:
            sess.run(init)
            out_tensors = sess.run(t_out)

        # TODO Document why we need this
        # Dirty
        component = None
        for comp in self.graph.components:
            if comp.name == 'matmul':
                component = comp
        outs = ','.join(component.output_names)
        print('In matmul tf engine:')
        print(f'{out_tensors}')
        print(f'{outs} = {out_tensors}')

        import re, ast
        placeholder = re.sub('\s+', ',', str(out_tensors))
        print(f'{outs} = {placeholder}')
        exec(f'{outs} = {placeholder}', globals())

        # For now it is required to provide outputs in a list.
        return [out_tensors]


    def conv2d(self, t_in, weights, biases):
        import tensorflow.compat.v1 as tf
        tf.disable_v2_behavior()

        t_out = tf.nn.conv2d(t_in, weights, strides=[1, 1, 1, 1], padding='SAME')

        init = tf.initialize_all_variables()
        with tf.Session() as sess:
            sess.run(init)
            out_tensors = sess.run(t_out)

        return [out_tensors, weights, biases]

    def max_pool(self, t_in):
        import tensorflow.compat.v1 as tf
        tf.disable_v2_behavior()

        t_out = tf.nn.max_pool(t_in, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

        init = tf.initialize_all_variables()
        with tf.Session() as sess:
            sess.run(init)
            out_tensors = sess.run(t_out)
        return [out_tensors]
