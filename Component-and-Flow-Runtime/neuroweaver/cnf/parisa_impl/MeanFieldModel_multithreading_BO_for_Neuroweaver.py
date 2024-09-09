#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is combining
@author: psarikh
"""
import os
#os.chdir('/home/psarikh/Downloads/neurolib') # Change this path

import matplotlib.pyplot as plt

import threading
import time
# import logging

import numpy as np

from queue import Queue
from random import randint
from threading import Lock
from collections import deque

import numpy as np
import scipy
import time
import threading
# import logging

from random import randint
import tensorflow as tf
import gpflow
from gpflowopt.domain import ContinuousParameter
from gpflowopt.bo import BayesianOptimizer
from gpflowopt.acquisition import LowerConfidenceBound, ExpectedImprovement
from gpflowopt.optim import SciPyOptimizer, StagedOptimizer, MCOptimizer
from pyDOE import *
import random
# Let's import the aln model
from neurolib.models.aln import ALNModel
# Some useful functions are provided here
import neurolib.utils.functions as func

from functools import partial
import numpy as np

from neurolib.models.aln import ALNModel
from neurolib.utils.loadData import Dataset
from neurolib.utils.signal import RatesSignal, BOLDSignal
import matplotlib.pyplot as plt

global iteration

from matplotlib.animation import FuncAnimation
plt.ion()


# ================= Plotting ================
fig = plt.figure(1)
fig2 = plt.figure(2)

ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

fig.canvas.draw()
fig2.canvas.draw()

xdata, ydata = [], []

X_final=[]
Y_final=[]
# ==========================================


iteration = 0
plt.rcParams['image.cmap'] = 'plasma'
# =======================
# Function to generate data: This is based on the mean-field model and a surrogate of the random number generator
# the parameters of the model are updated
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






# =========================== Multithreading =================================
# Thread-safe logging utility for debugging
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)-15s [%(levelname)s] (%(threadName)-10s) %(message)s',
# )

param = [1., 5.] # initial value for parameter
Flag = False
X = []
Y = []
counter = 0
def thread_1(output_q):
    # logging.debug('thread starting...')
    sleep_interval = 4  # seconds
    global param
    while True:
        data = MeanFieldModel(param)
        # data = np.random.uniform(0, 1, (n_rows, n_cols))
        # logging.debug(f'generated random data: \n{data}')
        print('param______________thread1 : ', param)
        data_out = (data,param)
        output_q.put(data_out)

        # logging.debug(f'wrote data to Buffer 1')
        # logging.debug(f'sleep for {sleep_interval} seconds...')
        time.sleep(sleep_interval)
    # logging.debug('thread ending...')

def thread_2(input_q, output_q, copy_q):
    # logging.debug('thread starting...')
    sleep_interval = 0.5
    threshold = 100 # a predefined threshold
    global param
    global Flag
    while True:
        input_data = input_q.get()
        # logging.debug(f'data read from Buffer 1: \n{input_data}')
        print('in signal', input_data[0])
        objective = Signal_Processing(input_data[0][0])
        print('thread2-----------objectiiiiiiiive',objective)
#        local_param = randint(0, 10)
        if objective.any():
            if objective[0] >= threshold:
                new_param = param
            else:
                # TODO: Change to 0. and 0. that corresponds to no stimulation
                new_param = [0.1, 2.]

        data = (objective, input_data[1])
        copy_q.put(data)

        # logging.debug(f'copied data to Buffer 1 Copy: \n{data}')

        # logging.debug(f'out data: \n{data}')

        if Flag == False:
            # logging.debug(f'FLAAAAAAG: \n{Flag}')
            if new_param:
                output_q.put(new_param)
            # else:
            #     output_q.put(param)
            # logging.debug(f'wrote out data to Buffer 2')

        print('----------------',data)
        #logging.debug(f'Buffer 2 contents after writing: {list(output_q.queue)}')
        time.sleep(sleep_interval)
        # logging.debug('thread ending...')

def thread_3(input_q):
    # logging.debug('thread starting...')
    sleep_interval2 = 2
    inter_interval = 2
    global Flag
    global param
    while True:
        # logging.debug(f'Buffer 2 contents before reading: {list(input_q.queue)}')

#        data = input_q.get()
        param = input_q.get()
        Flag = True
        # logging.debug(f'data read from Buffer 2: \n{param}')

        out = param
        # logging.debug(f'out data: \n{out}')
        # logging.debug(f'lock buffer 2')
        # logging.debug(f'FLAAAAAAG 333333333: \n{Flag}')
        # TODO: The next line must be substituted with the actual writting part
        time.sleep(sleep_interval2)
        # reset the param to 0 after writing and for the inter-interval period
        # TODO: return to 0
        #param = [0.1, 2]
        time.sleep(inter_interval)
        Flag = False
    #     logging.debug(f'release buffer 2')
    # logging.debug('thread ending...')

def thread_4(input_q, output_q):

    # logging.debug('thread starting...')
    sleep_interval = 2
    global Flag
    global X
    global Y
    while True:
        # logging.debug(f'Buffer 1 Copy contents before reading: {list(input_q.queue)}')
        # input_data = input_q.get()
        input_data = get_all_queue_result(input_q)
        print('thread4-------------input', input_data)
        # logging.debug(f'data read from Buffer 1 Copy: \n{input_data}')
        # logging.debug(f'Buffer 1 Copy contents after reading: {list(input_q.queue)}')
#        opt_data_out =11   #just a test
#        output_q.put(opt_data_out)
        opt_data_out = optimize(input_data)
        # logging.debug(f'opt_data_out data: \n{opt_data_out}')
        if opt_data_out:
            custom_logic(output_q, opt_data_out)
            # logging.debug(f'wrote out data to Buffer 2')
            # logging.debug(f'Buffer 2 contents after writing: {list(output_q.queue)}')

        time.sleep(sleep_interval)
    # logging.debug('thread ending...')



def custom_logic(buffer2, data):
    """Custom logic used by Thread 4 to put its data in Buffer 2."""
    with Lock() as lock:
        buffer2.queue.clear()
        buffer2.put(data)


def get_all_queue_result(queue):

    result_list = []
    while not queue.empty():
        result_list.append(queue.get())

    return result_list

from skimage import util
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

# ========================

def optimize(data_in):
    global X_final
    global Y_final
    global iteration

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

            # ================= Plotting ================
            # Plot the objective and the selected stimulation parameters by the optimizer
            x_data = np.arange(len(Y_final))
            y_data = np.maximum.accumulate(np.transpose(Y_final)[0])

            ax1.cla()
            ax1.plot(x_data, y_data, lw =2)
            ax1.set_xlabel('Iteration')
            ax1.set_ylabel('Objective')

            ax2.cla()
            ax2.plot(x_data, np.transpose(X_final)[0], lw =2, c = 'g')
            ax2.set_xlabel('Iteration')
            ax2.set_ylabel('Amplitude')

            ax3.cla()
            ax3.plot(x_data, np.transpose(X_final)[1], lw =2, c = 'r')
            ax3.set_xlabel('Iteration')
            ax3.set_ylabel('Frequency')
            plt.draw()
            # plt.pause(0.05)
            # plt.show()
            fig.canvas.draw()

            next_amp = alpha.data[0][-1][0]
            next_amp = np.float64((next_amp))
            next_freq = alpha.data[0][-1][1]
            next_freq = np.float64(next_freq)
            next_stim = [next_amp, next_freq]
            # ===================================================

    return next_stim




def main():
    # Buffer between Thread 1 and Thread 2
    buffer_1 = Queue()
    # Copy of Buffer 1
    buffer_1_copy = Queue()
    # Buffer read by Thread 3, written by Thread 2 and 4
    buffer_2 = Queue()

    thread_1_thread = threading.Thread(name='Thread 1',
                                       target=thread_1,
                                       args=(buffer_1,))
    thread_2_thread = threading.Thread(name='Thread 2',
                                       target=thread_2,
                                       args=(buffer_1, buffer_2, buffer_1_copy))
    thread_3_thread = threading.Thread(name='Thread 3',
                                       target=thread_3,
                                       args=(buffer_2,))
    thread_4_thread = threading.Thread(name='Thread 4',
                                        target=thread_4,
                                        args=(buffer_1_copy, buffer_2))
    thread_1_thread.start()
    thread_2_thread.start()
    thread_3_thread.start()
    thread_4_thread.start()


if __name__ == '__main__':
    main()
