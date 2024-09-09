import logging
import pprint

from qfdfg.graph import Graph
from runtime.runtime import Runtime
from testing_components import Brain, Trainer, Inference, WeightUpdate

logging.basicConfig(format='%(levelname)-5s [%(filename)s:%(lineno)d] %(message)s',
    level=logging.DEBUG)
logger = logging.getLogger(__name__) 


''' Four-Component with state output
[Brain]-(o)-(i)->[Training]-(s)-(i)->[Weight update] 
    \ 
    (o)                                                  
      \-(i)->[Inference]                                
                 |
                (o)
'''

def test_state_queues_graph():
    logger.info("test_four_components with cyclic")
    deep_brain_stimulation = Graph("DeepBrainStim")

    pp = pprint.PrettyPrinter(indent=4)
    brain = Brain()
    brain.set_output("brain_signal", (1,1))
    #logger.debug(brain.name)    
    #logger.debug(pp.pprint(brain.__dict__))

    training = Trainer(lp_parameter=1)
    training.set_input("brain_signal", (1,1))
    training.set_output("stimulation", (1,1))
    training.set_state("weights", (1,1))
    # training._device = "gpu"
    # logger.debug(loopback.name)
    # logger.debug(pp.pprint(loopback.__dict__))

    weight_update = WeightUpdate()
    weight_update.set_input("weights", (1,1))
    weight_update.set_output("weights_dmx", (1,1))
    #weight_update._device = "cpu"

    inference= Inference(filepath="./weights.txt")
    inference.set_input("brain_signal", (1,1))
    inference.set_state("weights_dmx", (1,1))
    inference.set_output("rl_output", (1,1))
    # logger.debug(sink.name)
    # logger.debug(pp.pprint(sink.__dict__))

    deep_brain_stimulation.add_component(brain)
    deep_brain_stimulation.add_component(training)
    deep_brain_stimulation.add_component(inference)
    deep_brain_stimulation.add_component(weight_update)

    deep_brain_stimulation.add_flow("brain_signal", brain, "brain_signal", training)
    deep_brain_stimulation.add_flow("brain_signal", brain, "brain_signal", inference)
    deep_brain_stimulation.add_flow("weights", training, "weights", weight_update)
	# TODO: this line depends on keep-running attribute of the "inference" component
    # deep_brain_stimulation.add_flow("weights_dmx", inference, "weights_dmx", weight_update)
    # for k,v in deep_brain_stimulation.edges.items():
    #     print(k,"->",v)

    runtime = Runtime(deep_brain_stimulation)
    runtime._use_futures = True
    runtime.iterations = 5
    runtime.initialize()
    runtime.execute()

test_state_queues_graph()




