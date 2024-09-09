from collections import defaultdict
from .flow import Flow, FlowQueue
from typing import Any, List, Dict, Tuple
import inspect
from enum import Enum
from multiprocessing import shared_memory as shm
        
class ComponentStatus(Enum):
    created=1    
    initialized=2
    running=3
    paused=4
    completed=5

class Component(object):
    ID_COUNTER = 0
    INSTANCES = {}

    ## status of the components: stopped, running, paused, completed.
    ## Walk through the graph with BFS but it doesn't mean the whole graph is completed
    ## as the "source" of the entire graph can generate more inputs.
    ## A realistic example e.g. stop->run->pause->run->pause-> completed 
    ## (only if the "source" component is marked as completed)

    def __init__(self,
                 inputs=None,
                 outputs=None,
                 states=None,
                 header=None,
                 cid=None,
                 compilation=None,
                 runtime_args=None,
                 compilation_args=None,
                 device="cpu",
                 runtime=None, **kwargs):
        name = self.__class__.__name__
        # if cid:
        #     self._cid = cid
        #     assert name in Component.INSTANCES, f"{name} is not an existing component for instantiation"
        #     Component.INSTANCES[name] += 1
        # else:
        self._cid = Component.ID_COUNTER
        Component.ID_COUNTER += 1
        # Component.INSTANCES[name] = 0
        self._input_queues = inputs or {}
        self._state_queues = states or {}
        self._output_queues = outputs or {}
        # assert all(isinstance(i, FlowQueue) for i in self.input_queues)
        assert all(isinstance(v, FlowQueue) for _, v in self._output_queues.items())
        # assert all(isinstance(s, FlowQueue) for s in self.state_queues)

        self._parameters = kwargs

        self._name = name

        if len(self.init_arg_names) > 0:
            init_sig = inspect.signature(self.initialize)
            if len(init_sig.parameters) != (len(self.init_arg_names)):
                raise RuntimeError(
                    f"Arguments for the init function  in component {name} do not match the names of component arguments:\n"
                    f"Implementation arguments: {list(init_sig.parameters.keys())}\n"
                    f"User-defined argument names: {(self.init_arg_names)}")

            for i, p in enumerate(init_sig.parameters):
                if self.init_arg_names[i] != p:
                    raise RuntimeError(f"Parameter arguments do not much initialize function signature:\n"
                                       f"Signature: {list(init_sig.parameters.keys())}\n"
                                       f"Param names: {self.init_arg_names}")
                elif p not in kwargs and p in self.param_names:
                    raise RuntimeError(f"Missing parameter definition for component {name} instantiation:\n"
                                       f"Parameter: {p}")

        exec_sig = inspect.signature(self.execute)
        if len(exec_sig.parameters) != (len(self.exec_arg_names)):
            raise RuntimeError(f"Arguments for the execution function in {name} do not match the names of component arguments:\n"
                               f"Implementation arguments: {list(exec_sig.parameters.keys())}\n"
                               f"User-defined argument names: {self.exec_arg_names}")

        impl_sig = []

        for i, inp in exec_sig.parameters.items():

            assert i in self.exec_arg_names, f"Argument {i} does not match the input/outputs names defined for {name}:\n" \
                                              f"{self.exec_arg_names}"
            impl_sig.append(i)

        assert impl_sig == (self.exec_arg_names)


        self._instances = []

        self._compilation_args = compilation_args or {}
        self._runtime_args = runtime_args or {}

        self._compilation = compilation or []
        self._runtime = runtime or []
        self._header = header
        self._device = device
        self._process_handle = None
        self._component_status = ComponentStatus.created
        self._iterations = -1
        self._is_observed = False #True
        self._ingress_timestamps = None
        self._egress_timestamps = None

    @property
    def init_arg_names(self):
        return self.state_names + self.param_names

    @property
    def exec_arg_names(self):
        return self.input_names + self.state_names + self.output_names

    @property
    def read_queues(self):
        return self.input_names + self.state_names

    @property
    def write_queues(self):
        return self.output_names + self.state_names

    @property
    def name(self) -> str:
        return self._name

    @property
    def cid(self) -> int:
        return self._cid

    @property
    def input_names(self) -> List[str]:
        return []

    @property
    def state_names(self) -> List[str]:
        return []

    @property
    def param_names(self) -> List[str]:
        return []

    @property
    def input_queues(self):
        return self._input_queues

    @property
    def output_queues(self):
        return self._output_queues

    @property
    def state_queues(self):
        return self._state_queues		

    @property
    def output_names(self) -> List[str]:
        return []

    @property
    def compilation(self) -> List[str]:
        return []

    @property
    def runtime(self) -> List[str]:
        return []

    @property
    def header(self) -> str:
        return self._header

    @property
    def compilation_args(self):
        return self._compilation_args

    @property
    def runtime_args(self):
        return self._runtime_args

    @property
    def compilation_str(self) -> str:
        return "".join(self.compilation)

    @property
    def runtime_str(self) -> str:
        return "".join(self.runtime)

    def initialize(self, *args):
        ## for timestampings the start and end of the execution
        if self._is_observed:
            llist = [0.0] * self._iterations
            print(f"{self.name}_{self._cid}_ingress_timestamps")
            self._ingress_timestamps = shm.ShareableList(llist, name = f"{self.name}_{self._cid}_ingress_timestamps")
            self._egress_timestamps  = shm.ShareableList(llist, name = f"{self.name}_{self._cid}_egress_timestamps")
        else:
            pass
    
    def execute(self, *args, **kwargs):
        raise NotImplemented

    def destory(self):
        ## clean up the timestamps shared list
        if self._is_observed:
            ## TODO: flush list to a file
            #print(f"{self.name}_{self._cid}_ingress_timestamps")
            ingress_list = shm.ShareableList(name=f"{self.name}_{self._cid}_ingress_timestamps")
            ingress_list.shm.close()
            ingress_list.shm.unlink()
            egress_list = shm.ShareableList(name=f"{self.name}_{self._cid}_egress_timestamps")
            egress_list.shm.close()
            egress_list.shm.unlink()
        else:
            pass

    @property
    def component_status(self) -> ComponentStatus:
        return self._component_status

    @component_status.setter
    def component_status(self, status: ComponentStatus):
        self._component_status = status

    @property
    def iterations(self) -> int:
        return self._iterations
    
    @iterations.setter
    def iterations(self, iter: int):
        self._iterations = iter

    @property
    def device(self) -> str:
        return self._device

    ## TODO: merge this into set_intput, set_output, and set_state with 
    # if self._deivce != "cpu": # when the component wants to run on something no CPU
    #     q = FlowQueue(name, shape, queue_type, interprocess=True)

    def set_interprocess_queues(self, name, shape, queue_type):
        assert name in self.input_names or name in self.state_names \
            or name in self.output_names
        q = FlowQueue(name, shape, queue_type, interprocess=True)
        # print(f"set_interprocess_queues, queue {q}")
        if queue_type == "input":
            self._input_queues[name] = q
        elif queue_type == "state":
            self._state_queues[name] = q
        elif queue_type == "output":
            self._output_queues[name] = q
        else:
            raise RuntimeError(f"Invalid type {queue_type} for queues of the component {self._name}")

    def set_input(self, name, shape, is_process_parallel=True, is_observed=False,is_interprocess=False):
        assert name in self.input_names and name not in self.input_queues
        if is_process_parallel == False:
            q = FlowQueue(name, shape, queue_type="input", interprocess=is_interprocess)
            self._input_queues[name] = q
        else:
            self._input_queues[name] = shape, is_observed

    def set_state(self, name, shape, is_process_parallel=True, is_observed=False, is_interprocess=False):
        assert name in self.state_names and name not in self.state_queues
        if is_process_parallel == False:
            q = FlowQueue(name, shape, queue_type="state", interprocess=is_interprocess)
            self._state_queues[name] = q
        else:
            self._state_queues[name] = shape, is_observed

    def set_output(self, name, shape, is_process_parallel=True, is_observed=False, is_interprocess=False):
        assert name in self.output_names and name not in self.output_queues
        if is_process_parallel == False:
            q = FlowQueue(name, shape, queue_type="output", interprocess=is_interprocess)
            self._output_queues[name] = q
        else:
            self._output_queues[name] = shape, is_observed

    def set_header(self, header):
        assert self.header is None
        self._header = header

    def set_input_names(self, input_names):
        assert len(self.input_names) == 0, f"Input names already set for component definition {self.name}:\n" \
                                           f"Existing names: {self.input_names}\n" \
                                           f"New names: {input_names}"
        self._input_names = input_names

    def set_output_names(self, output_names):
        assert len(self.output_names) == 0, f"Output names already set for component definition {self.name}:\n" \
                                           f"Existing names: {self.output_names}\n" \
                                           f"New names: {output_names}"
        self._output_names = output_names

    def set_state_names(self, state_names):
        assert len(self.state_names) == 0, f"State names already set for component definition {self.name}:\n" \
                                           f"Existing names: {self.state_names}\n" \
                                           f"New names: {state_names}"
        self._state_names = state_names

    def set_param_names(self, param_names):
        assert len(self.param_names) == 0, f"Parameter names already set for component definition {self.name}:\n" \
                                           f"Existing names: {self.param_names}\n" \
                                           f"New names: {param_names}"
        self._param_names = param_names

    def set_compilation_args(self, comp_args):
        assert len(self.compilation_args) == 0
        self._compilation_args = comp_args

    def set_runtime_args(self, runtime_args):
        assert len(self.runtime_args) == 0
        self._runtime_args = runtime_args

    def set_compilation(self, compilation_lines):
        assert len(self.compilation) == 0
        self._compilation = compilation_lines

    def set_runtime(self, runtime_lines):
        assert len(self.runtime) == 0
        self._runtime = runtime_lines

    def add_output_name(self, argname):
        self._output_names.append(argname)

    def add_input_name(self, argname):
        self._input_names.append(argname)

    def add_state_name(self, argname):
        self._state_names.append(argname)

    def add_param_name(self, argname):
        self._param_names.append(argname)

    def instantiate(self, instance_name, inputs, outputs, states=None) -> 'ComponentInstance':
        return ComponentInstance(instance_name, Component.INSTANCES[self.name] - 1, inputs, outputs, self.copy(), states=states)

    def copy(self) -> 'Component':
        return Component(self.name, self.input_names.copy(), self.output_names.copy(),
                         states=self.state_names.copy(),
                         cid=self.cid,
                         params=self.param_names.copy(),
                         compilation=self.compilation.copy()
                         )

    def is_valid(self):
        return len(self.runtime) != 0

class ComponentInstance(object):

    def __init__(self, inst_id, instance_name, inputs, outputs, definition, states=None):
        self._instance_id = inst_id
        self._instance_name = instance_name
        self._inputs = inputs
        self._outputs = outputs
        self._states = states or []
        self._flowlist = []
        self._definition = definition


    @property
    def definition(self) -> Component:
        return self._definition

    @property
    def definition_name(self) -> str:
        return self.definition.name

    @property
    def instance_name(self) -> str:
        return self._instance_name

    @property
    def instance_id(self) -> str:
        return self._instance_id

    @property
    def inputs(self) -> List:
        return self._inputs

    @property
    def states(self):
        return self._states

    @property
    def outputs(self):
        return self._outputs

    @property
    def flowlist(self) -> List[Flow]:
        return self._flowlist

    def add_flow(self, flow):
        self._flowlist.append(flow)
