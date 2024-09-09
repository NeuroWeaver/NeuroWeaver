import logging
import pprint

from qfdfg.graph import Graph
from runtime.runtime import Runtime
from testing_components import Brain, SingalSink, Trainer

logging.basicConfig(format='%(levelname)-5s [%(filename)s:%(lineno)d] %(message)s',
    level=logging.DEBUG)
logger = logging.getLogger(__name__) 


'''
[Brain]-(o)-(i)->[Training]-(o)
    \ 
    (o)
      \-(i)->[Sink]
'''
def test_branching_graph():
    logger.info("test_three_components")
    deep_brain_stimulation = Graph("DeepBrainStim")

    pp = pprint.PrettyPrinter(indent=4)
    brain = Brain()
    brain.set_output("brain_signal", (1,1))
    #logger.debug(brain.name)    
    #logger.debug(pp.pprint(brain.__dict__))

    trainer = Trainer(lp_parameter=1)
    trainer.set_input("brain_signal", (1,1))
    trainer.set_output("stimulation", (1,1))
    trainer.set_state("weights", (1,1))
    # logger.debug(loopback.name)
    # logger.debug(pp.pprint(loopback.__dict__))

    sink = SingalSink()
    sink.set_input("brain_signal", (1,1))
    # logger.debug(sink.name)
    # logger.debug(pp.pprint(sink.__dict__))

    deep_brain_stimulation.add_component(brain)
    deep_brain_stimulation.add_component(trainer)
    deep_brain_stimulation.add_component(sink)

    deep_brain_stimulation.add_flow("brain_signal", brain, "brain_signal", trainer)
    deep_brain_stimulation.add_flow("brain_signal", brain, "brain_signal", sink)
    # for k,v in deep_brain_stimulation.edges.items():
    #     print(k,"->",v)

    runtime = Runtime(deep_brain_stimulation)
    runtime._use_futures = True
    runtime.iterations = 5
    runtime.initialize()
    runtime.execute()

if __name__ == '__main__':
    test_branching_graph()




