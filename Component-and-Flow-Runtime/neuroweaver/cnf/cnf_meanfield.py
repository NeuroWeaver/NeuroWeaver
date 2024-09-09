import matplotlib.pyplot as plt

import threading
import time
# import logging

from queue import Queue
from random import randint
from threading import Lock
from collections import deque

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


import pickle

from pathlib import Path

import ohai.digital_signal_processing as dsp



global iteration

X_final=[]
Y_final=[]
iteration = 0

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


def custom_logic(data):
    """Custom logic used by Thread 4 to put its data in Buffer 2."""
    f = open('new_param', 'wb')
    pickle.dump(data, f)
    f.close()


def get_all_queue_result():
    result_list = []
    copy_data_file = Path('copy_data')
    while not copy_data_file.is_file():
        pass

    f = open('copy_data', 'r+b')
    while True:
        print('PLEASE')
        try:
            data = pickle.load(f)
            print('PLEASE: ', data)
        except EOFError:
            break
        result_list.append(data)
    f.close()
    f = open('copy_data', 'wb')
    f.write(b'')
    f.close()
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
    with Component(outputs=[data_out]) as thread_1:
        sleep_interval = 4  # seconds
        f = open('param', 'rb')
        param = pickle.load(f)
        f.close()
        data = MeanFieldModel(param)
        print('param______________thread1 : ', param)
        data_out = (data,param)
        f = open('thread_1_data_out', 'a')
        f.write(str(data_out) + '\n')
        f.close()
        time.sleep(sleep_interval)
    data_out = thread_1()
    with Component() as thread_2_wrapper:
        with Component(inputs=[input_data], outputs=[out_data]) as thread_2_sub1:
            print('in signal', input_data[0])
            f = open('thread_2_sub1_input_data', 'a')
            f.write(str(input_data[0]) + '\n')
            f.close()
            out_data = input_data[0][0]
        out_data = thread_2_sub1(data_out)
        with Component(inputs=[data_in], outputs=[slices]) as Signal_Processing:
            data_in = data_in[10000:] # remove the first second
            rate = 1000
            N = data_in.shape[0]
            L = N / rate
            M = 10000
            slices = util.view_as_windows(data_in, window_shape=(M,), step=100)
            win = np.hanning(M + 1)[:-1]
            slices = slices * win
            slices = slices.T
            f= open('Signal_Processing_slices', 'a')
            f.write(str(slices) + '\n')
            f.close()
        slices = Signal_Processing(out_data)
        fft_out = dsp.fft(slices)
        with Component(inputs=[fft_out, input_data]) as post_processing:
            sleep_interval = 0.5
            threshold = 100 # a predefined threshold
            M = 10000
            spectrum = fft_out[:M // 2 + 1:-1]
            spectrum = np.abs(spectrum)
            S = np.abs(spectrum)
            objective = np.array([np.sum(S[40:50])])
            print('thread2-----------objectiiiiiiiive',objective)
            f = open('param', 'rb')
            param = pickle.load(f)
            f.close()
            if objective.any():
                if objective[0] >= threshold:
                    new_param = param
                else:
                    new_param = [0.1, 2.]
            copy_data = (objective, input_data[1])
            f = open('copy_data', 'ab')
            pickle.dump(copy_data, f)
            f.close()
            f = open('Flag', 'rb')
            Flag = pickle.load(f)
            f.close()
            Flag = False
            if Flag == False:
                if new_param:
                    f = open('new_param', 'ab')
                    print(f'FUCK NEW PARAM: {new_param}')
                    pickle.dump(new_param, f)
                    f.close()
            print('----------------',copy_data)
            time.sleep(sleep_interval)
        post_processing(fft_out, data_out)
    thread_2_wrapper()
    with Component() as thread_3:
        sleep_interval2 = 2
        inter_interval = 2
        new_param_file = Path('new_param')
        while not new_param_file.is_file():
            pass
        f = open('new_param', 'r+b')
        objs = []
        while True:
            try:
                o = pickle.load(f)
            except EOFError:
                break
            objs.append(o)
        while len(objs) == 0:
            pass
        param = objs.pop(0)
        f.seek(0)
        for o in objs:
            pickle.dump(o, f)
        f.truncate()
        f.close()
        f = open('param', 'wb')
        print(f'FUCK thread3: param {param}')
        pickle.dump(param, f)
        f.close()
        Flag = True
        f = open('Flag', 'wb')
        pickle.dump(Flag, f)
        f.close()
        time.sleep(sleep_interval2)
        time.sleep(inter_interval)
        Flag = False
        f =  open('Flag', 'wb')
        pickle.dump(Flag, f)
        f.close()
        f = open('thread_3_Flag', 'a')
        f.write(str(Flag) + '\n')
        f.close()
    thread_3()
    with Component() as thread_4:
        sleep_interval = 2
        while True:
            input_data = get_all_queue_result()
            print('thread4-------------input', input_data)
            opt_data_out = optimize(input_data)
            print(f'FUCK OPT DATA OUT: {opt_data_out}')
            if opt_data_out:
                custom_logic(opt_data_out)
            time.sleep(sleep_interval)
    thread_4()
main()
