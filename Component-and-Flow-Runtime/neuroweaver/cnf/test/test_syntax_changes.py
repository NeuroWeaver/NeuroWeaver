from qfdfg.component import Component
from qfdfg.graph import Graph
from qfdfg.flow import Flow
import ohai.digital_signal_processing as dsp

import gym
import torch
from time import sleep
from stable_baselines3.common.base_class import BaseAlgorithm
from stable_baselines3 import PPO

## TODO: generate the brain signal from oscillator

## TODO: how to have (1) init phase, like settting up weights (2) running phase
## TODO: termination condition for the entire program

# Rule: A non-sink component MUST have at least one state and/or output


# Semantic Definitions
## States
### States represent data which is required to be initialized at compile time, and may be read or written at different intervals
### State values are not required to be present in order for component executiuon to occur
## Parameters
### Parameters are static, named values for usage during both compilation and runtime. They are not modeled as queues, as their value is the same throughout execution
### Examples include filepath, learning rate, etc

# class CompSignal(Component):


with Component(outputs=[fft_out]) as comp_signal:
	with comp_signal.runtime() as comp_signal_runtime:
		signal = create_signal()

### OPTION 2: Users define when data is written to a queue directing in the runtiem code

with Component(inputs=[fft_dmx_queue], states=[weights], parameters=[filepath]) as comp_training:

	# The code within the "compile" context will be executed during compilation
	# It will be stored as an attribute in the "Component" object
	with comp_training.compile(shared=[model]) as comp_train_compile:
		# Populate queue
		weight_vars = open(filepath)
		weights.push(weight_vars)

		# TODO: Move env to separate component
		env = gym.make('oscillator-v0')
		model = PPO("MlpPolicy", env, verbose=1)


	with comp_training.runtime(timeval) as comp_train_runtime:

		fft_res = fft_dmx_queue.pop()
		model.train(fft_res, timesteps=1000)
		if timeval % 1000 == 0:
			weights.push(model.get_parameters())

###################################################################################



## TODO: a dmx component for train -> inference

## TODO: weights should be a state argument (e.g. state input, state output)
## do we need new senmatics for this weight update? -> it's periodic input for the weights
##
with Component(inputs=[fft_dmx], states=[weights], outputs=[action], parameters=[filepath]) as comp_inference:

	with comp_inference.compile(shared=[model]) as comp_inference_compile:
		weight_vars = open(filepath)
		weights.push(weight_vars)
		model.set_parameters(weights)

	## poll the input queue for weights input
	with comp_inference.runtime(_) as comp_inference_runtime:
		## treat fft_max as a queue

		# This solution can potentially be optimized by te
		if not weights.empty():
			model.set_parameters(weights.pop())

		fft_dmx_element = fft_dmx.pop()
		action_element , _states = model.predict(fft_dmx_element)
		action.push(action_element)
		obs, rewards, dones, info = env.step(action_element)

## TODO: a component update the FPGA weights, thinking about how to do it with FPGA but do it on CPU

## TODO: translate the "action" output from inference to menaingful actions
## back to source

signal = comp_signal()
trained_weights = comp_training(input_names=[signal], states=[None], parameters=["weights.csv"])
# action, _ = comp_inference(input_names=[env_input], states=[trained_weights], parameters=["weights.csv"])

# The semantics for variables for returned queues from Component instantiation are as follows:
#  <output1>, ..., <output_n>, <state1>, ..., <state_n> = <component_name>(input_names=[<input1>, ..., <input_n>], states=[<state1>, ..., <state_n>], parameters=[<param1>, ..., <param_n>])
