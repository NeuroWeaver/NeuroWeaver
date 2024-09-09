### How to run the PPO example?
```{bash}
python3 test_ppo.py
```
This generates debug_test_ppo.log. It contains all the DEBUG logs you see on the screen.
debug_ppo_components.log contains DEBUG logs inside the components.  

### Test individual components and their combinations
```{bash}
python3 test_components.py 
```
This generates debug_test_components.log. It contains all the DEBUG printout you see on the screen.  

### PPO components we have right now
Every component except `Brain` has a local PPO model for compatblity with the stable-baseline3 codebase.  

**RLInference**: It runs the inference, i.e. forward pass of the RL nerual networks.
The code is snppaed from stable-baseline3 codebase. The line that we acutally do forward pass is the following line.
`obs_tensor` is the observation tensor as an input to forward.  
```{python}
actions, values, log_probs = self.model.policy.forward(obs_tensor)
```
  
**Brain**: It runs the oscillator wrapped as OpenAI gym environment. it use `env.step(action)` to interact with the environment and get observations, rewards, dones, and infos back.
```{python}
new_obs_array, reward_array, done_array, _ = self._env.step(action)
```
  
**RolloutCollector**: It collects the observations, rewards, dones from the `Brain`. The `Rolloutcollecter` stores all these items into a `rollout_buffer` provides by stable-baseline3, which we have our own slightly modified version at `buffers.py`. The following line is the insetion of new items into the `rollout_buffer`.    
```{python}
self.model.rollout_buffer.add(new_obs, action, reward, self.model._last_episode_starts, value, logprob)
```
  
`Rolloutcollecter` outputs its `rollout_buffer` to RLTrainer if its has taken more timesteps than `rollout_steps`.
For example, if we set rollout_steps to 5, then `Rolloutcollecter` only outputs its `rollout_buffer` after 5 timesteps.

 **RLTrainer**: As its name suggests, it performs the traning. The following line does the actual training.
 ```{python}
self.model.train()
``` 

### Our own version of PPO
In the case we need to modify the PPO codebase, we have our own local copy of `ppo.py`, its parent class `on_policy_algorithm.py`, and the base class of all RL algorithms `base_class.py` in the directory. Feel free to change anything there.  


### system setup on Linux for process-parallel runtime to work
sudo su
echo 3145728 > /proc/sys/fs/mqueue/msgsize_max
echo 2048 > /proc/sys/fs/mqueue/msg_max

### clear up hung processes with mqueue and shm leftover
rm /dev/mqueue/*
rm /dev/shm/msgq_dtype

### debug hung processes taken GPU memory 
sudo fuser -v /dev/nvidia*
find the PID with user name
sudo kill -9 $PID

### CUDA related code should be local to components
In our runtime setup, we use fork to launch new processes, but Pytorch + CUDA
can't deal with fork and it'll cause runtime error
`RuntimeError: Cannot re-initialize CUDA in forked subprocess. To use CUDA with multiprocessing, you must use the 'spawn' start method` 

Our workarond for this is to launch pytorch and CUDA related code only in the components's initialize() and execute(). Each component by itself is a process we don't fork component process to another process, so it's the right place to launch Pytorch and CUDA related code there.

See this Github issue for more details: Cannot re-initialize CUDA in forked subprocess[https://github.com/pytorch/pytorch/issues/40403]
