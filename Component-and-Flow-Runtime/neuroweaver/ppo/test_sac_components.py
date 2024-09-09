# def drop_privileges():    
#     import os, pwd
#     if os.getuid() != 0:
#         # We're not root so, like, whatever dude
#         print("not root, return here")
#         return

#     # Get the uid/gid from the name
#     user_name = os.getenv("SUDO_USER")
#     pwnam = pwd.getpwnam(user_name)

#     # Remove group privileges
#     os.setgroups([])

#     # Try setting the new uid/gid
#     os.setgid(pwnam.pw_gid)
#     os.setuid(pwnam.pw_uid)

#     #Ensure a reasonable umask
#     old_umask = os.umask(0o22)

# import resource, os
# ## TODO:make this a seperted script and launch this as a seperated process by that script
# ## so it can inherit the rlimit?
# print(resource.getrlimit(resource.RLIMIT_MSGQUEUE))
# limit=3145728*10000 
# resource.setrlimit(resource.RLIMIT_MSGQUEUE, (limit, limit))
# print(resource.getrlimit(resource.RLIMIT_MSGQUEUE))

# print(os.getresuid())
# ##---------------------##
# drop_privileges()
# ##---------------------##
# print(os.getresuid())

import sys
sys.path.append("../..") #add ../.. to python path
sys.path.append("..")
print(sys.path)

from qfdfg.component import Component
from qfdfg.graph import Graph
from runtime.process_runtime import POSIXMsgQueue, PPRuntime as Runtime

import os
from typing import List
import numpy as np
import logging

import gym
import gym_oscillator # for using oscillator in gym env
import oscillator_src.oscillator_cpp # for the oscillator code
import torch as th
import posix_ipc
from sac_components import RLInference, Brain, RolloutCollector, RLTrainer

# import pprint
# pp = pprint.PrettyPrinter(indent=4)

## our own local version of SAC in sac.py not the stock version
from sac.sac import SAC

log_file_name = './debug_sac_components.log'
logging.basicConfig(format='%(levelname)-5s [%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG) 
logger = logging.getLogger(__name__) 
fh = logging.FileHandler(log_file_name)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

def test_inference_runtime():
    graph = Graph("inference_alone")
    inference = RLInference()
    inference.set_output("actions", (1,), is_process_parallel=True)
    inference.set_output("scaled_actions", (1,), is_process_parallel=True)
    inference.set_state("observations", (250,), is_process_parallel=True)
    inference.set_state("weights", (1,), is_process_parallel=True)

    graph.add_component(inference)

    runtime = Runtime(graph)
    runtime._iterations = 2
    runtime.initialize(max_msg_count=runtime._iterations+1, max_msg_size=3000000)
    w_qid = runtime._qid_table.get('/weights')
    w_queue = POSIXMsgQueue('/weights', (1,), "state", w_qid)
    mq = posix_ipc.MessageQueue('/weights', posix_ipc.O_CREAT)
    w_queue.init_queue(mq)    

    runtime.execute()

def test_brain():
    graph = Graph("brain_alone")
    brain = Brain()
    brain.set_input("actions", (1,), is_process_parallel=True)
    brain.set_state("observations", (250,), is_process_parallel=True)
    brain.set_output("rewards", (1,) , is_process_parallel=True)
    brain.set_output("dones", (1,) , is_process_parallel=True)
    brain.set_output("observation_updates", (250,) , is_process_parallel=True)

    graph.add_component(brain)

    runtime = Runtime(graph)
    test_iteration = 2
    runtime._iterations = test_iteration
    runtime.initialize(max_msg_count=runtime._iterations+1, max_msg_size=3000000)
    w_qid = runtime._qid_table.get('/actions')
    action_queue = POSIXMsgQueue('/actions', (1,), "input", w_qid)
    mq = posix_ipc.MessageQueue('/actions', posix_ipc.O_CREAT)
    action_queue.init_queue(mq)  
    for i in range(test_iteration):
        action = np.array([0.4])
        action_queue.push(action, (1,))  

    runtime.execute()


def test_inference_and_brain():
    graph = Graph("inference_and_brain")
    inference = RLInference()
    inference.set_output("actions", (1,), is_process_parallel=True)
    inference.set_output("scaled_actions", (1,), is_process_parallel=True)
    inference.set_state("observations", (250,), is_process_parallel=True)
    inference.set_state("weights", (1,), is_process_parallel=True)

    brain = Brain()
    brain.set_input("actions", (1,), is_process_parallel=True)
    brain.set_state("observations", (250,), is_process_parallel=True)
    brain.set_output("rewards", (1,) , is_process_parallel=True)
    brain.set_output("dones", (1,) , is_process_parallel=True)
    brain.set_output("observation_updates", (250,) , is_process_parallel=True)

    graph.add_component(inference)
    graph.add_component(brain)

    graph.add_flow("actions", inference, "actions", brain)
    graph.add_flow("observations", brain, "observations", inference)

    runtime = Runtime(graph)
    # we configure the POSIXMsgQueue qsize limit! 
    runtime._iterations = 2
    runtime.initialize(max_msg_count=runtime._iterations+1, max_msg_size=3000000)
    w_qid = runtime._qid_table.get('/weights')
    w_queue = POSIXMsgQueue('/weights', (1,), "state", w_qid)
    mq = posix_ipc.MessageQueue('/weights', posix_ipc.O_CREAT)
    w_queue.init_queue(mq)    

    runtime.execute()

def test_brain_and_rollout():
    graph = Graph("brain_and_rollout")
    test_iteration = 5

    brain = Brain()
    brain.set_input("actions", (1,), is_process_parallel=True)
    brain.set_state("observations", (250,), is_process_parallel=True)
    brain.set_output("rewards", (1,), is_process_parallel=True)
    brain.set_output("dones", (1,), is_process_parallel=True)
    brain.set_output("observation_updates", (250,), is_process_parallel=True)

    rollout_collector = RolloutCollector(rollout_steps=2048)    
    rollout_collector.set_input("observation_updates", (250,), is_process_parallel=True)
    rollout_collector.set_input("rewards", (1,), is_process_parallel=True)
    rollout_collector.set_input("dones", (1,), is_process_parallel=True)
    rollout_collector.set_input("scaled_actions", (1,), is_process_parallel=True)
    #rollout_collector.set_input("policy_forward_output", (3,), is_process_parallel=True)

    rollout_collector.set_state("rollout", (1,), is_process_parallel=True) # not an array but a struct, use (1,) as shape
    rollout_collector.set_state("timesteps", (1,), is_process_parallel=True)

    graph.add_component(brain)
    graph.add_component(rollout_collector)
    
    graph.add_flow("observation_updates", brain, "observation_updates", rollout_collector)
    graph.add_flow("rewards", brain, "rewards", rollout_collector)
    graph.add_flow("dones", brain, "dones", rollout_collector)

    runtime = Runtime(graph)
    #runtime._use_futures = True
    runtime._iterations = test_iteration
    runtime.initialize(max_msg_count=test_iteration+1, max_msg_size=3000000)

    print(runtime._qid_table)
    actions_qid = runtime._qid_table.get('/actions')
    action_queue = POSIXMsgQueue('/actions', (1,), "input", actions_qid)
    mq1 = posix_ipc.MessageQueue('/actions', posix_ipc.O_CREAT)
    action_queue.init_queue(mq1)
    for i in range(test_iteration):
        action = np.array([0.4])
        action_queue.push(action, (1,))

    scaled_actions_qid = runtime._qid_table.get('/scaled_actions')
    scaled_actions_queue = POSIXMsgQueue('/scaled_actions', (1,), "input", scaled_actions_qid)
    mq = posix_ipc.MessageQueue('/scaled_actions', posix_ipc.O_CREAT)
    scaled_actions_queue.init_queue(mq)
    for i in range(test_iteration):
        action = np.array([0.4])
        scaled_actions_queue.push(action, (1,))

    # # fill # test_iteration of policy_forward_output in policy_forward_output queue
    # policy_forward_output_qid = runtime._qid_table.get('/policy_forward_output')
    # forward_queue = POSIXMsgQueue('/policy_forward_output', (3,), "input", policy_forward_output_qid)
    # mq = posix_ipc.MessageQueue('/policy_forward_output', posix_ipc.O_CREAT)
    # forward_queue.init_queue(mq)
    # forward_tuple = np.array([-0.1753,0.7701,-0.9341])
    # for i in range(test_iteration):
    #     policy_forward_output = forward_tuple.copy()
    #     forward_queue.push(policy_forward_output, (3,))

    runtime.execute()


def test_inference_brain_rollout():
    graph = Graph("inference_brain_rollout")
    test_iteration = 5

    inference = RLInference()
    inference.set_output("actions", (1,))
    inference.set_output("scaled_actions", (1,))
    inference.set_state("observations", (250,))
    inference.set_state("weights", (1,))

    brain = Brain()
    brain.set_input("actions", (1,))
    brain.set_state("observations", (250,))
    brain.set_output("rewards", (1,))
    brain.set_output("dones", (1,))
    brain.set_output("observation_updates", (250,))

    rollout_collector = RolloutCollector(rollout_steps=5)
    rollout_collector.set_input("observation_updates", (250,))
    rollout_collector.set_input("rewards", (1,))
    rollout_collector.set_input("dones", (1,))
    rollout_collector.set_input("scaled_actions", (1,))

    rollout_collector.set_state("rollout", (1,)) # not an array but a struct, use (1,) as shape
    rollout_collector.set_state("timesteps", (1,))

    graph.add_component(inference)
    graph.add_component(brain)
    graph.add_component(rollout_collector)
    
    graph.add_flow("observation_updates", brain, "observation_updates", rollout_collector)
    graph.add_flow("rewards", brain, "rewards", rollout_collector)
    graph.add_flow("dones", brain, "dones", rollout_collector)

    graph.add_flow("scaled_actions", inference, "scaled_actions", rollout_collector)
    graph.add_flow("actions", inference, "actions", brain)
    graph.add_flow("observations", brain, "observations", inference)

    runtime = Runtime(graph)
    runtime._use_futures = True
    runtime._iterations = test_iteration
    runtime.initialize(max_msg_count=test_iteration+1, max_msg_size=3000000)
    #runtime.initialize()
    runtime.execute()

def test_rollout_trainer():
    test_iteration = 260
    rollout_steps = 256

    rollout_collector = RolloutCollector(rollout_steps=rollout_steps)
    rollout_collector.set_input("observation_updates", (250,))
    rollout_collector.set_input("rewards", (1,))
    rollout_collector.set_input("dones", (1,))
    rollout_collector.set_input("scaled_actions", (1,))
    
    rollout_collector.set_state("rollout", (1,)) # not an array but a struct, use (1,) as shape
    rollout_collector.set_state("timesteps", (1,))

    training_timesteps = 10
    trainer = RLTrainer(total_training_timesteps=training_timesteps)
    trainer.set_input("rollout", (1,))
    trainer.set_state("weights", (1,))    
    trainer.set_state("timesteps", (1,))
    # set the iteratio
    trainer.iterations = 1

    graph = Graph("test_rollout_trainer")
    graph.add_component(rollout_collector)
    graph.add_component(trainer)
    
    graph.add_flow("rollout", rollout_collector, "rollout", trainer)
    graph.add_flow("timesteps", rollout_collector, "timesteps", trainer)

    runtime = Runtime(graph)
    runtime._iterations = test_iteration
    runtime.initialize(max_msg_count=test_iteration, max_msg_size=5800000)

    obs_up_qid = runtime._qid_table.get('/observation_updates')
    obs_up_queue = POSIXMsgQueue('/observation_updates', (250,), "input", obs_up_qid)
    mq = posix_ipc.MessageQueue('/observation_updates', posix_ipc.O_CREAT)
    obs_up_queue.init_queue(mq)
    env = gym.make('oscillator-v0')
    obs = env.reset()    
    for i in range(test_iteration):
        up = np.copy(obs)  
        obs_up_queue.push(up, (250,))

    # value = 0.7701, log_prob= -0.9341, reward=-1.575
    r_qid = runtime._qid_table.get('/rewards')
    reward_queue = POSIXMsgQueue('/rewards', (1,), "input", r_qid)
    rmq = posix_ipc.MessageQueue('/rewards', posix_ipc.O_CREAT)
    reward_queue.init_queue(rmq)
    for i in range(test_iteration):
        r = np.array([-1.575])
        reward_queue.push(r, (1,))
    
    d_qid = runtime._qid_table.get('/dones')
    done_queue = POSIXMsgQueue('/dones', (1,), "input", d_qid)
    dmq = posix_ipc.MessageQueue('/dones', posix_ipc.O_CREAT)
    done_queue.init_queue(dmq)
    for i in range(test_iteration):
        d = np.array([False])
        done_queue.push(d, (1,))

    f_qid = runtime._qid_table.get('/scaled_actions')
    scaled_actions_queue = POSIXMsgQueue('/scaled_actions', (1,), "input", f_qid)
    fmq = posix_ipc.MessageQueue('/scaled_actions', posix_ipc.O_CREAT)
    scaled_actions_queue.init_queue(fmq)    
    for i in range(test_iteration):
        action = np.array([-0.1753])
        scaled_actions_queue.push(action, (1,))
    
    # we should see RLTrainer exec once in this setup
    runtime.execute()

def test_trainer_inference():
    test_iteration = 11
    training_timesteps = 10
    trainer = RLTrainer(total_training_timesteps=training_timesteps)
    trainer.set_state("weights", (1,))
    trainer.set_input("rollout", (1,))
    trainer.set_state("timesteps", (1,))

    inference = RLInference()
    inference.set_output("clipped_actions", (1,))
    inference.set_output("policy_forward_output", (3,))
    inference.set_state("observations", (250,))
    inference.set_state("weights", (1,))

    graph = Graph("test_rollout_trainer")    
    graph.add_component(trainer)
    graph.add_component(inference)
    
    graph.add_flow("weights", trainer, "weights", inference)

    runtime = Runtime(graph)
    runtime._iterations = test_iteration
    runtime.initialize(max_msg_count=test_iteration, max_msg_size=2500000)

    # rollout_queue = trainer.state_queues.get("rollout")
    # timestep_queue = trainer.state_queues.get("timesteps")

    ts_qid = runtime._qid_table.get('/timesteps')
    ts_queue = POSIXMsgQueue('/timesteps', (1,), "state", ts_qid)
    ts_mq = posix_ipc.MessageQueue('/timesteps', posix_ipc.O_CREAT)
    ts_queue.init_queue(ts_mq)
    
    rollout_qid = runtime._qid_table.get('/rollout')
    rollout_queue = POSIXMsgQueue('/rollout', (250,), "input", rollout_qid)
    mq = posix_ipc.MessageQueue('/rollout', posix_ipc.O_CREAT)
    rollout_queue.init_queue(mq)
    ## create fake data to feed into rollout_buffer
    _env = gym.make('oscillator-v0')
    _model = SAC("MlpPolicy", _env, verbose=1)
    _model.policy.set_training_mode(False)
    _model.replay_buffer.reset()
    new_obs = _env.reset()

    action_value_logprob_array = np.array([-0.1753,0.7701,-0.9341])
    action = np.array(action_value_logprob_array[0])
    value = th.FloatTensor([action_value_logprob_array[1]])
    logprob = th.FloatTensor([action_value_logprob_array[2]])  
    reward = np.array([-1.575])
    for i in range(_model.rollout_buffer.buffer_size):
        _model.rollout_buffer.add(new_obs, action, reward, _model._last_episode_starts, value, logprob)
    
    assert _model.rollout_buffer.full
    
    for i in range(test_iteration): 
        rollout_queue.push_object(_model.rollout_buffer)

    for i in range(test_iteration):
        ts_queue.push(np.array([i*5]), (1,))
    
    runtime.execute()

# if os.path.exists(log_file_name):
#     os.remove(log_file_name)

#single component testing
#test_inference_runtime() #PASS #tested push_object and pop_object

## component-wise testing
#test_inference_and_brain() #PASS
#test_brain() #PASS
#test_brain_and_rollout() #PASS
#test_inference_brain_rollout() #PASS #check with 5 iters
# this one needs to be run seperately
#test_rollout_trainer() # check with 520 iters > 512 the size of rollout buffer, n_steps

# BUG: trainer_inference() needs more verification
# params_dicts = weights.pop_object()
#test_trainer_inference() # not used and need work to make it work 


