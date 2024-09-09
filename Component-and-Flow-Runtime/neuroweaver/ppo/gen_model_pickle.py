
# -*- coding: utf-8 -*-
import pickle
import gym
import gym_oscillator
from stable_baselines3.common.utils import set_random_seed
import random
import numpy as np
from stable_baselines3 import PPO

if __name__ == '__main__':
    env_id = 'oscillator-v0'
    seed = 0
    set_random_seed(seed)
    np.random.seed(seed)
    random.seed(seed)    
    env = gym.make(env_id) 
    clip = 0.2
    model = PPO("MlpPolicy", env, gamma= 0.99,  n_steps=512, ent_coef=0.01, learning_rate=2.5e-4, vf_coef=0.5,
                max_grad_norm=0.5, gae_lambda=0.95, verbose=1, clip_range=clip, tensorboard_log="MLP/")
    params = model.get_parameters()
    print(f"model got from get_parameters() {model.__dict__}")
    pickled = pickle.dumps(params)
    with open('trained_models/ppo.pickle', 'wb') as handle:
        pickle.dump(params, handle, protocol=pickle.HIGHEST_PROTOCOL)

    handle = open('trained_models/ppo.pickle', 'rb')
    param_read = pickle.load(handle)
    model.set_parameters(param_read)
    print(f"model readout{model.__dict__}")

    handle.close()

