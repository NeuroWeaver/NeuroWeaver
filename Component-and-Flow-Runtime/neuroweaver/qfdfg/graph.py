from .component import Component, ComponentInstance
from typing import List, Dict
import pprint, logging

pp = pprint.PrettyPrinter(indent=4)
class Graph(object):
    def __init__(self, name):
        self._name = name
        self._components = []

        # self._edges = []
        self._edges = {}
        # name -> _components index
        self._component_map = {}
        self.using_only_threads = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def components(self) -> List[Component]:
        return self._components

    @property
    def edges(self):
        return self._edges

    @property
    def component_names(self):
        return [c.name for c in self.components]
    
    def get_component_byname(self, name: str) -> Component:
        index = self._component_map.get(name)        
        return self._components[index] 

    def add_component(self, component: Component):
        assert component not in self.components
        self._components.append(component)
        self._component_map[component.name] = len(self._components) - 1
        # print(f"component.name {component.name}, index: {self._component_map[component.name]}")

    def get_queue_component(self, qname) -> Component:
        for c in self.components:
            if qname in c.exec_arg_names:
                return c
        raise RuntimeError(f"Could not find queue with name {qname}")
    
    ## Convert existing queue.Queue to multiprocessing.Queue if the edge is cross process 
    ## Components on different devices are on different process
    ## this method works for the main process coordinating and relaying 
    ## communication to all the other process
    def convert_queues(self, src_q, src_comp, dst_q, dst_comp):        
        # print("-"*12, "before ipc queue handling", "-"*13)
        # pp.pprint(src_comp.name)
        # pp.pprint(src_comp.__dict__)
        # pp.pprint(dst_comp.name)
        # pp.pprint(dst_comp.__dict__)
        # print("-"*50)  
         
        if dst_comp.device != "cpu":
            print("-"*12, "set_interprocess_queues starts", "-"*13)
            dst_queue_dict = {**dst_comp.input_queues, **dst_comp.state_queues}
            dst_queue = dst_queue_dict.get(dst_q)            
            print(f"dst_comp {dst_comp.name}, dst_queue.name:{dst_queue.name}, dst_queue.queue_type:{dst_queue.queue_type}")
            dst_comp.set_interprocess_queues(dst_queue.name, dst_queue.shape, dst_queue.queue_type)            
            print("-"*12, "set_interprocess_queues ends", "-"*13)   
        
        if src_comp.device != "cpu":
            print("-"*12, "set_interprocess_queues starts", "-"*13)
            src_queue_dict = {**src_comp.output_queues, **src_comp.state_queues}
            src_queue = src_queue_dict.get(src_q)
            print(f"src_comp {src_comp.name}, src_queue.name:{src_queue.name}, src_queue.queue_type:{src_queue.queue_type}")
            src_comp.set_interprocess_queues(src_queue.name, src_queue.shape, src_queue.queue_type)
            print("-"*12, "set_interprocess_queues ends", "-"*13)   

        # print("-"*12, "after ipc queue handling", "-"*13)
        # pp.pprint(src_comp.name)
        # pp.pprint(src_comp.__dict__)
        # pp.pprint(dst_comp.name)
        # pp.pprint(dst_comp.__dict__)
        # print("-"*50)

    
    def add_flow(self, src_q, src_comp, dst_q, dst_comp):
        assert src_comp != dst_comp
        assert src_comp in self.components and dst_comp in self.components
        assert src_q in src_comp.write_queues, f"{src_q} not a writeable queue in component {src_comp.name}"
        assert dst_q in dst_comp.read_queues, f"{dst_q} not a readable queue in component {dst_comp.name}"
		## the name needs to be the same, so the flow can be connected
        assert src_q == dst_q 

        if self.using_only_threads:
            self.convert_queues(src_q, src_comp, dst_q, dst_comp)
            
        ## (src_q, src_name) -> [(dst1_q, dst1_name), (dst2_q, dst2_name), ...]
        ## the value is a list so we can handle a branch, e.g. src->dst1, src->dst2  
        if self._edges.get((src_q, src_comp.name)) == None:
            self._edges[(src_q, src_comp.name)] = []
        self._edges[(src_q, src_comp.name)].append((dst_q, dst_comp.name))
