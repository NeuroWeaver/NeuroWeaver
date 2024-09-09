import pprint

from qfdfg.graph import Graph
from runtime.runtime import Runtime
from testing_components import Brain, SingalSink

pp = pprint.PrettyPrinter(indent=4)

def test_straight_line_graph():
    print("three components in a straight line")
    deep_brain_stimulation = Graph("DeepBrainStim")

    brain = Brain()
    brain.set_output("brain_signal", (1,1))

    sink = SingalSink()
    sink.set_input("brain_signal", (1,1))

    pp.pprint(brain.name)
    pp.pprint(brain.__dict__)

    pp.pprint(sink.name)
    pp.pprint(sink.__dict__)

    print("-"*50)

    deep_brain_stimulation.add_component(brain)
    deep_brain_stimulation.add_component(sink)

    deep_brain_stimulation.add_flow("brain_signal", brain, "brain_signal", sink)
    runtime = Runtime(deep_brain_stimulation)
    runtime._use_futures = True
    runtime.initialize()
    runtime.execute()    

if __name__ == '__main__':
	test_straight_line_graph()




