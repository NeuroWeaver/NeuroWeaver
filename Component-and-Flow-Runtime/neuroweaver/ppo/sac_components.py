import os, time
from qfdfg.component import Component
from runtime.process_runtime import uidarray

from typing import List
import numpy as np
import logging

import gym
import gym_oscillator # for using oscillator in gym env
import oscillator_src.oscillator_cpp # for the oscillator code
import torch as th

from stable_baselines3.common.utils import get_schedule_fn, obs_as_tensor, set_random_seed

import pprint
pp = pprint.PrettyPrinter(indent=4)

from sac.sac import SAC

logging.basicConfig(format='%(levelname)-5s [%(filename)s:%(lineno)d] %(message)s',level=logging.DEBUG) 
logger = logging.getLogger(__name__) 
fh = logging.FileHandler('debug_sac_components.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

# class Brain_pipeline(Component):    
#     @property
#     def state_names(self) -> List[str]:
#         return ["clipped_actions"]

#     @property
#     def output_names(self) -> List[str]:
#         return ["observations", "observation_updates", "rewards", "dones"]

#     def initialize(self, clipped_actions):
#         super().initialize()
#         self._env = gym.make('oscillator-v0')
#         logger.debug("oscillator-v0")
#         set_random_seed(0)
#         #time.sleep(1.68)
#         action = np.array([0])
#         clipped_actions.push(action, (1,))
#         self.uid = 0
#         print(f"iter:{self._iterations}")
        
#     def destory(self):
#         super().destory()
#         print(f"{self.name} destory called")

#     def execute(self, clipped_actions, observations, observation_updates, rewards, dones):
#         #logger.debug("brain-execute")
#         start = time.time()
#         #self._timestamps.append(start)        
#         action = clipped_actions.pop()
#         new_obs_array, reward_array, done_array, _ = self._env.step(action)
#         reward_array = np.array([reward_array])
#         done_array = np.array([done_array])
#         #logger.debug(f"reward_array {reward_array}")
#         #logger.debug(f"done_array {done_array}")
#         time.sleep(0.002)
#         # manual duplication here
#         new_obs_array_uid = uidarray(new_obs_array, uid=self.uid)
#         observations.push(new_obs_array, (250,))
#         end = time.time()        
#         observation_updates.push(new_obs_array_uid, (250,))
#         rewards.push(reward_array, (1,))
#         dones.push(done_array, (1,))
#         self._ingress_timestamps[self.uid] = start
#         self._egress_timestamps[self.uid] = end
#         self.uid += 1
#         #logger.debug(f"{self._name}: action {action}")

class Brain(Component):
    @property
    def input_names(self) -> List[str]:
        # come from RLInference's clipped_actions
        return ["actions"]
    
    @property
    def state_names(self) -> List[str]:
        # observations goes to RLInference's observations
        return ["observations"]

    @property
    def output_names(self) -> List[str]:
        # reward goes to  RolloutCollector's reward
        # observation_updates goes to RolloutCollector's observation_updates
        # dones goes to RolloutCollector's dones
        return ["observation_updates", "rewards", "dones"]

    def initialize(self, observations):
        self._env = gym.make('oscillator-v0')
        logger.debug("oscillator-v0")
        set_random_seed(0)

    def execute(self, actions, observations, observation_updates, rewards, dones):
        logger.debug("brain-execute")
        action = actions.pop()
        new_obs_array, reward_array, done_array, _ = self._env.step(action)
        reward_array = np.array([reward_array])
        done_array = np.array([done_array])
        logger.debug(f"reward_array {reward_array}")
        logger.debug(f"done_array {done_array}")
        observations.push(new_obs_array, (250,))
        observation_updates.push(new_obs_array, (250,))
        rewards.push(reward_array, (1,))
        dones.push(done_array, (1,))

class RLInference(Component):
    @property
    def state_names(self) -> List[str]:
        # observation receives new_obs from Brain's observation        
        # weights receives state_dict? from RLTrainer's weight_updates
        return ["observations", "weights"]

    @property
    def output_names(self) -> List[str]:
        # scaled_actions outputs to Brain's scaled_actions
        return ["actions", "scaled_actions"]

    def initialize(self, observations, weights):
        logger.debug(f"comp initialize on process {os.getpid()}")
        set_random_seed(0)

        self.env = gym.make('oscillator-v0')
        logger.debug(f"after env")
        last_obs = self.env.reset()
        #self.n_steps = 512
        self.learning_starts = 0
        
        self.model = SAC("MlpPolicy", self.env, buffer_size=512, verbose=1, tensorboard_log="MLP/")
        self.model._last_obs = last_obs
        logger.debug(f"obs dtype: {last_obs.dtype}")
        # logger.debug(f"self.model._last_obs dtype: {self.model._last_obs.dtype}")
        observations.push(last_obs, (250,))        
        self.model._setup_learn(total_timesteps=1, eval_env=self.model.env, callback=None)
        self.model.policy.set_training_mode(False)

        params = self.model.get_parameters()
        weights.push_object(params)	

    def execute(self, observations, weights, actions, scaled_actions):
        #logger = logging.getLogger(__name__)
        logger.debug("RLInference-execute")
        obs = observations.pop()
        logger.debug(f"obs type {type(obs)}")
        logger.debug("after obs pop")
        params_dicts = weights.pop_object()
        #params_dicts = weights.pop()
        logger.debug("after weights pop")
        logger.debug(f"params_dicts type {type(params_dicts)}")		
        if type(params_dicts) == np.ndarray:
           logger.debug("NO weights from trainer")
        elif params_dicts is not None:
            logger.debug("SET weights from trainer")
            #print(params_dicts)
            self.model.set_parameters(params_dicts)
        else:
            logger.debug("NO weights from trainer")

        ## Noted that the dtype and shape needs to be matched up
        # print(np.allclose(obs, self.model._last_obs))     
        obs = obs.astype('float32')
        logger.debug(f"obs dtype: {obs.dtype}")
        logger.debug(f"_last_obs.dtype: {self.model._last_obs.dtype}")
        #self.model._last_obs = obs.reshape((1,250)) #? do we need this
        #logger.debug(f"obs shape: {obs.shape}")
        #logger.debug(f"_last_obs shape: {self.model._last_obs.shape}")

        ## for osc_env we can only use scaled_actions
        ## we return actions but we don't use it for now        
        action, scaled_action = self.model._sample_action(self.learning_starts)
        #logger.warning(f"{self._name}: scaled_action {scaled_action}")        
        logger.debug(f"{self._name}: action {action}")        
        actions.push(scaled_action[0],(1,))
        scaled_actions.push(scaled_action[0],(1,))
        

class RolloutCollector(Component):
    @property
    def input_names(self) -> List[str]:        
        return ["observation_updates", "rewards", "dones", "scaled_actions"]
        
    @property
    def state_names(self) -> List[str]:
        return ["rollout", "timesteps"]

    @property
    def param_names(self) -> List[str]:
        return ["rollout_steps"]

    def initialize(self, rollout, timesteps, rollout_steps):
        _env = gym.make('oscillator-v0')        
        set_random_seed(0)
        self.model = SAC("MlpPolicy", _env, buffer_size=512, verbose=1)
        # self.model = SAC("MlpPolicy", _env, gamma= 0.99,  n_steps=rollout_steps, ent_coef=0.01, learning_rate=2.5e-4, vf_coef=0.5,
        #     max_grad_norm=0.5, gae_lambda=0.95, verbose=1, clip_range=0.2) #tensorboard_log="MLP/")
        self.model.policy.set_training_mode(False)
        self.model.replay_buffer.reset()
        self.model.n_steps = rollout_steps

        self.n_steps = 0 # to track rollout counters
        logger.debug(f"{self._name}:  initialized")
        
    def execute(self, observation_updates, rewards, dones, scaled_actions, rollout, timesteps):
        #logger.info("RolloutCollector execute()") 
        # move to the botm if self.n_steps == self.model.n_steps:
        if self.n_steps == self.model.n_steps:
            ## reset env
            self.model.replay_buffer.reset()
            self.model.replay_buffer.increment_id()
            self.n_steps = 0            

        new_obs = observation_updates.pop()
        new_obs = new_obs.astype('float32')
        new_obs = new_obs.reshape((1,250))
        reward = rewards.pop()
        done = float(dones.pop())
        done = np.array([done])
        scaled_action = scaled_actions.pop()

        ## We don't know whether "info" is useful in SAC
        # self._update_info_buffer(infos)

        self.n_steps += 1
        self.model.num_timesteps += 1
        #logger.debug(f"{self._name}:  n_steps {self.n_steps}")        
        #logger.debug(f"{self._name}:  num_timesteps {self.model.num_timesteps}")
        
        # stingw: we don't use the _store_transition method from 
        # off_policy_algorithm.py as it overcomplicates the buffer update
        # our default env is osc_env which offer boolena dones and empty infos
        # it doesn't have compilcated strcuture of dones or infos

        self.model.replay_buffer.add(self.model._last_obs, new_obs, scaled_action, reward, done, None)
        self.model._last_obs = new_obs
        self.model._last_episode_starts = done

        # we only push the replay_buffer when its size is reight
        if self.n_steps == self.model.n_steps: # for PPO, model.n_steps is 2048 by default
            logger.debug("rollout:push replay_buffer")
            logger.debug(f"rollout:replay_buffer.full:{self.model.replay_buffer.full}")
            logger.debug(f"rollout:replay_buffer pos {self.model.replay_buffer.pos}")
            logger.debug(f"rollout:replay_buffer-buffer-size {self.model.replay_buffer.size()}")
            # we'll need a copy here for the replay_buffer we pushed into, 
            # when replay_buffer.reset(), it won't be all zeros and cleared out
            #print(f"pushed replay_buffer buffer-id:{self.model.replay_buffer.id}")
            # addr=hex(id(self.model.replay_buffer))
            # print(addr)
            #rollout.push(self.model.replay_buffer, (1,))            
            rollout.push_object(self.model.replay_buffer)
            logger.debug(f"rollout:rollout.qsize:{rollout.qsize}")
            timesteps.push(np.array([self.model.num_timesteps]), (1,) )
            # self.model.replay_buffer.reset()
            # self.model.replay_buffer.increment_id()
            # self.n_steps = 0  

        # DEBUG: dump reward to npy files
        # if self.model.num_timesteps%100000 == 0:
        #         rewards = self.model.rollout_buffer.get_reward_array()
        #         filname = "reward/Compo4_p1.5_PPOsb1.4_nsteps512_dump{:04d}.npy".format(int(self.model.num_timesteps/100000))
        #         np.save(filname, rewards)

class RLTrainer(Component):
    @property
    def input_names(self) -> List[str]:        
        return ["rollout"]
    
    @property
    def state_names(self) -> List[str]:
        #return ["rollout", "weights", "timesteps"]
        return ["weights", "timesteps"]

    @property
    def param_names(self) -> List[str]:
        return ["total_training_timesteps"]

    def initialize(self, weights, timesteps, total_training_timesteps):
    #def initialize(self, rollout, weights, timesteps, total_training_timesteps):
        self.total_training_timesteps = total_training_timesteps
        self.n_steps = 512 # fixed value to avoid messing up the training
        set_random_seed(0)

        _env = gym.make('oscillator-v0')
        
        self.model = SAC("MlpPolicy", _env, buffer_size=512, verbose=1)
        # Hao-Lun's PPO parameter + n_steps=512
        # self.model = PPO("MlpPolicy", _env, gamma= 0.99,  n_steps=self.n_steps, ent_coef=0.01, learning_rate=2.5e-4, vf_coef=0.5,
        #     max_grad_norm=0.5, gae_lambda=0.95, verbose=1, clip_range=0.2) #tensorboard_log="MLP/")
        ## check _setup_learn in on_policy_algorithm.py and base_class.py
        eval_freq = -1
        self.model._setup_learn(total_timesteps=1, eval_env=self.model.env, callback=None, eval_freq=eval_freq)
        self.model.policy.set_training_mode(True)
        #self.model._total_timesteps = total_training_timesteps

        ## TODO: parameter: load weights from a pickle file?
        logger.debug(f"RLTrainer initialize does something")
        pass

    def execute(self, rollout, weights, timesteps):
        #logger = logging.getLogger(__name__)
        logger.info("RLTrainer execute()") 
        logger.debug(f"RLTrainer:rollout.qsize{rollout.qsize}")

        self.model.replay_buffer = rollout.pop_object()
        #self.model.rollout_buffer = rollout.pop()
        #print(self.model.rollout_buffer.__dict__)
        logger.debug(f"popped replay buffer id:{self.model.replay_buffer.id}")
        # addr=hex(id(self.model.rollout_buffer))
        # print(addr)
        self.model.num_timesteps = timesteps.pop()
        logger.debug(f"timestamps:{self.model.num_timesteps}")

        ## asserttion make it work for now
        ## these lines block the following execution until it has its input data
        assert self.model.num_timesteps is not None
        assert self.model.replay_buffer is not None
        buf_size= self.model.replay_buffer.size()
        logger.debug(f"replay_buffer.full:{self.model.replay_buffer.full}")
        logger.debug(f"replay_buffer.size:{buf_size}")
        
        #assert self.model.rollout_buffer.full is True
        #print(f"self.model.batch_size: {self.model.batch_size}")
        #rollout.clear()
        logger.debug(f"model.num_timesteps.size:{self.model.num_timesteps}")
        if self.model.num_timesteps > 0: #and self.model.num_timesteps > self.model.learning_starts:
            # If no `gradient_steps` is specified,
            # do as many gradients steps as steps performed during the rollout               
            logger.debug(f"model.gradient_steps:{self.model.gradient_steps}")
            if self.model.gradient_steps > 0:
                gradient_steps = self.model.gradient_steps
                self.model.train(batch_size=self.model.batch_size, gradient_steps=gradient_steps)
            # stingw: where do we handle self.gradient_steps assignment?
			# we pass gradient_steps when we construct SAC, if not the default is 1 step
			# Special case when the user passes `gradient_steps=0`?            
            
        #self._total_timesteps comes from base_class.py
        self.model._update_current_progress_remaining(self.model.num_timesteps, self.total_training_timesteps)

		#self.model.train()
        params_dicts = self.model.get_parameters()
        #pp.pprint(params_dicts)        
        # BUG: comment this out to prevent NaN values propogate to RLInference        
        # weights.push_object(params_dicts)
        ## TODO: RLTrainer save model to file when num_timesteps reaches say like 5M
        if self.model.num_timesteps >= self.total_training_timesteps:
            m_steps = int(self.model.num_timesteps/1000000)
            self.model.save(f"trained_models/Compo4_p1.5_PPOsb1.4_nsteps512_{m_steps}msteps.zip")        