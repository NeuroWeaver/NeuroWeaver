import os
import time

from queue import Queue
import torch

from mpc import mpc
from mpc.mpc import QuadCost, LinDx

from util import write_to, read_protobuf
from qfdfg_pb2 import Component, Flow, Graph
from parser import EngineSystemUtil

from engines.engine import Engine


class MPCPytorchEngine(Engine):

    def __init__(self):
        super(MPCPytorchEngine, self).__init__('mpc_pytorch')

    def open(self):
        pass

    def read(self):
        # TODO check self.output_data is set
        return self.output_data

    def write(self, *args):
        self.data = args[0]

    def compute(self, capability: str, metadata):
        if capability == 'mpc':
            n_state = self.data[0]
            n_ctrl = self.data[1]
            T = self.data[2]
            self.output_data = self.logistic_regression(n_state, n_ctrl, T)

    def close(self):
        pass

    def mpc(self, n_state, n_ctrl, T):
        n_batch = 2

        # Randomly initialize a PSD quadratic cost and linear dynamics.
        C = torch.randn(T*n_batch, n_sc, n_sc)
        C = torch.bmm(C, C.transpose(1, 2)).view(T, n_batch, n_sc, n_sc)
        c = torch.randn(T, n_batch, n_sc)

        alpha = 0.2
        R = (torch.eye(n_state)+alpha*torch.randn(n_state, n_state)).repeat(T, n_batch, 1, 1)
        S = torch.randn(T, n_batch, n_state, n_ctrl)
        F = torch.cat((R, S), dim=3)

        x_init = torch.randn(n_batch, n_state)
        x_lqr, u_lqr, objs_lqr = mpc.MPC(n_state, n_ctrl, T)(x_init, QuadCost(C, c), LinDx(F))
        return x_lqr
