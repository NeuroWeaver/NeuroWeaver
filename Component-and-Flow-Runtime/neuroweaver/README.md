# Neuroweaver

Neuroweaver is a framework to utilize multiple domain-specific accelerators for end-to-end cross-domain applications. 
Neuroweaver provides a simple and lightweight programming interface, called Component and Flow programming model, which allows application programmers to specify various components of their program to be targeted for acceleration. 
Finally, Neuroweaver is equipped with a runtime system which creates a component and flow graph, schedules the components and handles the data transfers between components.

This repository consists of the source code for the component and flow classes, runtime, as well as example application programs to run.

## Repository structure
The qfdfg folder contains the implementation of the Component, Flow and Graph classes. 
The runtime folder contains the implementation of the Runtime class

## Writing your first component and flow program

### Component
A programmer creating a new component for their application extends the `Component` baseclass.
The programmer optionally defines one or more of the following four methods with the `@property` decorator
- `input_names`
- `output_names`
- `state_names`
- `property_names`

Each of them return a list of strings which are the respective queue names.
The programmer also extends the baseclass with the following two methods:
- `initialize`
- `execute`

In the following toy example a simple component called Brain is created. It has one output queue, called 
`brain_signal`.

```python

from qfdfg.component import Component
from typing import List
import numpy as np

'''
This component is used to emulate the brain generating a signal
It has one output called brain_signal
'''
class Brain(Component):
    # create an output named brain_signal
    @property
    def output_names(self) -> List[str]:
        return ["brain_signal"]
    
    # runs once during initialization of the component
    def initialize(self):
        print("brain-v0")

    # pushes generated signal to output
    def execute(self, brain_signal):
        signal = np.array([10])
        print(f"{self._name}: signal {signal}")
        brain_signal.push(signal, (1,1))

```

The `initialize` method can be used for code to set up the initial state of the component and perform other one time tasks
The `execute` method contains most of the functionality of the code. The `execute` function runs every time an input is available on any of the input queues.
In the above example there is no input queue, so it will run only once.

The following example creates another component called `SignalSink`. This component will receive a `brain_signal` input.

```python

'''
This component receives a brain signal. Currently it simply logs the received signal.
'''
class SignalSink(Component):
    # create an input named brain_signal
    @property
    def input_names(self) -> List[str]:
        return ["brain_signal"]

    def initialize(self):
        print(f"initialize does nothing")

    def execute(self, brain_signal):
        signal = brain_signal.pop()
        print(f"{self._name}: signal {signal}")
```

The `Component` class provides the following methods which initialize the queues for each of the interfaces with a shape
-  `set_input`
-  `set_output`
-  `set_state`
The shape is provided as a tuple, e.g. (100,1) for a 1-D array with 100 elements. Every element pushed to the queue needs to be this particular shape.
The following code snippet initilizes `Brain` and `SignalSink` components. The output queue `brain_signal` of `brain` instance is set to aceept shape (1,1).
The input queue `brain_signal` of `sink` instance is set to accept shape (1,1) as well. 

```python
# Initialize the Brain and SignalSink components
brain = Brain()
sink = SignalSink()

# Bind the output and input names to Queues
brain.set_output("brain_signal", (1,1))
sink.set_input("brain_signal", (1,1))
```


### Graph
The graph class allows the programmer to declare a component and flow program.
The `add_component` method is used to add components to the graph. In the following example, we add `brain` as a component to a graph called 
`graph` 
```python
brain = Brain()
graph.add_component(brain)
```

The `add_flow` method is used to connect two components with a flow.
We specify source and destination component instance along with their corresponding queue names. In the following example, we add a flow to a graph called 
`graph` by specifying the source component `brain` with its output queue name `brain_singal` and the destination component with its input queue name `brain_signal`.
```python
brain = Brain()
sink = SignalSink()

brain.set_output("brain_signal", (1,1))
sink.set_input("brain_signal", (1,1))

graph.add_flow("brain_signal", brain, "brain_signal", sink)
```

The following code snippet adds `Brain` and `SignalSink` components to a graph called `deep_brain_stimulation`. 
Their queues are initialized. A flow is created between the two components.

```python
from qfdfg.graph import Graph

# Create a component and flow (CNF) graph. This is named DeepBrainStim
deep_brain_stimulation = Graph("DeepBrainStim")

# Initialize the Brain and SignalSink components
brain = Brain()
sink = SignalSink()

# Bind the output and input names to Queues
brain.set_output("brain_signal", (1,1))
sink.set_input("brain_signal", (1,1))

# Add components to the graph
deep_brain_stimulation.add_component(brain)
deep_brain_stimulation.add_component(sink)

# Create a flow between the brain component and the sink component
deep_brain_stimulation.add_flow("brain_signal", brain, "brain_signal", sink)
```


### Runtime
The runtime is initialized with an instance of the component and flow graph object. 
The `initialize` method of the graph class is used to initialize all the components in the graph.
The `execute` method begins the execution. The runtime will schedule ready components and do the data transfers according to the flows specified.

For example, the following snippet of code can be used to begin the execution of the CNF program previously

```python
from runtime.runtime import Runtime
runtime = Runtime(deep_brain_stimulation)
# Run the initialize functions of all components
runtime.initialize()
# Begin execution
runtime.execute()   
```

### Your first runnable CNF program
With the all the pieces from the pervious sections, we now have a runnable CNF program with two components.

```python
from runtime.runtime import Runtime
from qfdfg.graph import Graph

class Brain(Component):
    @property
    def output_names(self) -> List[str]:
        return ["brain_signal"]
    
    def initialize(self):
        print("brain-v0")

    def execute(self, brain_signal):
        signal = np.array([10])
        print(f"{self._name}: signal {signal}")
        brain_signal.push(signal, (1,1))

class SignalSink(Component):
    @property
    def input_names(self) -> List[str]:
        return ["brain_signal"]

    def initialize(self):
        print(f"initialize does nothing")

    def execute(self, brain_signal):
        signal = brain_signal.pop()
        print(f"{self._name}: signal {signal}")

# Create a component and flow (CNF) graph. This is named DeepBrainStim
deep_brain_stimulation = Graph("DeepBrainStim")

# Initialize the Brain and SignalSink components
brain = Brain()
sink = SignalSink()

# Bind the output and input names to Queues
brain.set_output("brain_signal", (1,1))
sink.set_input("brain_signal", (1,1))

# Add components to the graph
deep_brain_stimulation.add_component(brain)
deep_brain_stimulation.add_component(sink)

# Create a flow between the brain component and the sink component
deep_brain_stimulation.add_flow("brain_signal", brain, "brain_signal", sink)

runtime = Runtime(deep_brain_stimulation)
# Run the initialize functions of all components
runtime.initialize()
# Begin execution
runtime.execute()   
```