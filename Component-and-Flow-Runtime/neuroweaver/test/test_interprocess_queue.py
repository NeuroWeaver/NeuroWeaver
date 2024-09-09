import pprint

from qfdfg.graph import Graph
from runtime.runtime import Runtime
from testing_components import Brain, StimulationSink, SignalToStimulationOnGPU

pp = pprint.PrettyPrinter(indent=4)

def test_straight_line_graph():
    print("three components in a straight line")
    deep_brain_stimulation = Graph("DeepBrainStim")

    brain = Brain()
    brain.set_output("brain_signal", (1,1))

    singal2stimu = SignalToStimulationOnGPU(component_parameter=1)
    singal2stimu.set_input("brain_signal", (1,1))
    singal2stimu.set_output("stimulation", (1,1))
    singal2stimu.set_state("component_state", (1,1))
    singal2stimu._device = "gpu"

    sink = StimulationSink()
    sink.set_input("stimulation", (1,1))

    pp.pprint(brain.name)
    pp.pprint(brain.__dict__)

    pp.pprint(singal2stimu.name)
    pp.pprint(singal2stimu.__dict__)

    pp.pprint(sink.name)
    pp.pprint(sink.__dict__)

    print("-"*50)

    deep_brain_stimulation.add_component(brain)
    deep_brain_stimulation.add_component(singal2stimu)
    deep_brain_stimulation.add_component(sink)

    deep_brain_stimulation.add_flow("brain_signal", brain, "brain_signal", singal2stimu)
    deep_brain_stimulation.add_flow("stimulation", singal2stimu, "stimulation", sink)
    runtime = Runtime(deep_brain_stimulation)
    runtime._use_futures = False
    runtime.iterations = 5
    runtime.initialize()
    runtime.execute()    

if __name__ == '__main__':
	test_straight_line_graph()




