#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 21:12:39 2020

@author: psarikh
"""


import threading
import time
import logging

import numpy as np

from random import randint
import gpflow
from gpflowopt.domain import ContinuousParameter
from gpflowopt.bo import BayesianOptimizer
from gpflowopt.acquisition import LowerConfidenceBound
from gpflowopt.optim import SciPyOptimizer, StagedOptimizer, MCOptimizer
#from pyDOE import *


n_rows =1
n_cols = 100
param = np.float64(randint(0, 100))

def Data_generator(n_rows, n_cols, param):
    data = np.random.uniform(0, 1, (n_rows, n_cols))
    return (data,param)


def Signal_Processing(data_in):
    signal = data_in[0]
    param = data_in[1]
    objective = np.sum(abs(np.fft.fft(data_in[0])),axis=1)

    return (objective, param)



# GP model
def GP_Model_BO(X, Y):
    k1 = gpflow.kernels.Matern32(1, active_dims=[0], ARD=True)
    m = gpflow.gpr.GPR(X, Y.T, k1)
    m.kern.lengthscales = np.std(X)
    m.kern.lengthscales = np.std(X)
    m.kern.variance = np.std(Y) / np.sqrt(2)
    m.likelihood.variance = np.std(Y) / np.sqrt(2)
    # print(m)
    return m



def optimize(data_in):

    Y = np.array([list(data_in[i][0]) for i in range(len(data_in))]) # Objective values
    X = np.array([data_in[i][1] for i in range(len(data_in))]).reshape(1,-1) # parameter values

    # train a gp model on all input data points

    model=GP_Model_BO(X.T, Y.T)
    print(model)

    def objective_function(x):
        mean, std = model.predict_y(x)
        return mean
    sigma = 3.0
    alpha = LowerConfidenceBound(model, sigma)

    domain = ContinuousParameter('X', 0, 100)

    acquisition_opt = StagedOptimizer([MCOptimizer(domain, 100), SciPyOptimizer(domain)])
    optimizer = BayesianOptimizer(domain, alpha, optimizer=acquisition_opt)
    # with optimizer.silent():
    r = optimizer.optimize(objective_function, n_iter=1)

    print(r)

    # alpha.data gives the next stimulation parameters

    next_stim = alpha.data[0][-1][0]
    next_stim = np.float64(int(next_stim))

    return next_stim




def main():
    n_rows =1
    n_cols = 100

    all_data=[]
    burn_in = 5 # number of initial runs to get 5 pairs of data points to feed into the optimizer
    for i in range(burn_in):
        param = np.float64(randint(0, 100))
        # component one: random data generator
        data_in = Data_generator(n_rows, n_cols, param)

        # Compnent two: signal processing component
        # You can replace it with your fft implementation from signal processing module
        data_out_signal = Signal_Processing(data_in)
        # print(data_out_signal)
        all_data.append(data_out_signal)

    # While true or for a given number of iterations
    while True:

        # Component three: Optimizer (Bayesian Optimization)
        # It has an underlying model (Gaussin Process) called GP_Model_BO
        # running the Bayesian optimization
        next_control_param = optimize(all_data)
        print ('next control parametr', next_control_param)
        # Repeat generating data while True and

        # component one: random data generator
        data_in = Data_generator(n_rows, n_cols, next_control_param)

        # Compnent two: signal processing component
        # You can replace it with your fft implementation from signal processing module
        data_out_signal = Signal_Processing(data_in)
        all_data.append(data_out_signal)


main()
