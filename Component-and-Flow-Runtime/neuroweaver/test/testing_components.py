from qfdfg.component import Component
from typing import List
import numpy as np
import logging, time
import torch
# logging.basicConfig(format='%(levelname)-5s [%(filename)s:%(lineno)d] %(message)s',
#     level=logging.DEBUG)
logger = logging.getLogger(__name__) 

class AllQueueTypesSink(Component):
    @property
    def input_names(self) -> List[str]:
        return ["output2input", "state2input"]

    @property
    def state_names(self) -> List[str]:
        return ["state2state", "output2state"]

    def initialize(self, state2state, output2state):
        logger.debug("sink for all types of edges")

    def execute(self, output2input, state2input, state2state, output2state):
        logger.debug(f"{self._name}.execute")
        #logger.debug(f"s2s qsize: {state2state.qsize}")
        state1 = state2state.pop()
        state2 = output2state.pop()
        input1 = output2input.pop()
        input2 = state2input.pop()
        logger.debug(f"state_from_state: {state1}")
        logger.debug(f"state_from_output: {state2}")
        logger.debug(f"input_from_output: {input1}")
        logger.debug(f"input_from_state: {input2}")

class AllQueueTypesSource(Component):
    @property
    def state_names(self) -> List[str]:
        return ["state2state", "state2input"]

    @property
    def output_names(self) -> List[str]:
        return ["output2input", "output2state"]

    def initialize(self, state2state, state2input):
        logger.debug("source for all types of edges")

    def execute(self, state2state, state2input, output2input, output2state):
        logger.debug(f"{self._name}.execute")
        s2s = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64)
        s2i = s2s*2
        state2state.push(s2s, s2s.shape)
        state2input.push(s2i, s2i.shape)            

        o2i = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64)
        o2i = o2i*3
        o2s = o2i*4
        output2input.push(o2i, o2i.shape)
        output2state.push(o2s, o2s.shape)

class Brain_posix_mq(Component):
    @property
    def output_names(self) -> List[str]:
        return ["brain_signal"]

    def initialize(self):
        logger.debug("brain-v0-posix-mq")

    def execute(self, brain_signal):
        logger.debug(f"{self._name}.execute")        
        signal = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64)
        #signal = np.array([65, 66, 67], dtype=np.float64)
        logger.debug(f"{self._name}: signal {signal}")
        brain_signal.push(signal, (2,3))
        time.sleep(1)
        #arr = signal.tobytes()
        #logger.debug(f"{self._name}: arr {arr}")
        #brain_signal.send(signal.tobytes())

class Brain(Component):
    @property
    def output_names(self) -> List[str]:
        return ["brain_signal"]

    def initialize(self):
        logger.debug("brain-v0")

    def execute(self, brain_signal):
        signal = np.array([10])
        logger.debug(f"{self._name}: signal {signal}")
        brain_signal.push(signal, (1,1))

class SingalSink_posix_mq(Component):
    @property
    def input_names(self) -> List[str]:
        return ["brain_signal"]

    def initialize(self):
        logger.debug(f"initialize does nothing for SingalSink_posix_mq")
        pass

    def execute(self, brain_signal):
        logger.debug(f"{self._name}.execute")
        signal = brain_signal.pop()
        # raw, p = brain_signal.receive()
        # print(type(raw))
        # logger.debug(f"{self._name}: raw {raw}")
        # signal = np.frombuffer(raw, dtype=np.float64)
        # signal = signal.reshape(2,3)
        ## signal.reshape(1,1)
        logger.debug(f"{self._name}: signal {signal}")

class SingalSink(Component):
    @property
    def input_names(self) -> List[str]:
        return ["brain_signal"]

    def initialize(self):
        logger.debug(f"initialize does nothing")
        pass

    def execute(self, brain_signal):
        logger.debug(f"{self._name}: brain_signal.empty():{brain_signal.empty()}")
        signal = brain_signal.pop()
        logger.debug(f"{self._name}: signal {signal}")

class StimulationSink(Component):
    @property
    def input_names(self) -> List[str]:
        return ["stimulation"]

    def initialize(self):
        pass

    def execute(self, stimulation):        
        #logger.debug(f"{self._name}: stimulation.empty():{stimulation.empty()}")
        stimulating_signal = stimulation.pop()
        logger.debug(f"{self._name}: stimulation:{stimulating_signal}")

class SignalToStimulation_posix_mq(Component):  
    @property
    def input_names(self) -> List[str]:
        return ["brain_signal"]

    @property
    def output_names(self) -> List[str]:
        return ["stimulation"]

    # @property
    # def state_names(self) -> List[str]:
    #     return ["component_state"]

    # @property
    # def param_names(self) -> List[str]:
    #     return ["component_parameter"]

    #def initialize(self):
    #    print("we do nothing")

    def initialize(self):#, component_state):#, component_parameter):
        #component_parameter += 1
        #arr = np.array([1], dtype=np.float64)
        #component_state.push(arr, (1,))
        logger.debug(f"initialize does nothing")
        pass
    
    def execute(self, brain_signal, stimulation):
        #print("exec {self.name}")
        #state = component_state.pop()
        #logger.debug(f"state:{state}")     
        signal = brain_signal.pop()
        logger.debug(f"signal:{signal}")
        stimulation.push(signal, (2,3))


class SignalToStimulation(Component):    
    @property
    def input_names(self) -> List[str]:
        return ["brain_signal"]

    @property
    def output_names(self) -> List[str]:
        return ["stimulation"]

    @property
    def state_names(self) -> List[str]:
        return ["component_state"]

    @property
    def param_names(self) -> List[str]:
        return ["component_parameter"]

    def initialize(self, component_state, component_parameter):
        component_parameter += 1
        component_state.push([1], (1,1))
        logger.debug(f"initialize does something")
        pass

    def execute(self, brain_signal, component_state, stimulation):
        #print("exec {self.name}")
        logger.debug(f"{self._name}: component_state.empty():{component_state.empty()}")
        state = component_state.pop()
        logger.debug(f"state:{state}")
        logger.debug(f"brain_signal:{brain_signal}")        
        signal = brain_signal.pop()
        logger.debug(f"signal:{signal}")
        ## runtime get the stimulation queue out
        logger.debug(f"{self._name}: stimulation:{stimulation}")
        logger.debug(f"{self._name}: stimulation.is_interprocess:{stimulation.is_interprocess}")
        stimulation.push(signal, (1,1))
        logger.debug(f"{self._name}: stimulation.empty():{stimulation.empty()}")

class Trainer(Component):    
    @property
    def input_names(self) -> List[str]:
        return ["brain_signal"]

    @property
    def output_names(self) -> List[str]:
        return ["stimulation"]

    @property
    def state_names(self) -> List[str]:
        return ["weights"]

    @property
    def param_names(self) -> List[str]:
        return ["lp_parameter"]

    def initialize(self, weights, lp_parameter):
        lp_parameter += 1
        weights.push([20], (1,1))
        logger.debug(f"initialize does something")
        pass

    def execute(self, brain_signal, weights, stimulation):
        state = weights.pop()
        signal = brain_signal.pop()
        signal = state + signal
        ## runtime get the stimulation queue out
        logger.debug(f"{self._name}: signal {signal}")
        stimulation.push(state, (1,1))
        weights.push(state, (1,1))

class Inference(Component):
    @property
    def input_names(self) -> List[str]:
        return ["brain_signal"]
    
    @property
    def output_names(self) -> List[str]:
        return ["rl_output"]

    @property
    def state_names(self) -> List[str]:
        return ["weights_dmx"]

    @property
    def param_names(self) -> List[str]:
        return ["filepath"]

    def initialize(self, weights_dmx, filepath):
        logger.debug(f"initialize does something")
        ## load weight from file, we're not there yet
        weights_dmx.push([10], (1,1))
        pass

    def execute(self, brain_signal, weights_dmx, rl_output):
        signal = brain_signal.pop()
        weight = weights_dmx.pop()
        rl_val=np.dot(weight, signal) + 1
        rl_output.push(rl_val, (1,1))
        logger.debug(f"{self._name}: rl_output {rl_val}")

class WeightUpdate(Component):
    @property
    def input_names(self) -> List[str]:
        return ["weights"]
    
    @property
    def output_names(self) -> List[str]:
        return ["weights_dmx"]    

    def initialize(self):
        logger.debug(f"initialize does nothing")
        pass

    ## execute's weights can't pop things out
    def execute(self, weights, weights_dmx):
        w = weights.pop()
        weights_dmx.push(w, (1,1))

class SignalToStimulationOnGPU(Component):    
    @property
    def input_names(self) -> List[str]:
        return ["brain_signal"]

    @property
    def output_names(self) -> List[str]:
        return ["stimulation"]

    @property
    def state_names(self) -> List[str]:
        return ["component_state"]

    @property
    def param_names(self) -> List[str]:
        return ["component_parameter"]

    def initialize(self, component_state, component_parameter):
        component_parameter += 1
        logger.debug(f"initialize does something")
        pass

    def execute(self, brain_signal, component_state, stimulation):
        #print(f"exec {self.name}")
        logger.debug(f"{self._name}: brain_signal:{brain_signal}")
        logger.debug(f"{self._name}: stimulation:{stimulation}")
        logger.debug(f"{self._name}: stimulation.is_interprocess:{stimulation.is_interprocess}")

        signal = brain_signal.pop()
        logger.debug(f"signal:{signal}")        
        state = torch.tensor([21.], device="cpu")
        signal_tensor = torch.from_numpy(signal)

        cuda_is_here = torch.cuda.is_available()

        if self.device == "gpu" and cuda_is_here:
            signal_tensor = signal_tensor.to("cuda") ## move signal to GPU             
            state = state.to("cuda")
            state = state + signal_tensor
            ## Don't pass torch tensor over IPC queue
            state = state.cpu()  ## move signal back to GPU
        else:
            state = state + signal_tensor
        
        state = state.numpy()
        ## runtime get the stimulation queue out
        logger.debug(f"{self._name}: state {state}")
        stimulation.push(state, (1,1))
        component_state.push(state, (1,1))
        logger.debug(f"{self._name}: stimulation.empty():{stimulation.empty()}")
