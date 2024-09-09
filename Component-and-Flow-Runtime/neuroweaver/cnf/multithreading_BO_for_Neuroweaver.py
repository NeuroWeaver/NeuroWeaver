#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 23:58:57 2020

@author: psarikh
"""


import threading
import time
import logging

import numpy as np
import sys

from queue import Queue
from random import randint
from threading import Lock
from collections import deque

import gpflow
from gpflowopt.domain import ContinuousParameter
from gpflowopt.bo import BayesianOptimizer
from gpflowopt.acquisition import LowerConfidenceBound
from gpflowopt.optim import SciPyOptimizer, StagedOptimizer, MCOptimizer
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"




file_handler = logging.FileHandler(filename='cnf_meanfield_mt_runtime.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]
# Thread-safe logging utility for debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)-15s [%(levelname)s] (%(threadName)-10s) %(message)s',
    handlers=handlers
)

param = 8. # initial value for parameter(frequency)
Flag = False
X = []
Y = []
counter = 0 
total_iterations = 50
terminate = False
# Thread 1: Data generator
# Generates random data every iteration
def thread_1(output_q):
    logging.debug('thread 1 starting...')
    sleep_interval = 0.5  # seconds
    n_rows = 1
    n_cols = 1
    global terminate
    iteration = 0
    while True:
        iteration_start_time = time.time()
        data = np.random.uniform(0, 1, (n_rows, n_cols))
        logging.debug(f'generated random data: {data}')
        output_q.put(data)

        logging.debug(f'wrote data to Buffer 1')
        logging.debug(f'sleep for {sleep_interval} seconds...')
        time.sleep(sleep_interval)
        iteration += 1
        logging.debug(f'Iteration {iteration} time {time.time() - iteration_start_time} seconds')    
        if terminate:
            break
    logging.debug('thread 1 ending...')

# Thread 2: Signal processing
# Every iteration processes data from thread 1, creates copy of original data
def thread_2(input_q, output_q, copy_q):
    logging.debug('thread 2 starting...')
    sleep_interval = 2
    threshold = 0.5 # a predefined threshold
    global param
    global Flag
    global terminate
    iteration = 0
    while True:
        iteration_start_time = time.time()
        input_data = input_q.get()
        logging.debug(f'data read from Buffer 1: {input_data}')
        objective = Signal_Processing(input_data)
        print('objective',objective)
#        local_param = randint(0, 10)
        if not objective:
            if objective >= threshold:
                param = param
            else:
                param = 0.

        data = (objective, param)
        copy_q.put(data)
    
        logging.debug(f'copied data to Buffer 1 Copy: {data}')

        logging.debug(f'out data: {data}')
        
        if Flag == False:
            logging.debug(f'FLAG: {Flag}')
            output_q.put(param)
            logging.debug(f'wrote out data to Buffer 2')
        

        #logging.debug(f'Buffer 2 contents after writing: {list(output_q.queue)}')
        time.sleep(sleep_interval)
        iteration += 1
        logging.debug(f'Iteration {iteration} time {time.time() - iteration_start_time} seconds')    
        if terminate:
            break
    logging.debug('thread 2 ending...')

def thread_3(input_q):
    logging.debug('thread 3 starting...')
    sleep_interval2 = 5
    inter_interval = 5
    global Flag
    global param
    global terminate
    iteration = 0
    while True:
        iteration_start_time = time.time()
        logging.debug(f'Buffer 2 contents before reading: {list(input_q.queue)}')
        
#        data = input_q.get()
        param = input_q.get()
        Flag = True
        logging.debug(f'data read from Buffer 2: {param}')

        out = param
        logging.debug(f'out data: {out}')
        logging.debug(f'lock buffer 2')
        logging.debug(f'FLAG thread 3: {Flag}')
        # TODO: The next line must be substituted with the actual writting part
        time.sleep(sleep_interval2) 
        # reset the param to 0 after writing and for the inter-interval period
        param = 0.
        time.sleep(inter_interval)
        Flag = False 
        logging.debug(f'release buffer 2')
        iteration += 1
        logging.debug(f'Iteration {iteration} time {time.time() - iteration_start_time} seconds')    
        if  terminate:
            break
    logging.debug('thread 3 ending...')

def thread_4(input_q, output_q):
    logging.debug('thread 4 starting...')
    sleep_interval = 0.5
    global Flag
    global X
    global Y
    global terminate
    iteration = 0
    while True:
        iteration_start_time = time.time()
        logging.debug(f'Buffer 1 Copy contents before reading: {list(input_q.queue)}')
        # input_data = input_q.get()
        input_data = get_all_queue_result(input_q)
        logging.debug(f'data read from Buffer 1 Copy: {input_data}')
        logging.debug(f'Buffer 1 Copy contents after reading: {list(input_q.queue)}')
#        opt_data_out =11   #just a test
#        output_q.put(opt_data_out)
        opt_data_out = optimize(input_data)
        logging.debug(f'opt_data_out data: {opt_data_out}')
    
        custom_logic(output_q, opt_data_out)
        logging.debug(f'wrote out data to Buffer 2')
        logging.debug(f'Buffer 2 contents after writing: {list(output_q.queue)}')
            
        time.sleep(sleep_interval)
        iteration += 1
        logging.debug(f'Iteration {iteration} time {time.time() - iteration_start_time} seconds')    
        if iteration == total_iterations:
            break
    terminate = True
    logging.debug('thread 4 ending...')







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
    objective = np.sum(abs(np.fft.fft(data_in)),axis=1)
    return objective[0]



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
    global X
    global Y

    logging.debug(f'Optimization starts here')
    print(data_in)
    next_stim = 0.
    Y2 = [[data_in[i][0]] for i in range(len(data_in))] # Objective values
    X2 = [[data_in[i][1]] for i in range(len(data_in))] # parameter values
    
    print('XXXXXXXXX', X2)
    print('YYYYYYYYY',Y2)
    
    Y1 = [[0.2], [0.8], [0.9], [0.4]] #initial values in burning phase
    X1 = [[0.], [60.], [50.], [20.]] #initial values in burning phase
    if not X:
        if X2:
            X = X1+X2
            Y = Y1+Y2
        else:
            X = X + X1
            Y = Y + Y1
            
    else:
        if X2:
            X = X+X2
            Y = Y+Y2
        else:
            X = X 
            Y = Y 
        
    print('XXXXXXXXX', X)
    print('YYYYYYYYY',Y)
    X_final = np.array(X).reshape(1,-1)
    Y_final = np.array(Y)
    # train a gp model on all input data points
    model=GP_Model_BO(X_final.T, Y_final.T)
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
