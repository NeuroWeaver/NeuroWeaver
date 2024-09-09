import sys
sys.path.append("../..") #add ../.. to python path
sys.path.append("..")
print(sys.path)

from typing import List
import logging
from qfdfg.graph import Graph
from qfdfg.component import Component, ComponentStatus
from runtime.process_runtime import PPRuntime
import numpy as np
import time
from ppo_components import RLInference, Brain, RolloutCollector, RLTrainer

logging.basicConfig(format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)

print("okay import solved")

#from runtime.runtime import Runtime


log_file_name = './debug_test_ppo.log'
logging.basicConfig(format='%(levelname)-5s [%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG) 
logger = logging.getLogger(__name__) 
fh = logging.FileHandler(log_file_name)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

def test_all_ppo_components():
    # logging.basicConfig(format='%(levelname)-5s [%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
    # logger = logging.getLogger(__name__) 
    graph = Graph("PPO-end-to-end-example")

    inference = RLInference()
    inference.set_output("clipped_actions", (1,))
    inference.set_output("policy_forward_output", (3,))
    inference.set_state("observations", (250,))
    inference.set_state("weights", (1,))

    brain = Brain()
    brain.set_input("clipped_actions", (1,))
    brain.set_state("observations", (250,))
    brain.set_output("rewards", (1,))
    brain.set_output("dones", (1,))
    brain.set_output("observation_updates", (250,))

    steps = 512 # 512 is PPO's n_steps for now 
    rollout_collector = RolloutCollector(rollout_steps=steps)
    rollout_collector.set_input("observation_updates", (250,))
    rollout_collector.set_input("rewards", (1,))
    rollout_collector.set_input("dones", (1,))
    rollout_collector.set_input("policy_forward_output", (3,))

    rollout_collector.set_state("rollout", (1,)) # not an array but a struct, use (1,) as shape
    rollout_collector.set_state("timesteps", (1,))

    training_timesteps = 65536*2
    trainer = RLTrainer(total_training_timesteps=training_timesteps)
    trainer.set_state("weights", (1,))
    trainer.set_input("rollout", (1,))
    trainer.set_state("timesteps", (1,))
    # set the iterations
    # test_iteration=5120000 if we run the real training

    # test_iteration = 1028 # 1028 for 2 training runs
    # trainer.iterations = 2 # 1028/512 in integer

    # test_iteration = 1028 + 512 
    # trainer.iterations = 3

    ## ~12 seconds, 11.6 seconds
    # test_iteration = 2048 + 4 
    # trainer.iterations = 4

    ## 24.6 seconds
    # test_iteration = 4096 + 4 
    # trainer.iterations = int(4096/512)
    
	## 2^20 ~= 1 M iterations
    # test_iteration = 512*2048 # ~3*2048 seconds= 1.7 hrs
    # trainer.iterations = int(2048)

	## 4*2^20 + 2^20 = 5242880 iterations
	## 5242880/512 = 10240 trainer-iteration
    test_iteration = 512*10240
    trainer.iterations = int(10240)

    graph.add_component(inference)
    graph.add_component(brain)
    graph.add_component(rollout_collector)
    graph.add_component(trainer)
    
    graph.add_flow("observation_updates", brain, "observation_updates", rollout_collector)
    graph.add_flow("rewards", brain, "rewards", rollout_collector)
    graph.add_flow("dones", brain, "dones", rollout_collector)

    graph.add_flow("policy_forward_output", inference, "policy_forward_output", rollout_collector)
    graph.add_flow("clipped_actions", inference, "clipped_actions", brain)
    graph.add_flow("observations", brain, "observations", inference)

    graph.add_flow("rollout", rollout_collector, "rollout", trainer)
    graph.add_flow("timesteps", rollout_collector, "timesteps", trainer)

    graph.add_flow("weights", trainer, "weights", inference)

    runtime = PPRuntime(graph)
    # runtime._use_futures = False
    # runtime._iterations = test_iteration
    # runtime._force_state_update = False
    # runtime.initialize()
    # runtime.execute()
    runtime._iterations = test_iteration
    #runtime.initialize(max_msg_count=128, max_msg_size=2500000)
    runtime.initialize(max_msg_count=1035, max_msg_size=1000000)
    runtime.execute()

## end-to-end run, may take a min or two as it runs 2048 steps to fill PPO's rolloutbuffer
# if os.path.exists(log_file_name):
#     os.remove(log_file_name)
test_all_ppo_components()