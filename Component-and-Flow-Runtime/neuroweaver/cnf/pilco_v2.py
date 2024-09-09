import numpy as np
import gym
from pilco.models import PILCO
from pilco.controllers import RbfController, LinearController
from pilco.rewards import ExponentialReward
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt
from utils import rollout, policy
from gpflow import set_trainable
import gym
import gym_oscillator
import oscillator_cpp
import threading
import time
from queue import Queue
from random import randint
from threading import Lock
from collections import deque
from functools import partial
import os
import pickle



with Component() as main:
    with Component() as thread_1:
        np.random.seed(0)
        env_id = 'oscillator-v0'
        env = gym.make(env_id)
        env.reset()
        sleep_interval = 0.1  # seconds
        n_burn_in = 20
        iteration = 0
        while True:
            iteration_start_time = time.time() 
            if iteration ==0:
                iteration +=1
                X,Y, _, _, all_states,_ = rollout(env, None, timesteps=1, verbose=False, random=True, SUBS=1, render=False)
                state_dim = Y.shape[1]
                control_dim = X.shape[1] - state_dim
                controller = RbfController(state_dim=state_dim, control_dim=control_dim, num_basis_functions=10, max_action=1.)
                R = ExponentialReward(X[:,0], state_dim=state_dim) #, W=weights
                pilco = PILCO(X[:,0], (X, Y), controller=controller, horizon=30, reward=R)
                with open('pilco', 'wb') as f:
                    pickle.dump(pilco, f)
            elif iteration <= n_burn_in:
                iteration +=1
                X_,Y_, _, _, all_states,_ = rollout(env, None, timesteps=1, verbose=False, random=True, SUBS=1, render=False)
                X = np.vstack((X, X_))
                Y = np.vstack((Y, Y_))
            else:
                iteration +=1
                X_,Y_, _, _, all_states,_ = rollout(env, pilco, timesteps=1, verbose=False, random=False, SUBS=1, render=False)
                X = np.vstack((X, X_))
                Y = np.vstack((Y, Y_))
            data_out = (X,Y)
            if iteration % 40 ==0:
                componentProduce('iter_q', iteration)
                componentProduce('output_q', data_out)
            print(f'[Thread 1] Iteration {iteration} time {time.time() - iteration_start_time} seconds')    
            if iteration == 500:
                componentProduce('iter_q', iteration)
                break
            time.sleep(sleep_interval)
    thread_1()
    with Component() as thread_2:
        # logging.debug('thread starting...')
        sleep_interval = 0.1
        np.random.seed(0)
        m_init = np.reshape([1.0], (1,1))
        S_init = np.diag([0.01])
        maxiteropt = 100
        maxiter = 20
        iteration = 0
        while not os.path.exists('pilco'):
            time.sleep(0)
        time.sleep(0.1)
        with open('pilco', 'rb') as f:
            pilco = pickle.load(f)
        while True:
            iteration_start_time = time.time() 
            input_data = componentConsume('output_q')
            #print('****************', input_data)
            X = input_data[0]
            Y = input_data[1]
            state_dim = Y.shape[1]
            control_dim = X.shape[1] - state_dim
            controller = RbfController(state_dim=state_dim, control_dim=control_dim, num_basis_functions=10, max_action=1.)
            R = ExponentialReward(X[:,0], state_dim=state_dim) #, W=weights
            pilco = PILCO(X[:,0], (X, Y), controller=controller, horizon=30, reward=R,  m_init=m_init, S_init=S_init)
            #print('===================== ', len(input_data[0]))
            #print('----------optimization--------------------------------------')
            pilco.optimize_models(maxiter=maxiteropt)
            pilco.optimize_policy(maxiter=maxiter)
            iteration = componentConsume('iter_q')
            print(f'[Thread 2] Iteration {iteration} time {time.time() - iteration_start_time} seconds')    
            if iteration == 500:
                break
            time.sleep(sleep_interval)
    thread_2()
main()
