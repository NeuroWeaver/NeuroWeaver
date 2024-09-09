import numpy as np
from random import randint
from time import sleep

import ohai.digital_signal_processing as dsp

import gpflow
from gpflowopt.domain import ContinuousParameter
from gpflowopt.bo import BayesianOptimizer
from gpflowopt.acquisition import LowerConfidenceBound
from gpflowopt.optim import SciPyOptimizer, StagedOptimizer, MCOptimizer


with Component(outputs=[all_data]) as init:
    n_rows =1
    n_cols = 100
    param = np.float64(randint(0, 100))
    all_data = []

with Component(outputs=[data_param]) as data_generator:
    data = np.random.uniform(0, 1, (1, 100))
    data_param = (data,np.float64(randint(0, 100)))

with Component(inputs=[data_in], outputs=[signal, param]) as parse:
    signal = data_in[0]
    param = data_in[1]

with Component(inputs=[fft_out, param], outputs=[all_data], state=[all_data]) as produce:
    objective = np.sum(abs(fft_out),axis=1)
    obj_param = (objective, param)
    all_data.append(obj_param)
    print(all_data)

with Component(inputs=[data_in], outputs=[X, Y]) as gen_params:
    Y = np.array([list(data_in[i][0]) for i in range(len(data_in))]) # Objective values
    X = np.array([data_in[i][1] for i in range(len(data_in))]).reshape(1,-1) # parameter values

with Component(inputs=[X, Y], outputs=[m]) as GP_Model_BO:
    k1 = gpflow.kernels.Matern32(1, active_dims=[0], ARD=True)
    m = gpflow.gpr.GPR(X, Y.T, k1)
    m.kern.lengthscales = np.std(X)
    m.kern.lengthscales = np.std(X)
    m.kern.variance = np.std(Y) / np.sqrt(2)
    m.likelihood.variance = np.std(Y) / np.sqrt(2)

with Component(inputs=[model], outputs=[next_stim]) as gp_opt:
    sigma = 3.0
    alpha = LowerConfidenceBound(model, sigma)
    domain = ContinuousParameter('X', 0, 100)
    acquisition_opt = StagedOptimizer([MCOptimizer(domain, 100), SciPyOptimizer(domain)])
    BayesianOptimizer(domain, alpha, optimizer=acquisition_opt)
    def objective_function(x):
        mean, std = model.predict_y(x)
        return mean
    r = optimizer.optimize(objective_function, n_iter=1)
    next_stim = alpha.data[0][-1][0]
    next_stim = np.float64(int(next_stim))


all_data = init()
for i in range(5):
    data_param = data_generator()
    signal, param = parse(data_param)
    data_out_signal = dsp.fft(signal)
    out_data = produce(data_out_signal, param, all_data)
X, Y = gen_params(out_data)
model = GP_Model_BO(X, Y)
next_control_param = gp_opt(model)
