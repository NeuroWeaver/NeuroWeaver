import threading
import time
import logging

import numpy as np

from queue import Queue
from random import randint
from threading import Lock
from collections import deque

from random import randint
import tensorflow as tf
import gpflow
from gpflowopt.domain import ContinuousParameter
from gpflowopt.bo import BayesianOptimizer
from gpflowopt.acquisition import LowerConfidenceBound
from gpflowopt.optim import SciPyOptimizer, StagedOptimizer, MCOptimizer
from pyDOE import *
import random
from neurolib.models.aln import ALNModel
# Some useful functions are provided here
import neurolib.utils.functions as func

from functools import partial
import numpy as np

from neurolib.models.aln import ALNModel
from neurolib.utils.loadData import Dataset
from neurolib.utils.signal import RatesSignal, BOLDSignal
import matplotlib.pyplot as plt


import pickle

from pathlib import Path

import ohai.digital_signal_processing as dsp
from skimage import util

from qfdfg.qfdfg_pb2 import Component

def MeanFieldModel(X):
    stim_amp = X[0]
    stim_freq = X[1]
    model = ALNModel()
    model.params['duration'] = 2 * 1000 # time duration in ms : Updated
    model.params['sigma_ou'] = 0.0 # we add some noise : Updated
    # define the stimulus
    stimulus = func.construct_stimulus("ac", duration=model.params.duration, dt=model.params.dt, stim_amp=stim_amp, stim_freq=stim_freq)
    # Model
    model.params['ext_exc_current'] = stimulus
    model.run()
    # Output signal
    output = model.output
    return output

def custom_logic(buffer2, data):
    """Custom logic used by Thread 4 to put its data in Buffer 2."""
    with Lock() as lock:
        f = open('new_param', 'wb')
        pickle.dump(data, f)
        f.close()

def get_all_queue_result(queue):
    result_list = []
    while not queue.empty():
        result_list.append(queue.get())

    return result_list

# Signal processing is updated
def Signal_Processing(data_in):
    data_in = data_in[10000:] # remove the first second
    rate = 1000
    N = data_in.shape[0]
    L = N / rate
    M = 10000
    slices = util.view_as_windows(data_in, window_shape=(M,), step=100)
    win = np.hanning(M + 1)[:-1]
    slices = slices * win
    slices = slices.T
    spectrum = np.fft.fft(slices, axis=0)[:M // 2 + 1:-1]
    spectrum = np.abs(spectrum)
    # f, ax = plt.subplots(figsize=(4.8, 2.4))

    S = np.abs(spectrum)
    # ================= Plotting ================
    # This part is not needed for this code ---------
    # It is plotting the spectrograms of the input signal generated from the model
    # S = 20 * np.log10(S / np.max(S))
    # ax.imshow(S[30:50], origin='lower', cmap='viridis',
    #           extent=(0, L, 0, rate / 20 ))
    # ax.axis('tight')
    # ax.set_ylabel('Frequency [kHz]')
    # ax.set_xlabel('Time [s]');
    objective = np.array([np.sum(S[40:50])])
    # objective = np.sum(abs(np.fft.fft(data_in)),axis=1)/data_in.shape[0]
    return objective

def GP_Model_BO(X,Y):
    # print('GPModelX',X.shape)
    k1 = gpflow.kernels.Matern32(2, active_dims=[0,1] , ARD=True)
    m = gpflow.gpr.GPR(X, Y, k1)
    x1=X[:,0]
    y1=X[:,1]
    m.kern.lengthscales=[np.std(x1), np.std(y1)]
    m.kern.lengthscales=np.std(x1), np.std(y1)
    m.kern.variance=np.std(Y)/np.sqrt(2)
    m.likelihood.variance=np.std(Y)/np.sqrt(2)
    return m


def optimize(data_in):
    X_final = []
    Y_final = []
    iteration =0 

    next_stim = []

    # logging.debug(f'Optimization starts here')
    print(data_in)

    Y = [list(data_in[i][0]) for i in range(len(data_in))] # Objective values
    X = [data_in[i][1] for i in range(len(data_in))] # parameter values
    print('heree1 YYY', Y)
    print('heree2 XXX', X)
    burn_in_amp = [2, 3, 8, 9, 5 ]
    burn_in_freq = [10, 35, 20,40, 25]
    # Burn-in phase:
    if X:
        if iteration<5:

            # logging.debug(f'iteratiiiiiiiiiiiiion: {iteration}')
            X_final.append(X[0])
            Y_final.append(Y[0])
            print('xxxxxxxxxxxx_final', X_final)
            print('yyyyyyyyyyyy_final', Y_final)

            # amp = np.float64(int(np.random.uniform(1,10))) + 0.1
            # freq = np.float64(int(np.random.uniform(1,45))) + 5.0
            amp = burn_in_amp[iteration]
            freq = burn_in_freq[iteration]
            iteration +=1
            next_stim = [amp, freq]


        else:
            X_final.append(X[0])
            Y_final.append(Y[0])
            print('xxxxxxxxxxxx_oppppppt', X_final)
            print('yyyyyyyyyyyy_oppppppt', Y_final)
            X_final_arr = np.array(X_final)
            Y_final_arr = np.array(Y_final)


            # train a gp model on all input data points
            gp_model=GP_Model_BO(X_final_arr, Y_final_arr)

            # ================= Plotting ================
            # Plot the mean surface of the GP model:
            xx = np.arange(0.5, 10., abs(0.5-10.)/20)
            yy = np.arange(5., 50., abs(5.-50.)/20)
            XX, YY = np.meshgrid(xx, yy)
            X_NEW=np.array(list(zip(XX.reshape(400,1).T[0],YY.reshape(400,1).T[0])))
            mean, var = gp_model.predict_y(X_NEW)

            plt.cla()
            plt.pcolor(xx,yy,mean.reshape(20,20))
            plt.xlabel('Amplitude')
            plt.ylabel('Frequency')
            plt.title('Mean of GP Model')
            fig2.canvas.draw()
            # ================================================


            def objective_function(x):
                mean, std = gp_model.predict_y(x)
                return mean
            sigma = 3.0
            alpha = LowerConfidenceBound(gp_model, sigma)
            # alpha = ExpectedImprovement(gp_model)
            domain = domain=ContinuousParameter('x1', 0.5, 10) + ContinuousParameter('x2', 5., 50.)
            acquisition_opt = StagedOptimizer([MCOptimizer(domain, 100), SciPyOptimizer(domain)])
            optimizer = BayesianOptimizer(domain, alpha, optimizer=acquisition_opt)
            # with optimizer.silent():
            r = optimizer.optimize(objective_function, n_iter=1)
            print(r)


            next_amp = alpha.data[0][-1][0]
            next_amp = np.float64((next_amp))
            next_freq = alpha.data[0][-1][1]
            next_freq = np.float64(next_freq)
            next_stim = [next_amp, next_freq]
            # ===================================================

    return next_stim

with Component() as main:
    with Component() as thread_1:
        sleep_interval = 4
        lock = threading.Lock()
        param = [1., 5.]
        iter = 0
        componentProduce('flag', False) 
        while True:
            data = MeanFieldModel(param)
            print("praram______________thread1 : ", param)
            data_out = (data,param)
            componentProduce('thread_1_out', data_out)
            time.sleep(sleep_interval)
            lock.acquire()
            iter = iter+1
            componentProduce('iter_1', iter)
            componentProduce('iter_2', iter)
            componentProduce('iter_3', iter)
            componentProduce('iter_4', iter)
            lock.release()
            if iter==100:
                break
    thread_1()
    with Component() as thread_2:
        sleep_interval = 0.5
        Flag = False
        iter = 0 
        while True:
            input_data = componentConsume('thread_1_out')
            print('insignal', input_data[0])
            threshold=100
            data_in = input_data[0][0]
            objective = Signal_Processing(data_in)
            param = [1., 5.]
            if objective.any():
                if objective[0] >= threshold:
                    new_param = param
                else:
                    # TODO: Change to 0. and 0. that corresponds to no stimulation
                    new_param = [0.1, 2.]
            data = (objective, input_data[1])
            componentProduce('thread_2_copy_data', data)
            Flag = componentConsume('flag')
            if Flag == False:
                if new_param:
                    componentProduce('thread_2_out', new_param)
            print('data-----',data)
            time.sleep(sleep_interval)
            iter = componentConsume('iter_2')
            print("iteration in thread 2 is", iter)
            if iter==100:
                break 
    thread_2()
    with Component() as thread_3:
        sleep_interval2 = 2
        inter_interval = 2
        Flag = False
        param = []
        while True:
            if thread_2_out.empty()==False:
                param = componentConsume('thread_2_out')
            componentProduce('flag', True)
            out = param
            print("out param in thread3 is", out)
            time.sleep(inter_interval)
            componentProduce('flag', False)  
            try:
                iter = componentConsume('iter_3')
                print("iteration in thread3", iter)
                if iter==100:
                    break
            except Queue.Empty:
                pass
    thread_3()
    with Component() as thread_4:
        sleep_interval = 2
        iter =0 
        while True:
            input_data = []
            try:
                val = componentConsume('thread_2_copy_data')
                input_data.append(val)
            except Queue.Empty:
                pass
            print('thread4-------------input', input_data)
            opt_data_out = optimize(input_data)
            if opt_data_out:
                thread_2_out.queue.clear()
                componentProduce('thread_2_out', opt_data_out)
            try:
                iter = componentConsume('iter_4')
                print("iteration in thread4", iter)
                if iter==100:
                    break
            except Queue.Empty:
                pass
    thread_4()

main()