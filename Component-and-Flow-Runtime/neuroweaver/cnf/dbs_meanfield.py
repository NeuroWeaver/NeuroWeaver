import os
#os.chdir('/home/joon/.local/lib/python3.6/site-packages') # Change this path

import threading
import time
import logging

import numpy as np

from queue import Queue
from random import randint
from threading import Lock
from collections import deque
import random
from random import randint

from functools import partial

import gpflow
from gpflowopt.domain import ContinuousParameter
from gpflowopt.bo import BayesianOptimizer
from gpflowopt.acquisition import LowerConfidenceBound
from gpflowopt.optim import SciPyOptimizer, StagedOptimizer, MCOptimizer

from pyDOE import *

from functools import partial
import neurolib.utils.functions as func
from neurolib.models.aln import ALNModel
from neurolib.utils.loadData import Dataset
from neurolib.utils.signal import RatesSignal, BOLDSignal
import matplotlib as plt

import scipy


from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

from skimage import util


# Thread-safe logging utility for debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)-15s [%(levelname)s] (%(threadName)-10s) %(message)s',
)

plt.rcParams['image.cmap'] = 'plasma'
# =======================
# Function to generate data: This is based on the mean-field model and a surrogate of the random number generator
def MeanFieldModel(X):
    stim_amp = X[0]
    stim_freq = X[1]
    model = ALNModel()
    model.params['duration'] = 2 * 1000 # time duration in ms
    model.params['sigma_ou'] = 0.0 # we add some noise
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
        buffer2.queue.clear()
        buffer2.put(data)

# Following functions are compute kernels used by each thread above
def fft(data_in):
    return np.fft.fft(data_in)

def model_fit(data_in):
    # TODO provide specific kernel implementation for model fit
    return data_in * 2

def control_opt(data_in_1, data_in_2):
    # TODO provide specific kernel implementation for model fit
    return data_in_1 * 10

def get_all_queue_result(queue):
    result_list = []
    while not queue.empty():
        result_list.append(queue.get())
    return result_list

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

    #objective = np.sum(abs(np.fft.fft(data_in)),axis=1)/data_in.shape[0]
    #sig = dsp.fft(data_in)
    #print(f'DEBUG {sig}')
    #objective = np.sum(abs(sig), axis=1)
    return objective

# GP model
def GP_Model_BO(X, Y):
    k1 = gpflow.kernels.Matern32(2, active_dims=[0, 1], ARD=True)
    m = gpflow.gpr.GPR(X, Y, k1)
    x1=X[:,0]
    y1=X[:,1]
    m.kern.lengthscales=[np.std(x1), np.std(y1)]
    m.kern.lengthscales=np.std(x1), np.std(y1)
    m.kern.variance=np.std(Y)/np.sqrt(2)
    m.likelihood.variance=np.std(Y)/np.sqrt(2)

    return m


def optimize(data_in):
    next_stim = []

    logging.debug(f'Optimization starts here')
    print(data_in)

    Y = [list(data_in[i][0]) for i in range(len(data_in))] # Objective values
    X = [data_in[i][1] for i in range(len(data_in))] # parameter values

    # Burn-in phase:
    if X:
        if main.iteration<5:
            main.iteration +=1
            logging.debug(f'iteratiiiiiiiiiiiiion: {main.iteration}')
            main.X_final.append(X[0])
            main.Y_final.append(Y[0])
            print('xxxxxxxxxxxx_final', main.X_final)
            print('yyyyyyyyyyyy_final', main.Y_final)
            amp = np.float64(int(np.random.uniform(1,10))) + 0.1
            freq = np.float64(int(np.random.uniform(1,45))) + 5.0
            next_stim = [amp, freq]


        else:
            main.X_final.append(X[0])
            main.Y_final.append(Y[0])
            print('xxxxxxxxxxxx_oppppppt', main.X_final)
            print('yyyyyyyyyyyy_oppppppt', main.Y_final)
            X_final_arr = np.array(main.X_final)
            Y_final_arr = np.array(main.Y_final)

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

            # next_amp = alpha.data[0][-1][0]
            # next_amp = np.float64(int(next_amp))
            # next_freq = alpha.data[0][-1][1]
            # next_freq = np.float64(int(next_freq))
            # next_stim = [next_amp, next_freq]

    return next_stim






with Component() as main:
    param = [1., 5.] # initial value for parameter(frequency)
    Flag = False
    X = []
    Y = []
    counter = 0
    X_final = []
    Y_final = []
    iteration = 0
    buffer_1 = Queue()
    buffer_1_copy = Queue()
    buffer_2 = Queue()
    plt.ion()
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
    with Component() as thread_1:
        sleep_interval = 4  # seconds
        while True:
            data = MeanFieldModel(main.param)
            data_out = (data, main.param)
            main.buffer_1.put(data_out)
            time.sleep(sleep_interval)
    thread_1()
    with Component() as thread_2:
        sleep_interval = 0.5
        threshold = 100 # a predefined threshold
        while True:
            logging.debug(f'Thread 2 DEBUG: {main.buffer_1}')
            input_data = main.buffer_1.get()
            logging.debug(f'Thread 2: data read from Buffer 1: \n{input_data}')
            objective = Signal_Processing(input_data[0])
            print('objectiiiiiiiive',objective)
            if objective.any():
                if objective[0] >= threshold:
                    new_param = main.param
                else:
                    new_param = [0.1, 2.]
            data = (objective, input_data[1])
            main.buffer_1_copy.put(data)
            print(f't2: main.Flag = {main.Flag}')
            if main.Flag == False:
                logging.debug(f'FLAAAAAAG: \n{main.Flag}')
                if new_param:
                    main.buffer_2.put(new_param)
            time.sleep(sleep_interval)
    thread_2()
    with Component() as thread_3:
        sleep_interval2 = 2
        inter_interval = 2
        while True:
            logging.debug(f'Thread 3: Buffer 2 contents before reading: {list(main.buffer_2.queue)}')
            main.param = main.buffer_2.get()
            main.Flag = True
            logging.debug(f'Thread 3: data read from Buffer 2: \n{main.param}')
            out = main.param
            logging.debug(f'Thread 3: out data: \n{out}')
            logging.debug(f'Thread 3: lock buffer 2')
            logging.debug(f'FLAAAAAAG 333333333: \n{main.Flag}')
            time.sleep(sleep_interval2)
            time.sleep(inter_interval)
            main.Flag = False
    thread_3()
    with Component() as thread_4:
        sleep_interval = 2
        while True:
            logging.debug(f'Thread 4: Buffer 1 Copy contents before reading: {list(main.buffer_1_copy.queue)}')
            input_data = get_all_queue_result(main.buffer_1_copy)
            logging.debug(f'Thread 4: data read from Buffer 1 Copy: \n{input_data}')
            logging.debug(f'Thread 4: Buffer 1 Copy contents after reading: {list(main.buffer_1_copy.queue)}')
            opt_data_out = optimize(input_data)
            if opt_data_out:
                logging.debug(f'Thread 4: opt_data_out data: \n{opt_data_out}')
                custom_logic(main.buffer_2, opt_data_out)
                logging.debug(f'Thread 4: Buffer 2 contents after writing: {list(main.buffer_2.queue)}')
            time.sleep(sleep_interval)
    thread_4()


main()
