import threading
import time
import logging

import numpy as np

from queue import Queue
from random import randint
from threading import Lock
from collections import deque

import gpflow
from gpflowopt.domain import ContinuousParameter
from gpflowopt.bo import BayesianOptimizer
from gpflowopt.acquisition import LowerConfidenceBound
from gpflowopt.optim import SciPyOptimizer, StagedOptimizer, MCOptimizer

import ohai.analytics as analytics


# Thread-safe logging utility for debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)-15s [%(levelname)s] (%(threadName)-10s) %(message)s',
)

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
    #sig = dsp.fft(data_in)
    #print(f'DEBUG {sig}')
    #objective = np.sum(abs(sig), axis=1)
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
    logging.debug(f'Optimization starts here')
    print(data_in)
    next_stim = 0.
    Y2 = [[data_in[i][0]] for i in range(len(data_in))] # Objective values
    X2 = [[data_in[i][1]] for i in range(len(data_in))] # parameter values

    print('XXXXXXXXX', X2)
    print('YYYYYYYYY',Y2)

    Y1 = [[0.2], [0.8], [0.9], [0.4]] #initial values in burning phase
    X1 = [[0.], [60.], [50.], [20.]] #initial values in burning phase
    if not main.X:
        if X2:
            main.X = X1+X2
            main.Y = Y1+Y2
        else:
            main.X = main.X + X1
            main.Y = main.Y + Y1

    else:
        if X2:
            main.X = main.X+X2
            main.Y = main.Y+Y2
        else:
            main.X = main.X
            main.Y = main.Y

    print('XXXXXXXXX', main.X)
    print('YYYYYYYYY', main.Y)
    X_final = np.array(main.X).reshape(1,-1)
    Y_final = np.array(main.Y)
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



with Component() as main:
    param = 8. # initial value for parameter(frequency)
    Flag = False
    X = []
    Y = []
    counter = 0
    buffer_1 = Queue()
    buffer_1_copy = Queue()
    buffer_2 = Queue()
    with Component() as thread_1:
        sleep_interval = 0.5  # seconds
        n_rows = 1
        n_cols = 1
        while True:
            data = np.random.uniform(0, 1, (n_rows, n_cols))
            logging.debug(f'Thread 1: generated random data: \n{data}')
            main.buffer_1.put(data)
            logging.debug(f'Thread 1 DEBUG: {id(main.buffer_1)}')
            time.sleep(sleep_interval)
    thread_1()
    with Component() as thread_2:
        sleep_interval = 2
        threshold = 0.5 # a predefined threshold
        while True:
            logging.debug(f'Thread 2 DEBUG: {id(main.buffer_1)}')
            input_data = main.buffer_1.get()
            logging.debug(f'Thread 2: data read from Buffer 1: \n{input_data}')
            objective = Signal_Processing(input_data)
            print('objectiiiiiiiive',objective)
            if not objective:
                if objective >= threshold:
                    main.param = main.param
                else:
                    main.param = 0.
            data = (objective, main.param)
            main.buffer_1_copy.put(data)
            logging.debug(f'Thread 2: copied data to Buffer 1 Copy: \n{data}')
            logging.debug(f'Thread 2: out data: \n{data}')
            if main.Flag == False:
                logging.debug(f'FLAAAAAAG: \n{main.Flag}')
                main.buffer_2.put(main.param)
            time.sleep(sleep_interval)
    thread_2()
    with Component() as thread_3:
        sleep_interval2 = 5
        inter_interval = 5
        while True:
            logging.debug(f'Thread 3: Buffer 2 contents before reading: {list(main.buffer_2.queue)}')
            main.param = main.buffer_2.get()
            main.Flag = True
            logging.debug(f'Thread 3: data read from Buffer 2: \n{main.param}')
            out = main.param
            logging.debug(f'Thread 3: out data: \n{out}')
            logging.debug(f'Thread 3: lock buffer 2')
            logging.debug(f'FLAAAAAAG 333333333: \n{main.Flag}')
            # TODO: The next line must be substituted with the actual writting part
            time.sleep(sleep_interval2)
            # reset the param to 0 after writing and for the inter-interval period
            main.param = 0.
            time.sleep(inter_interval)
            main.Flag = False
    thread_3()
    with Component() as thread_4:
        sleep_interval = 0.5
        while True:
            logging.debug(f'Thread 4: Buffer 1 Copy contents before reading: {list(main.buffer_1_copy.queue)}')
            input_data = get_all_queue_result(main.buffer_1_copy)
            logging.debug(f'Thread 4: data read from Buffer 1 Copy: \n{input_data}')
            logging.debug(f'Thread 4: Buffer 1 Copy contents after reading: {list(main.buffer_1_copy.queue)}')
            opt_data_out = optimize(input_data)
            logging.debug(f'Thread 4: opt_data_out data: \n{opt_data_out}')
            custom_logic(main.buffer_2, opt_data_out)
            logging.debug(f'Thread 4: Buffer 2 contents after writing: {list(main.buffer_2.queue)}')
            time.sleep(sleep_interval)
    thread_4()


main()
