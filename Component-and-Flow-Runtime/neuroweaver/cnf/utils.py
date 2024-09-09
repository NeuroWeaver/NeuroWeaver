import numpy as np
from gpflow import config
from gym import make
float_type = config.default_float()


def rollout(env, pilco, timesteps, verbose=True, random=False, SUBS=1, render=False, action_flag=True):
        X = []; Y = []; X_obs=[]; Y2 = []
        x_obs = env.x_val # changed it from env.reset() for neuroweaver (trail by trail not a batch)
        x = env.x_val
        y = env.y_val
        ep_return_full = 0
        ep_return_sampled = 0
        for timestep in range(timesteps):
            if render: env.render()
            u = policy(env, pilco, np.array([x]), random, action_flag) # changed x to np.array([x]) 
            for i in range(SUBS): 
                x_new_obs, r, done, _ = env.step(u)
                x_new = env.x_val
                y_new = env.y_val
                ep_return_full += r
                if done: break
                if render: env.render()
            if verbose:
                print("Action: ", u)
                print("State : ", x_new)
                print("Return so far: ", ep_return_full)
            X.append(np.hstack((x, u)))
            Y2.append([y_new])
            X_obs.append(np.hstack((x_obs, u)))
            #print('X',X.shape)
            #print('x',x.shape)
            #print('u',u.shape)
            Y.append([x_new - x])
            ep_return_sampled += r
            x = x_new
            if done: break
        return np.stack(X), np.stack(Y), ep_return_sampled, ep_return_full, np.stack(X_obs), Y2


def policy(env, pilco, x, random, action_flag):
    if action_flag:
        if random:
            return env.action_space.sample()
        else:
            #print('computeeeee action, x',x)
            return pilco.compute_action(x[None, -1])[0, :]
    # Modified for no action scenario-Parisa
    else:
        return [0]

class Normalised_Env():
    def __init__(self, env_id, m, std):
        self.env = make(env_id).env
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space
        self.m = m
        self.std = std

    def state_trans(self, x):
        return np.divide(x-self.m, self.std)

    def step(self, action):
        ob, r, done, _ = self.env.step(action)
        return self.state_trans(ob), r, done, {}

    def reset(self):
        ob =  self.env.reset()
        return self.state_trans(ob)

    def render(self):
        self.env.render()
