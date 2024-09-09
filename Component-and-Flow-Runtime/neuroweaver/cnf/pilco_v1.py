import numpy as np
import gym
from pilco.models import PILCO
from pilco.controllers import RbfController, LinearController
from pilco.rewards import ExponentialReward
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt
np.random.seed(0)
from utils import rollout, policy
from gpflow import set_trainable


import gym
import gym_oscillator
import oscillator_cpp






with Component() as main:
    with Component(outputs=[X, Y, m_init, S_init, max_action, T, env, SUBS]) as component_1:
        env_id = 'oscillator-v0'
        env = gym.make(env_id)
        SUBS=3 # subsampling rate
        T = 100 # number of timesteps (for planning, training and testing here)
        J = 3 # rollouts before optimisation starts
        max_action=1.0 # used by the controller, but really defined by the environment
        m_init = np.reshape([1.0], (1,1))
        S_init = np.diag([0.01])
        # Random rollouts
        X,Y, _, _, all_states,_ = rollout(env, None, timesteps=T, verbose=False, random=True, SUBS=SUBS, render=False)
        for i in range(1,J):
            print(i)
            X_, Y_, _, _, all_states, _ = rollout(env, None, timesteps=T, verbose=False, random=True, SUBS=SUBS, render=False)
            X = np.vstack((X, X_))
            Y = np.vstack((Y, Y_))
        print()
    X, Y, m_init, S_init, max_action, T, env, SUBS = component_1()
    with Component(inputs=[X, Y, m_init, S_init, max_action, T], outputs=[pilco, R]) as component_2:
        state_dim = Y.shape[1]
        control_dim = X.shape[1] - state_dim
        controller = RbfController(state_dim=state_dim, control_dim=control_dim, num_basis_functions=10, max_action=max_action)
        R = ExponentialReward(X[:,0], state_dim=state_dim) #, W=weights
        pilco = PILCO(X[:,0], (X, Y), controller=controller, horizon=T, reward=R,  m_init=m_init, S_init=S_init)
    pilco, R = component_2(X, Y, m_init, S_init, max_action, T)
    with Component(inputs=[X, Y, R], outputs=[r_new, state_dim]) as component_3:
        state_dim = Y.shape[1]
        control_dim = X.shape[1] - state_dim
        r_new = []
        for i in range(len(X)):
            r_new.append(R.compute_reward(X[i,0:state_dim,None], 0.001 * np.eye(state_dim), X[i,1,None].reshape(1,1))[0].numpy())
        print(np.transpose(r_new)[0])
        print(f'Length of X: {len(X)}')
    r_new, state_dim = component_3(X, Y, R)
    with Component(inputs=[pilco, R, env, SUBS, m_init, S_init, U_init, T]) as component_4:
        U_init=np.reshape([0.],(1,1))
        N = 3
        maxiteropt = 100
        maxiter = 20
        T_sim = 100
        for rollouts in range(N):
            print("**** ITERATION no", rollouts, " ****")
            pilco.optimize_models(maxiter=maxiteropt)
            pilco.optimize_policy(maxiter=maxiter)
            X_new, Y_new, _, _, _, _ = rollout(env, pilco, timesteps=T_sim, verbose=False, SUBS=SUBS, render=False)
            for i in range(len(X_new)):
                r_new.append(R.compute_reward(X_new[i,0:state_dim,None], 0.001 * np.eye(state_dim),X_new[i,1,None].reshape(1,1))[0].numpy())
            print('rewaaaaaard', np.transpose(r_new)[0])
            total_r = sum(r_new)
            _, _, r = pilco.predict(m_init, S_init, U_init, T)
            print("Total ", total_r, " Predicted: ", r)
            X = np.vstack((X, X_new)); Y = np.vstack((Y, Y_new.reshape(-1,1)))
            pilco.mgpr.set_data((X, Y))
            print(len(X_new))
    component_4(pilco, R, env, SUBS, m_init, S_init, U_init, T)
main()
