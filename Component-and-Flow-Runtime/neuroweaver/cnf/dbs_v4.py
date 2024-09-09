import numpy as np
from random import randint
from time import sleep

import ohai.digital_signal_processing as dsp

import gpflow
from gpflowopt.domain import ContinuousParameter
from gpflowopt.bo import BayesianOptimizer
from gpflowopt.acquisition import LowerConfidenceBound
from gpflowopt.optim import SciPyOptimizer, StagedOptimizer, MCOptimizer


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


with Component(outputs=[all_data]) as burn_in:
    all_data = []
    for i in range(5):
        data = np.random.uniform(0, 1, (1, 100))
        data_param = (data,np.float64(randint(0, 100)))
        signal = data_param[0]
        param = data_param[1]
        fft_out = dsp.fft(signal)
        objective = np.sum(abs(fft_out),axis=1)
        obj_param = (objective, param)
        all_data.append(obj_param)

with Component(inputs=[data_in], outputs=[next_stim]) as optimize:
    Y = np.array([list(data_in[i][0]) for i in range(len(data_in))]) # Objective values
    X = np.array([data_in[i][1] for i in range(len(data_in))]).reshape(1,-1) # parameter values
    model = GP_Model_BO(X.T, Y.T)
    def objective_function(x):
        mean, std = model.predict_y(x)
        return mean
    sigma = 3.0
    alpha = LowerConfidenceBound(model, sigma)
    domain = ContinuousParameter('X', 0, 100)
    acquisition_opt = StagedOptimizer([MCOptimizer(domain, 100), SciPyOptimizer(domain)])
    optimizer = BayesianOptimizer(domain, alpha, optimizer=acquisition_opt)
    r = optimizer.optimize(objective_function, n_iter=1)
    next_stim = alpha.data[0][-1][0]
    next_stim = np.float64(int(next_stim))

with Component(inputs=[next_control_param], outputs=[signal, param]) as data_gen:
    data = np.random.uniform(0, 1, (1, 100))
    data_param = (data,np.float64(randint(0, 100)))
    signal = data_param[0]
    param = data_param[1]

with Component(inputs=[signal, param], outputs=[all_data]) as signal_processing:
    fft_out = dsp.fft(signal)
    objective = np.sum(abs(fft_out),axis=1)
    obj_param = (objective, param)
    all_data.append(obj_param)


all_data = burn_in()
while True:
    next_control_param = optimize(all_data)
    signal, param = data_gen(next_control_param)
    signal_processing(signal, param)
