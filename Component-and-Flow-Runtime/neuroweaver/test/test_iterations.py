
from qfdfg.component import Component
from qfdfg.graph import Graph
from runtime.runtime import Runtime
from typing import List
import numpy as np
import pprint
pp = pprint.PrettyPrinter(indent=4)

class OutputClass(Component):
    @property
    def output_names(self) -> List[str]:
        return ["output_signal"]
    
    def initialize(self):
        #print(self._iterations)
        pass

    def execute(self, output_signal):
        signal = np.array([10])        
        output_signal.push(signal, (1,1))
        print(output_signal.queue.qsize())

class InputClass(Component):
    @property
    def input_names(self) -> List[str]:
        return ["input_signal"]

    def initialize(self):
        pass

    def execute(self, input_signal):
        #print(f"{self._name}: input_signal:{input_signal}")
        #print(f"{self._name}: input_signal.empty():{input_signal.empty()}")
        stimulating_signal = input_signal.pop()
        print(stimulating_signal)

def test_io_loops():
    io_test = Graph("Testing I/O")    

    iterations = 5
    
    source = OutputClass()  
    source._iterations = iterations
    source.set_output("output_signal", (1,1))
    output_q = source.output_queues["output_signal"]    
    pp.pprint(source.__dict__)

    sink = InputClass()
    sink.set_input("input_signal", (1,1))
    input_q = sink.input_queues["input_signal"]  

    io_test.add_component(source)
    io_test.add_component(sink)
    io_test.add_flow("output_signal", source, "input_signal", sink)

    runtime = Runtime(io_test)
    runtime.initialize()
    runtime.execute()

    assert input_q.qsize() == 0  ## completely drained
    assert output_q.qsize() == 0 ## completely drained too


test_io_loops()