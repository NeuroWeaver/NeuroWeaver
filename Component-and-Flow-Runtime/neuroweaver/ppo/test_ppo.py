from qfdfg.component import Component
from qfdfg.graph import Graph
from runtime.runtime import Runtime

from typing import List
import numpy as np
import logging
import os, time

import gym
import gym_oscillator # for using oscillator in gym env
import oscillator_src.oscillator_cpp # for the oscillator code
import torch as th
from ppo_components import RLInference, Brain, RolloutCollector, RLTrainer

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
    test_iteration = 4096 #test_iteration=5120000 if we run the real training

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

    steps = 2048 # 512 is PPO's n_steps for now 
    rollout_collector = RolloutCollector(rollout_steps=steps)
    rollout_collector.set_input("observation_updates", (250,))
    rollout_collector.set_input("rewards", (1,))
    rollout_collector.set_input("dones", (1,))
    rollout_collector.set_input("policy_forward_output", (3,))

    rollout_collector.set_state("rollout", (1,)) # not an array but a struct, use (1,) as shape
    rollout_collector.set_state("timesteps", (1,))

    training_timesteps = 10
    trainer = RLTrainer(total_training_timesteps=training_timesteps)
    trainer.set_state("weights", (1,))
    trainer.set_input("rollout", (1,))
    trainer.set_state("timesteps", (1,))

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

    runtime = Runtime(graph)
    runtime._use_futures = False
    runtime._iterations = test_iteration
    runtime._force_state_update = False
    runtime.initialize()
    start = time.time()
    runtime.execute()
    end = time.time()
    print(f"exec time:{end - start}")

## end-to-end run, may take a min or two as it runs 2048 steps to fill PPO's rolloutbuffer
if os.path.exists(log_file_name):
	os.remove(log_file_name)
test_all_ppo_components()