import logging
from qfdfg.graph import Graph
import pprint
from runtime.runtime import Runtime
from testing_components import Brain, Trainer, Inference, WeightUpdate

logging.basicConfig(format='%(levelname)-5s [%(filename)s:%(lineno)d] %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__) 

''' Four-Component with state output
[Brain]-(o)-(i)->[Training]-(s)-(i)->[Weight update] 
    \                                   |
    (o)                                (o)
      \-(i)->[Inference] <-(s)----------|
                 |
                (o)

queue connection types
o: output queues, i: input queues, s: state quues
1. o->i: the most common one
2. s->s: simple state sharing
3. s->i [component] o->s: state sharing pass through another component
'''
def test_four_components():
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
    #training._device = "gpu"
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
    # This line depends on keep-running attribute of the "inference" component, TODO: Does it?
    deep_brain_stimulation.add_flow("weights_dmx", weight_update, "weights_dmx", inference)
    for k,v in deep_brain_stimulation.edges.items():
        print(k,"->",v)

    runtime = Runtime(deep_brain_stimulation)
    runtime.initialize()
    runtime.iterations = 5
    #print(runtime.iterations)
    runtime.execute()

''' Five-Component
[Brain]-(i)->[Training]-(s)-(i)->[Weight update] 
    \                              (o)   
     \                              |
      \-(i)->[Inference]<-(s)-------|
                |
               (o)
                |
               (i)
                |
                V
        [Action to stimlation]    
'''

#test_three_components()
test_four_components()




