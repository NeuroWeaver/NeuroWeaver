#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 12:50:55 2021

@author: psarikh
"""



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


np.random.seed(0)




# component 1 is the environment or the data generator

n_burn_in = 20
global iteration
iteration = 0
global pilco

def thread_1 (output_q):
    global iteration
    # logging.debug('thread starting...')
    env_id = 'oscillator-v0'
    env = gym.make(env_id)
    env.reset()
    
    sleep_interval = 0.1  # seconds

    while True:
        if iteration ==0:
            iteration +=1
            X,Y, _, _, all_states,_ = rollout(env, None, timesteps=1, verbose=False, random=True, SUBS=1, render=False)
            state_dim = Y.shape[1]
            control_dim = X.shape[1] - state_dim
            # print(all_states.shape)
            controller = RbfController(state_dim=state_dim, control_dim=control_dim, num_basis_functions=10, max_action=1.)
            R = ExponentialReward(X[:,0], state_dim=state_dim) #, W=weights
            pilco = PILCO(X[:,0], (X, Y), controller=controller, horizon=30, reward=R)
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
        
        print(iteration)
        if iteration % 40 ==0:
            output_q.put(data_out)
            # print(data_out)

        time.sleep(sleep_interval)
    # logging.debug('thread ending...')


# component 2 updates the policy

def thread_2(input_q):
    # logging.debug('thread starting...')
    sleep_interval = 0.1
    m_init = np.reshape([1.0], (1,1))
    S_init = np.diag([0.01])
    maxiteropt = 100
    maxiter = 20
    global pilco
    
    while True:
        input_data = input_q.get()
        print('****************', input_data)
        X = input_data[0]
        Y = input_data[1]
        state_dim = Y.shape[1]
        control_dim = X.shape[1] - state_dim
        # print(all_states.shape)
        controller = RbfController(state_dim=state_dim, control_dim=control_dim, num_basis_functions=10, max_action=1.)
        R = ExponentialReward(X[:,0], state_dim=state_dim) #, W=weights
        pilco = PILCO(X[:,0], (X, Y), controller=controller, horizon=30, reward=R,  m_init=m_init, S_init=S_init)
        print('===================== ', len(input_data[0]))
        # if len(input_data[0])> 100 and len(input_data[0])%40:
        print('----------optimization--------------------------------------')
        pilco.optimize_models(maxiter=maxiteropt)
        pilco.optimize_policy(maxiter=maxiter)
            
        time.sleep(sleep_interval)










def main():

    buffer_1 = Queue()

    thread_1_thread = threading.Thread(name='Thread 1',
                                       target=thread_1,
                                       args=(buffer_1,))
    thread_2_thread = threading.Thread(name='Thread 2',
                                        target=thread_2,
                                        args=(buffer_1,))
    thread_1_thread.start()
    thread_2_thread.start()


if __name__ == '__main__':
    main()



















