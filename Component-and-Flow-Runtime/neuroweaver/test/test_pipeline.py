from qfdfg.graph import Graph
import numpy as np
from qfdfg.component import Component
from typing import List
from qfdfg.flow import Flow, FlowQueue
import pprint
import queue
import gym_oscillator # for using oscillator in gym env
import oscillator_src.oscillator_cpp # for the oscillator code

import gym
import torch
# from time import sleep
# from stable_baselines3.common.base_class import BaseAlgorithm
from stable_baselines3 import PPO

class Brain(Component):

    @property
    def output_names(self) -> List[str]:
        return ["brain_signal"]

    def initialize(self):
        self._signal_generator = gym.make('oscillator-v0')
        print("oscillator-v0")

    def execute(self, brain_signal):
        signal = np.random.randint()
        brain_signal.push(signal)


class FFT(Component):

    @property
    def input_names(self) -> List[str]:
        return ["brain_signal"]

    @property
    def output_names(self) -> List[str]:
        return ["fft_output"]

    def execute(self, brain_signal, fft_output):
        fft_output.push(brain_signal)

class FftDmxRLTrainer(Component):


    @property
    def input_names(self) -> List[str]:
        return ["fft_output"]

    @property
    def output_names(self) -> List[str]:
        return ["fft_dmx"]

    def execute(self, fft_output, fft_dmx):
        fft_dmx.push(fft_output)

class RLTrainer(Component):

    @property
    def param_names(self) -> List[str]:
        return ["filepath"]

    @property
    def input_names(self) -> List[str]:
        return ["fft_dmx"]

    @property
    def state_names(self) -> List[str]:
        return ["weights"]

    def initialize(self, weights, filepath):

        weights.push(open(filepath))
        # TODO: Move env to separate component
        env = gym.make('oscillator-v0')
        self.model = PPO("MlpPolicy", env, verbose=1)
        self.timer = 0

    def execute(self, fft_dmx, weights):
        self.model.train(fft_dmx, timesteps=1000)
        if self.timer %1000 == 0:
            weights.push()
            weights.push(self.model.get_parameters())
        self.timer += 1


class RLTrainerDmxRLInference(Component):


    @property
    def input_names(self) -> List[str]:
        return ["weights"]

    @property
    def output_names(self) -> List[str]:
        return ["weights_dmx"]

    def execute(self, weights, weights_dmx):
        weights_dmx.push(weights)


class RLInference(Component):

    @property
    def param_names(self) -> List[str]:
        return ["filepath"]

    @property
    def input_names(self) -> List[str]:
        return ["fft_dmx"]

    @property
    def state_names(self) -> List[str]:
        return ["weights_dmx"]

    @property
    def output_names(self) -> List[str]:
        return ["rl_output"]

    def initialize(self, weights_dmx, filepath):
        weights_dmx.push(open(filepath))
        # Placeholder code for when polymath is compiled
        env = gym.make('oscillator-v0')
        self.model = PPO("MlpPolicy", env, verbose=1)


    def execute(self, fft_dmx, weights_dmx, rl_output):
        if weights_dmx:
            self.model.set_parameters(weights_dmx.pop())
        rl_res, _ = self.model.predict(fft_dmx)
        rl_output.push(rl_res)

class ActionToStimulation(Component):

    @property
    def input_names(self) -> List[str]:
        return ["rl_output"]

    @property
    def output_names(self) -> List[str]:
        return ["stimulation"]

    def initialize():
        pass

    def execute(self, rl_output, stimulation):
        stimulation.push(rl_output)


class LoopBack(Component):    
    @property
    def input_names(self) -> List[str]:
        return ["brain_signal"]

    @property
    def output_names(self) -> List[str]:
        return ["stimulation"]

    def initialize(self):
        print(f"initialize does nothing")
        pass

    def execute(self, brain_signal, stimulation):
        ## runtime get the stimulation queue out
        stimulation.push(brain_signal)

class MiddleMan(Component):    
    @property
    def state_names(self) -> List[str]:
        return ["middle_state"]

    @property
    def input_names(self) -> List[str]:
        return ["brain_signal"]

    @property
    def output_names(self) -> List[str]:
        return ["brain_signal"]

    def initialize(self, middle_state):
        print(f"initialize middle_state")
        middle_state.push(np.float64(np.randint(0, 100)))

    def execute(self, brain_signal, middle_state, stimulation):
        ## runtime get the stimulation queue out
        stimulation.push(brain_signal)


class Runtime(object):
    def __init__(self, verbose:bool =False):
        self._runqueue = queue.Queue()
    
    def initialize(self, graph: Graph):
        for comp in graph.components:
            ## how to know initialize() with different number of argurments?
            ## class method? https://docs.python.org/3/library/functools.html#functools.singledispatch 
            '''
            def initialize(self, *args):
                pass
            def execute(self, *args, **kwargs):
                raise NotImplemented
            '''
            comp.initialize()

def test_class_creation():
    print("test_class_creation")
    deep_brain_stimulation = Graph("DeepBrainStim")

    pp = pprint.PrettyPrinter(indent=4)
    brain = Brain()
    brain.set_output("brain_signal", (100,1))
    pp.pprint(brain.name)
    pp.pprint(brain.__dict__)
    loopback = LoopBack()
    loopback.set_input("brain_signal", (100,1))
    loopback.set_output("stimulation", (100,1))
    pp.pprint(loopback.name)
    pp.pprint(loopback.__dict__)

    # fft = FFT()
    # fft_dmx_rl_trainer = FftDmxRLTrainer()
    # rl_trainer_dmx_rl_inference = RLTrainerDmxRLInference()
    # rl_trainer = RLTrainer(filepath="test")
    # rl_inference = RLInference(filepath="test")
    # action_to_stim = ActionToStimulation()

    # graph.add_component(brain)
    # graph.add_component(fft)
    # graph.add_component(fft_dmx_rl_trainer)
    # graph.add_component(rl_trainer_dmx_rl_inference)
    # graph.add_component(rl_trainer)
    # graph.add_component(rl_inference)
    # graph.add_component(action_to_stim)
    deep_brain_stimulation.add_component(brain)
    deep_brain_stimulation.add_component(loopback)
    deep_brain_stimulation.add_flow("brain_signal", brain, "brain_signal", loopback)
    runtime = Runtime(deep_brain_stimulation)
    runtime.initialize(deep_brain_stimulation)

    # graph.add_flow("brain_signal", brain, "brain_signal", fft)
    # graph.add_flow("fft_output", fft, "fft_output", fft_dmx_rl_trainer)
    # graph.add_flow("fft_dmx", fft_dmx_rl_trainer, "fft_dmx", rl_trainer)
    # graph.add_flow("weights", rl_trainer, "weights", rl_trainer_dmx_rl_inference)
    # graph.add_flow("weights_dmx", rl_trainer_dmx_rl_inference, "weights_dmx", rl_inference)
    # graph.add_flow("rl_output", rl_inference, "rl_output", action_to_stim)

# import queue
# from typing import NewType
# QueueType= NewType('simple_queue', queue.Queue)

# def push(queue:QueueType, item: int):
#     print(type(queue))
#     queue.put(item)

# q = queue.Queue()
# push(q,1)

test_class_creation()




