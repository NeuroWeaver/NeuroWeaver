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
import time, os
from sac_components import RLInference, Brain, RolloutCollector, RLTrainer

log_file_name = './debug_test_sac.log'
logging.basicConfig(format='%(levelname)-5s [%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG) 
logger = logging.getLogger(__name__) 
fh = logging.FileHandler(log_file_name)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

def test_all_sac_components():
    # logging.basicConfig(format='%(levelname)-5s [%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
    # logger = logging.getLogger(__name__) 
    graph = Graph("SAC-end-to-end-example")
    test_iteration = 512 #test_iteration=5120000 if we run the real training

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

    rollout_steps = 512 # 512 is PPO's n_steps for now 
    rollout_collector = RolloutCollector(rollout_steps=rollout_steps)
    rollout_collector.set_input("observation_updates", (250,))
    rollout_collector.set_input("rewards", (1,))
    rollout_collector.set_input("dones", (1,))
    rollout_collector.set_input("scaled_actions", (1,))

    rollout_collector.set_state("rollout", (1,)) # not an array but a struct, use (1,) as shape
    rollout_collector.set_state("timesteps", (1,))

    training_timesteps = 1
    trainer = RLTrainer(total_training_timesteps=training_timesteps)
    trainer.set_state("weights", (1,))
    trainer.set_input("rollout", (1,))
    trainer.set_state("timesteps", (1,))
    trainer.iterations = 1

    graph.add_component(inference)
    graph.add_component(brain)
    graph.add_component(rollout_collector)
    graph.add_component(trainer)
    
    graph.add_flow("observation_updates", brain, "observation_updates", rollout_collector)
    graph.add_flow("rewards", brain, "rewards", rollout_collector)
    graph.add_flow("dones", brain, "dones", rollout_collector)

    graph.add_flow("scaled_actions", inference, "scaled_actions", rollout_collector)
    graph.add_flow("actions", inference, "actions", brain)
    graph.add_flow("observations", brain, "observations", inference)

    graph.add_flow("rollout", rollout_collector, "rollout", trainer)
    graph.add_flow("timesteps", rollout_collector, "timesteps", trainer)

    graph.add_flow("weights", trainer, "weights", inference)

    runtime = PPRuntime(graph)
    runtime._iterations = test_iteration
    #runtime.initialize(max_msg_count=128, max_msg_size=2500000)
    runtime.initialize(max_msg_count=test_iteration, max_msg_size=2700000)
    runtime.execute()

## end-to-end run, may take a min or two as it runs 2048 steps to fill PPO's rolloutbuffer
if os.path.exists(log_file_name):
	os.remove(log_file_name)
test_all_sac_components()