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

## our own local version of PPO not the stock version
from ppo import PPO

logging.basicConfig(format='%(levelname)-5s [%(filename)s:%(lineno)d] %(message)s', level=logging.WARNING) 
logger = logging.getLogger(__name__) 
fh = logging.FileHandler('debug_ppo_components.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

class Brain_source(Component):    
    @property
    def state_names(self) -> List[str]:
        return ["clipped_actions"]

    @property
    def output_names(self) -> List[str]:
        return ["observations", "observation_updates", "rewards", "dones"]

    def initialize(self, clipped_actions):
        super().initialize(clipped_actions)
        self._env = gym.make('oscillator-v0')
        logger.debug("oscillator-v0")
        set_random_seed(0)
        time.sleep(1.68)
        action = np.array([0])
        clipped_actions.push(action, (1,))
        self.uid = 0
        print(f"iter:{self._iterations}")
        self._env.reset()
        # llist = [0.0] * self._iterations        
        # self._ingress_timestamps = shm.ShareableList(llist, name = f"{self.name}_ingress_timestamps")
        # self._egress_timestamps  = shm.ShareableList(llist, name = f"{self.name}_egress_timestamps")
        
    def destory(self):
        super().destory()
        print(f"{self.name} destory called")
        # #[temp: used-for-timestamps]
        # llist = shm.ShareableList(name='latencylist')
        # start_index = 0
        # end_index = int(len(llist)/2)
        # j = 0
        # for i in range(start_index, end_index):
        #     llist[i] = self._timestamps[j]
        #     j = j + 1

    def execute(self, clipped_actions, observations, observation_updates, rewards, dones):
        #logger.debug("brain-execute")
        start = time.time()
        #self._timestamps.append(start)        
        action = clipped_actions.pop()
        new_obs_array, reward_array, done_array, _ = self._env.step(action)
        reward_array = np.array([reward_array])
        done_array = np.array([done_array])
        #logger.debug(f"reward_array {reward_array}")
        #logger.debug(f"done_array {done_array}")
        time.sleep(0.002)
        # manual duplication here
        new_obs_array_uid = uidarray(new_obs_array, uid=self.uid)
        observations.push(new_obs_array, (250,))
        end = time.time()        
        observation_updates.push(new_obs_array_uid, (250,))
        rewards.push(reward_array, (1,))
        dones.push(done_array, (1,))
        self._ingress_timestamps[self.uid] = start
        self._egress_timestamps[self.uid] = end
        self.uid += 1
        #logger.debug(f"{self._name}: action {action}")


class RolloutCollector_pipeline(Component):
    @property
    def input_names(self) -> List[str]:        
        return ["observation_updates", "rewards", "dones", "policy_forward_output"]
        
    @property
    def state_names(self) -> List[str]:
        return ["rollout", "timesteps"]

    @property
    def param_names(self) -> List[str]:
        return ["rollout_steps"]

    def initialize(self, rollout, timesteps, rollout_steps):
        _env = gym.make('oscillator-v0')        
        set_random_seed(0)
		#### stingw: THIS IS the bottleneck !!! of making the latency spike on the inference path 4 ms -> 85 ms
		#### speculation: contention on PPO creation
		
        # self.model = PPO("MlpPolicy", _env, verbose=1)
        # # self.model = PPO("MlpPolicy", None, gamma= 0.99,  n_steps=rollout_steps, ent_coef=0.01, learning_rate=2.5e-4, vf_coef=0.5,
        # #     max_grad_norm=0.5, gae_lambda=0.95, verbose=1, clip_range=0.2) #tensorboard_log="MLP/")
        # self.model.policy.set_training_mode(False)
        # self.model.rollout_buffer.reset()
        # self.model.n_steps = rollout_steps

        self.n_steps = 0 # to track rollout counters
        logger.debug(f"{self._name}:  initialized")
        
    def execute(self, observation_updates, rewards, dones, policy_forward_output, rollout, timesteps):
        new_obs = observation_updates.pop()
        new_obs = new_obs.astype('float32')
        new_obs = new_obs.reshape((1,250))
        reward = rewards.pop()
        done = float(dones.pop())
        done = np.array([done])
        action_value_logprob_array = policy_forward_output.pop()
        action = np.array(action_value_logprob_array[0])


class middle_component(Component):
    @property
    def input_names(self) -> List[str]:
        # observation receives new_obs from Brain's observation        
        return ["observation_updates"]

    @property
    def output_names(self) -> List[str]:
        # observation receives new_obs from Brain's observation        
        return ["observation_output"]

    def initialize(self):
        super().initialize()
        pass

    def destory(self):
        super().destory()
        print(f"{self.name} destory called")
	
    def execute(self, observation_updates, observation_output):
        start = time.time()
        obs = observation_updates.pop()
        observation_output.push(obs, obs.shape)
        end = time.time()
        self._ingress_timestamps[obs.uid] = start
        self._egress_timestamps[obs.uid] = end

class simple_pipeline(Component):
    @property
    def input_names(self) -> List[str]:
        # observation receives new_obs from Brain's observation        
        #return ["observation_updates"]
        return ["observation_output"]

    def initialize(self):
        super().initialize()
        # llist = [0.0] * self._iterations        
        # self._ingress_timestamps = shm.ShareableList(llist, name = f"{self.name}_ingress_timestamps")
        # self._egress_timestamps  = shm.ShareableList(llist, name = f"{self.name}_egress_timestamps")
        pass

    def destory(self):
        super().destory()
        print(f"{self.name} destory called")
	
    def execute(self, observation_output):
        start = time.time()
        obs = observation_output.pop()
        one_arr = np.ones(obs.shape, dtype=obs.dtype)
        obs = obs*one_arr
        end = time.time()
        self._ingress_timestamps[obs.uid] = start
        self._egress_timestamps[obs.uid] = end

class RLInference_pipeline(Component):
    @property
    def input_names(self) -> List[str]:
        # observation receives new_obs from Brain's observation        
        return ["observations"]

    @property
    def state_names(self) -> List[str]:        
        # weights receives state_dict? from RLTrainer's weight_updates
        return ["weights"]

    @property
    def output_names(self) -> List[str]:
        # clipped_actions outputs to Brain's clipped_actions
        # policy_forward_output has <(unclipped) actions, values, log_probs>
        # policy_forward_output outputs to RolloutCollector's 
        # observation_update push last_obs to RolloutCollector's observation 
        return ["clipped_actions", "policy_forward_output"]

    def destory(self):
        super().destory()
        print(f"{self.name} destory called")

    def initialize(self, weights):
        super().initialize()
        logger.debug(f"comp initialize on process {os.getpid()}")
        set_random_seed(0)

        self.env = gym.make('oscillator-v0')
        logger.debug(f"after env")
        last_obs = self.env.reset()
        #self.model = PPO("MlpPolicy", self.env, verbose=1)
        self.n_steps = 512
        
        self.model = PPO("MlpPolicy", self.env, gamma= 0.99,  n_steps=self.n_steps, ent_coef=0.01, learning_rate=2.5e-4, vf_coef=0.5,
            max_grad_norm=0.5, gae_lambda=0.95, verbose=1, clip_range=0.2) #tensorboard_log="MLP/")
        self.model._last_obs = last_obs
        logger.debug(f"obs dtype: {last_obs.dtype}")
        # logger.debug(f"self.model._last_obs dtype: {self.model._last_obs.dtype}")
        # observations.push(last_obs, (250,))
        eval_freq = -1
        self.model._setup_learn(total_timesteps=1, eval_env=self.model.env, callback=None, eval_freq=eval_freq)
        self.model.policy.set_training_mode(False)

        params = self.model.get_parameters()
        weights.push_object(params)

        logger.debug("init inference-component")

    
    def execute(self, observations, weights, clipped_actions, policy_forward_output):
        #logger = logging.getLogger(__name__)
        # logger.debug("RLInference-execute")
        obs = observations.pop()
        # logger.debug(f"obs type {type(obs)}")
        # logger.debug("after obs pop")

        params_dicts = weights.pop_object()
        if  params_dicts is not None:
           self.model.set_parameters(params_dicts)

        # logger.debug("after weights pop")
        # logger.debug(f"params_dicts type {type(params_dicts)}")		
        # if type(params_dicts) == np.ndarray:
        #    logger.debug("NO weights from trainer")
        # elif params_dicts is not None:
        #     logger.debug("SET weights from trainer")
        #     self.model.set_parameters(params_dicts)
        # else:
        #     logger.debug("NO weights from trainer")

        ## Noted that the dtype and shape needs to be matched up
        # print(np.allclose(obs, self.model._last_obs))     
        obs = obs.astype('float32')
        # logger.debug(f"obs dtype: {obs.dtype}")
        # logger.debug(f"_last_obs.dtype: {self.model._last_obs.dtype}")
        obs = obs.reshape((1,250))
        # logger.debug(f"obs shape: {obs.shape}")
        # logger.debug(f"_last_obs shape: {self.model._last_obs.shape}")

        # self.model._last_obs = obs       
        with th.no_grad():
            obs_tensor = obs_as_tensor(obs, self.model.device)
            actions, values, log_probs = self.model.policy.forward(obs_tensor)
            # Rescale and perform action
            clipped_action = actions.cpu() # handle cuda tensor
            # Clip the actions to avoid out of bound error
            if isinstance(self.model.action_space, gym.spaces.Box):
                clipped_action = np.clip(clipped_action, self.model.action_space.low, self.model.action_space.high)

            # logger.debug(clipped_action)
            # logger.debug(values)
            # logger.debug(log_probs)

            forward_output = th.cat((actions[0], values[0], log_probs), 0)
            forward_output = forward_output.cpu() # handle cuda tensor
            forward_output = forward_output.numpy()
            clipped_action = clipped_action.flatten().numpy()
            # logger.debug(f"clipped_action:{clipped_action}")
            # logger.debug(type(forward_output))
            # logger.debug(forward_output.shape)
            clipped_actions.push(clipped_action, (1,))
            policy_forward_output.push(forward_output, (3,))
        end = time.time()
        #self._timestamps.append(end)

        # logger.debug(f"{self._name}: clipped_actions {clipped_actions}")
        # logger.debug(f"{self._name}: policy_forward_output {policy_forward_output}")

class RLInference(Component):
    @property
    def state_names(self) -> List[str]:
        # observation receives new_obs from Brain's observation        
        # weights receives state_dict? from RLTrainer's weight_updates
        return ["observations", "weights"]

    @property
    def output_names(self) -> List[str]:
        # clipped_actions outputs to Brain's clipped_actions
        # policy_forward_output has <(unclipped) actions, values, log_probs>
        # policy_forward_output outputs to RolloutCollector's 
        # observation_update push last_obs to RolloutCollector's observation 
        return ["clipped_actions", "policy_forward_output"]

    def initialize(self, observations, weights):
        logger.debug(f"comp initialize on process {os.getpid()}")
        set_random_seed(0)

        self.env = gym.make('oscillator-v0')
        logger.debug(f"after env")
        last_obs = self.env.reset()
        #self.model = PPO("MlpPolicy", self.env, verbose=1)
        self.n_steps = 512
        
        self.model = PPO("MlpPolicy", self.env, gamma= 0.99,  n_steps=self.n_steps, ent_coef=0.01, learning_rate=2.5e-4, vf_coef=0.5,
            max_grad_norm=0.5, gae_lambda=0.95, verbose=1, clip_range=0.2) #tensorboard_log="MLP/")
        self.model._last_obs = last_obs
        logger.debug(f"obs dtype: {last_obs.dtype}")
        # logger.debug(f"self.model._last_obs dtype: {self.model._last_obs.dtype}")
        observations.push(last_obs, (250,))        
        eval_freq = -1
        self.model._setup_learn(total_timesteps=1, eval_env=self.model.env, callback=None, eval_freq=eval_freq)
        self.model.policy.set_training_mode(False)

        params = self.model.get_parameters()
        weights.push_object(params)

        logger.debug("init inference-component")

    def execute(self, observations, weights, clipped_actions, policy_forward_output):
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
            self.model.set_parameters(params_dicts)
        else:
            logger.debug("NO weights from trainer")

        ## Noted that the dtype and shape needs to be matched up
        # print(np.allclose(obs, self.model._last_obs))     
        obs = obs.astype('float32')
        logger.debug(f"obs dtype: {obs.dtype}")
        logger.debug(f"_last_obs.dtype: {self.model._last_obs.dtype}")
        obs = obs.reshape((1,250))
        logger.debug(f"obs shape: {obs.shape}")
        logger.debug(f"_last_obs shape: {self.model._last_obs.shape}")

        # self.model._last_obs = obs       
        with th.no_grad():
            obs_tensor = obs_as_tensor(obs, self.model.device)
            actions, values, log_probs = self.model.policy.forward(obs_tensor)
            # Rescale and perform action
            clipped_action = actions.cpu() # handle cuda tensor
            # Clip the actions to avoid out of bound error
            if isinstance(self.model.action_space, gym.spaces.Box):
                clipped_action = np.clip(clipped_action, self.model.action_space.low, self.model.action_space.high)

            logger.debug(clipped_action)
            logger.debug(values)
            logger.debug(log_probs)

            forward_output = th.cat((actions[0], values[0], log_probs), 0)
            forward_output = forward_output.cpu() # handle cuda tensor
            forward_output = forward_output.numpy()
            clipped_action = clipped_action.flatten().numpy()
            logger.debug(f"clipped_action:{clipped_action}")
            # logger.debug(type(forward_output))
            # logger.debug(forward_output.shape)
            clipped_actions.push(clipped_action, (1,))
            policy_forward_output.push(forward_output, (3,))
            #observation_updates.push(obs, (1,250))


        logger.debug(f"{self._name}: clipped_actions {clipped_actions}")
        logger.debug(f"{self._name}: policy_forward_output {policy_forward_output}")

class Brain(Component):
    @property
    def input_names(self) -> List[str]:
        # come from RLInference's clipped_actions
        return ["clipped_actions"]
    
    @property
    def state_names(self) -> List[str]:
        # observations goes to  RLInference's observations
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

    def execute(self, clipped_actions, observations, observation_updates, rewards, dones):
        logger.debug("brain-execute")
        action = clipped_actions.pop()
        new_obs_array, reward_array, done_array, _ = self._env.step(action)
        reward_array = np.array([reward_array])
        done_array = np.array([done_array])
        logger.debug(f"reward_array {reward_array}")
        logger.debug(f"done_array {done_array}")
        observations.push(new_obs_array, (250,))
        observation_updates.push(new_obs_array, (250,))
        rewards.push(reward_array, (1,))
        dones.push(done_array, (1,))
        #logger.debug(f"{self._name}: action {action}")

class RolloutCollector(Component):
    @property
    def input_names(self) -> List[str]:        
        return ["observation_updates", "rewards", "dones", "policy_forward_output"]
        
    @property
    def state_names(self) -> List[str]:
        return ["rollout", "timesteps"]

    @property
    def param_names(self) -> List[str]:
        return ["rollout_steps"]

    def initialize(self, rollout, timesteps, rollout_steps):
        _env = gym.make('oscillator-v0')        
        set_random_seed(0)
        #self.model = PPO("MlpPolicy", env, verbose=1)
        self.model = PPO("MlpPolicy", _env, gamma= 0.99,  n_steps=rollout_steps, ent_coef=0.01, learning_rate=2.5e-4, vf_coef=0.5,
            max_grad_norm=0.5, gae_lambda=0.95, verbose=1, clip_range=0.2) #tensorboard_log="MLP/")
        self.model.policy.set_training_mode(False)
        self.model.rollout_buffer.reset()
        self.model.n_steps = rollout_steps

        self.n_steps = 0 # to track rollout counters
        logger.debug(f"{self._name}:  initialized")
        
    def execute(self, observation_updates, rewards, dones, policy_forward_output, rollout, timesteps):
        #logger.info("RolloutCollector execute()") 
        if self.n_steps == self.model.n_steps:
            ## reset env
            self.model.rollout_buffer.reset()
            self.model.rollout_buffer.increment_id()
            self.n_steps = 0            

        new_obs = observation_updates.pop()
        new_obs = new_obs.astype('float32')
        new_obs = new_obs.reshape((1,250))
        reward = rewards.pop()
        done = float(dones.pop())
        done = np.array([done])
        action_value_logprob_array = policy_forward_output.pop()
        action = np.array(action_value_logprob_array[0])

        value = th.FloatTensor([action_value_logprob_array[1]])
        logprob = th.FloatTensor([action_value_logprob_array[2]])

        ## We don't know whether "info" is useful in PPO
        # self._update_info_buffer(infos)

        self.n_steps += 1
        self.model.num_timesteps += 1
        #logger.debug(f"{self._name}:  n_steps {self.n_steps}")        
        #logger.debug(f"{self._name}:  num_timesteps {self.model.num_timesteps}")

        ## handle gym.spaces.Discrete case
        # if isinstance(self.model.action_space, gym.spaces.Discrete):
        #     # Reshape in case of discrete action
        #     reshape_action = action.reshape(-1, 1)
        #     action = reshape_action
        
        self.model.rollout_buffer.add(new_obs, action, reward, self.model._last_episode_starts, value, logprob)
        self.model._last_obs = new_obs
        self.model._last_episode_starts = done

        #TODO: this three statements should be moved to under "if self.n_steps == self.model.n_steps"
        with th.no_grad():
            # Compute value for the last timestep
            value = self.model.policy.predict_values(obs_as_tensor(new_obs, self.model.device))

        self.model.rollout_buffer.compute_returns_and_advantage(last_values=value, dones=done)        
        #logger.debug(f"{self._name}:  compute_returns_and_advantage {self.n_steps}")

        # we only push the rollout when its size is reight
        if self.n_steps == self.model.n_steps: # for PPO, model.n_steps is 2048 by default
            #logger.debug("push rollout buffer")
            #logger.debug(f"rollout_buffer.full:{self.model.rollout_buffer.full}")
            #logger.debug(f"rollout-buffer-size {self.model.rollout_buffer.size()}")
            # we'll need a copy here for the rollout_buffer we pushed into, 
            # when rollout_buffer.reset(), it won't be all zeros and cleared out
            #print(f"pushed rollout buffer-id:{self.model.rollout_buffer.id}")
            # addr=hex(id(self.model.rollout_buffer))
            # print(addr)
            #rollout.push(self.model.rollout_buffer, (1,))
            rollout.push_object(self.model.rollout_buffer)
            timesteps.push(np.array([self.model.num_timesteps]), (1,) )

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
        #self.model = PPO("MlpPolicy", _env, verbose=1)
        # Hao-Lun's PPO parameter + n_steps=512
        self.model = PPO("MlpPolicy", _env, gamma= 0.99,  n_steps=self.n_steps, ent_coef=0.01, learning_rate=2.5e-4, vf_coef=0.5,
            max_grad_norm=0.5, gae_lambda=0.95, verbose=1, clip_range=0.2) #tensorboard_log="MLP/")
        ## check _setup_learn in on_policy_algorithm.py and base_class.py
        eval_freq = -1
        self.model._setup_learn(total_timesteps=1, eval_env=self.model.env, callback=None, eval_freq=eval_freq)
        self.model.policy.set_training_mode(True)

        ## TODO: parameter: load weights from a pickle file?
        logger.debug(f"RLTrainer initialize does something")
        pass

    def execute(self, rollout, weights, timesteps):
        #logger = logging.getLogger(__name__)
        logger.info("RLTrainer execute()") 

        self.model.rollout_buffer = rollout.pop_object()
        #self.model.rollout_buffer = rollout.pop()
        #print(self.model.rollout_buffer.__dict__)
        print(f"popped rollout buffer-id:{self.model.rollout_buffer.id}")
        # addr=hex(id(self.model.rollout_buffer))
        # print(addr)
        self.model.num_timesteps = timesteps.pop()
        print(f"timestamps:{self.model.num_timesteps}")

        ## asserttion make it work for now
        ## these lines block the following execution until it has its input data
        assert self.model.num_timesteps is not None
        assert self.model.rollout_buffer is not None
        buf_size= self.model.rollout_buffer.size()
        logger.debug(f"rollout_buffer.full:{self.model.rollout_buffer.full}")
        logger.debug(f"rollout_buffer.size:{buf_size}")
        
        #assert self.model.rollout_buffer.full is True
        #print(f"after asserts, rollout is empty: {rollout.empty()}")
        #rollout.clear()

        self.model._update_current_progress_remaining(self.model.num_timesteps, self.total_training_timesteps)
        logger.info("RLTrainer after _update_current_progress_remaining()")

        self.model.train()
        params_dicts = self.model.get_parameters()
        #pp.pprint(params_dicts)        
        # weights.push(params_dicts , (1,))        
        weights.push_object(params_dicts)
        ## TODO: RLTrainer save model to file when num_timesteps reaches say like 5M
        if self.model.num_timesteps >= self.total_training_timesteps:
            m_steps = int(self.model.num_timesteps/1000000)
            self.model.save(f"trained_models/Compo4_p1.5_PPOsb1.4_nsteps512_{m_steps}msteps.zip")