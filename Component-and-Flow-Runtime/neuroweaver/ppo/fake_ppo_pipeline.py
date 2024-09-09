import sys, os, logging, time
import numpy as np

sys.path.append("../..") #add ../.. to python path
sys.path.append("..")
print(sys.path)

from qfdfg.graph import Graph
from qfdfg.component import Component, ComponentStatus
from runtime.process_runtime import PPRuntime
from ppo_components import Brain_source, RLInference_pipeline, RolloutCollector, RLTrainer, RolloutCollector_pipeline, middle_component, simple_pipeline

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

    brain = Brain_source()
    # set it as state, if inference cannpt keep up, use the last value    
    brain.set_state("clipped_actions", (1,)) 
    brain.set_output("observations", (250,))        # to inference
    brain.set_output("observation_updates", (250,), is_observed=True) # to training 
    brain.set_output("rewards", (1,))
    brain.set_output("dones", (1,))
    brain._iterations = 10  # takes priority over the runtime iteration

    middle = middle_component()
    middle.set_input("observation_updates", (250,), is_observed=True)
    middle.set_output("observation_output", (250,), is_observed=True)
    middle._iterations = 10

    # sink = simple_pipeline()
    # sink.set_input("observation_output", (250,), is_observed=True)
    # sink._iterations = 10

    inference = RLInference_pipeline()
    inference.set_input("observations", (250,))
    inference.set_state("weights", (1,))       
    inference.set_output("clipped_actions", (1,))
    inference.set_output("policy_forward_output", (3,))
    inference._iterations = 10

    # steps = 512 # 512 is PPO's n_steps for now 
    # #rollout_collector = RolloutCollector(rollout_steps=steps)
    # rollout_collector = RolloutCollector_pipeline(rollout_steps=steps)
    # rollout_collector.set_input("observation_updates", (250,))
    # rollout_collector.set_input("rewards", (1,))
    # rollout_collector.set_input("dones", (1,))
    # rollout_collector.set_input("policy_forward_output", (3,))

    # rollout_collector.set_state("rollout", (1,)) # not an array but a struct, use (1,) as shape
    # rollout_collector.set_state("timesteps", (1,))

    # training_timesteps = 65536*2
    # trainer = RLTrainer(total_training_timesteps=training_timesteps)
    # trainer.set_state("weights", (1,))
    # trainer.set_input("rollout", (1,))
    # trainer.set_state("timesteps", (1,))
    # set the iterations
    # test_iteration=5120000 if we run the real training

    #test_iteration = 1028 # 1028 for 2 training runs
    # trainer.iterations = 1 # 1028/512 in integer

    # test_iteration = 1028 # 1028 for 2 training runs
    # trainer.iterations = 2 # 1028/512 in integer

    # test_iteration = 1028 + 512 
    # trainer.iterations = 3

    ## ~12 seconds, 11.6 seconds
    # test_iteration = 2048 + 4 
    # trainer.iterations = 4

    ## 24.6 seconds
    # test_iteration = 4096 + 1 
    # trainer.iterations = int(4096/256)
    
    ## 2^20 ~= 1 M iterations
    # test_iteration = 512*2048 # ~3*2048 seconds= 1.7 hrs
    # trainer.iterations = int(2048)

    ## 4*2^20 + 2^20 = 5242880 iterations
    ## 5242880/512 = 10240 trainer-iteration
    # test_iteration = 512*10240
    # trainer.iterations = int(10240)

    graph.add_component(brain)
    graph.add_component(middle)
    graph.add_component(inference)
    graph.add_flow("observations", brain, "observations", inference)
    graph.add_flow("observation_updates", brain, "observation_updates", middle)
    #graph.add_flow("observation_output", middle, "observation_output", sink)
    #graph.add_flow("observation_updates", brain, "observation_updates", sink)    

    # graph.add_component(inference)
    # graph.add_component(rollout_collector)
    # graph.add_component(trainer)
    

    #graph.add_flow("observations", brain, "observations", inference)
    #graph.add_flow("observation_updates", brain, "observation_updates", rollout_collector)    
    #graph.add_flow("rewards", brain, "rewards", rollout_collector)
    #graph.add_flow("dones", brain, "dones", rollout_collector)

    #graph.add_flow("policy_forward_output", inference, "policy_forward_output", rollout_collector)
    #graph.add_flow("clipped_actions", inference, "clipped_actions", brain)    

    # graph.add_flow("rollout", rollout_collector, "rollout", trainer)
    # graph.add_flow("timesteps", rollout_collector, "timesteps", trainer)

    # graph.add_flow("weights", trainer, "weights", inference)

    runtime = PPRuntime(graph)
    # runtime._use_futures = False
    # runtime._iterations = test_iteration
    # runtime._force_state_update = False
    # runtime.initialize()
    # runtime.execute()
    runtime._iterations = test_iteration
    # max_msg_count is the max queue size of each queue
    # max_msg_size is the max size of each item in queue (bytes)
    runtime.initialize(max_msg_count=1035, max_msg_size=1000000)
    runtime.execute()

## end-to-end run, may take a min or two as it runs 2048 steps to fill PPO's rolloutbuffer
if os.path.exists(log_file_name):
    os.remove(log_file_name)
test_all_ppo_components()