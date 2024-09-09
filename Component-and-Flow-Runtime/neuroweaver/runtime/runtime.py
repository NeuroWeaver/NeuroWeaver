from qfdfg.graph import Graph
from qfdfg.component import Component
from qfdfg.component import ComponentStatus
from typing import List, Any
from qfdfg.flow import Flow, FlowQueue
import numpy as np
import multiprocessing as mp
import queue
import copy
from collections import deque
import logging
import concurrent.futures

# logging.basicConfig(format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#     level=logging.INFO) 

class Runtime(object):
    def __init__(self, graph: Graph, verbose:bool =False):
        self._iterations = 1
        self._ready_queue = deque()
        self._graph = graph
        self._force_state_update = True
        self._use_futures = True
        if self._use_futures:
            self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
            self._futures = []
            self._future_to_component_map = {}

        logging.basicConfig(format='%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            level=logging.DEBUG)         

    def __del__(self):
        if self._use_futures:
            self._executor.shutdown()

    @property
    def iterations(self) -> int:
        return self._iterations
    
    @iterations.setter
    def iterations(self, iter:int):
        if iter > 0:
            self._iterations = iter
    ## dealing with outgoing edges
    ## o: output queues, i: input queues, s: state quues            
    ## o->i and o->s cases are handled in output_queues_handler()
    ## state queues cases s->s and s->i are handled in state_queues_handler()
    
    ## o->i edges are "required" for the connected components
    ## edges from state queues are considered if state queues are ready
    ## s->s edges is the trivial example for state sharing
    ## s->i, o->s edges are to deal with state transformation
    
    def state_queues_handler(self, comp: Component):
        logger = logging.getLogger(__name__) 
        for state_name in comp.state_queues:
            logger.info(f"state_queue {state_name}!")
            src_queue = comp.state_queues.get(state_name)
            if src_queue is None:
                logger.error(f"cannot find queue named {src_queue.name} component:{comp.name}")
            assert src_queue is not None
                                
            ## treat state queues as non-optional
            if self._force_state_update == True:
                #logger.debug(f"output_q_name {src_queue.name}, comp.name {comp.name}")
                dst_q_list = self._graph.edges.get((src_queue.name, comp.name))
                #logger.debug(f"dst_q_list: {dst_q_list}")
                if dst_q_list is None:
                    continue
                self.ready_queue_push(dst_q_list)
                #logger.debug(f"src_comp: {comp} src_q:{src_queue}")
                self.dataflow(src_queue, dst_q_list)             
            else: ## [UNTESTED]: the actual implemenation of considering state queues as optional
                if src_queue.empty() == False:
                    logger.info(f"src_queue.empty():{src_queue.empty()}")
                    logger.info(f"output_q_name {src_queue.name}, comp.name {comp.name}")
                    dst_q_list = self._graph.edges.get((src_queue.name, comp.name))
                    logger.info(f"dst_q_list: {dst_q_list}")
                    if dst_q_list is None:
                        continue
                    self.ready_queue_push(dst_q_list)
                    logger.info(f"src_comp: {comp} src_q:{src_queue}")
                    self.dataflow(src_queue, dst_q_list) 
                ## if src_queue here i.e. state_queues, are empty then we do nothing!
                else:
                    logger.info(f"src_queue_empty, comp.name {comp.name}") 
                    continue
    
    def output_queues_handler(self, comp: Component):
        logger = logging.getLogger(__name__) 
        # print(f"comp.name {comp.name}")
        for output_name in comp.output_queues:
            #output_state_queues = {**comp.output_queues, **comp.state_queues}
            src_queue = comp.output_queues.get(output_name)
            if src_queue is None:
                logger.error(f"cannot find queue named {src_queue.name} component:{comp.name}")
            assert src_queue is not None
            
            src_q_name = src_queue.name
            logger.debug(f"output_q_name {src_q_name}, comp.name {comp.name}")
            ## check outgoing graph edge from this particular output queue 
            dst_q_list = self._graph.edges.get((src_q_name, comp.name))
            logger.debug(f"dst_q_list: {dst_q_list}")
            if dst_q_list is None:
                continue

            ## deal with edges for BFS, not the queue push/pop yet  
            self.ready_queue_push(dst_q_list)
            
            ## drain the output queue, i.e. src queue, from the current component
            ## push all items to its connected dst queues which can be state queues
            ## or input queues. 
            logger.debug(f"src_comp: {comp} src_q:{src_queue}")
            logger.debug(f"src_q_name:{src_q_name}.empty():{src_queue.empty()}")
            ## TODO: we may need to gate output for a certain size vector output
            self.dataflow(src_queue, dst_q_list)
        
    ## ready_queue_push(): add edgesfor BFS, make sure each connected component is visited once
    ## dataflow(): drain the output queues and fill the input queues
    ## We want to consider state queues as optional which means they may not be ready 
    ## eveytime BFS comes to it.
    
    ## drain the output queue, i.e. src queue, from the current component
    ## push all items to its connected dst queues which can be state queues
    ## or input queues.
    def dataflow(self, src_queue, dst_q_list):
        logger = logging.getLogger(__name__)   
        element = src_queue.pop() # queue.put() is blocking
        while element is not None:                    
            # logger.debug(f"after while-loop -> src_q_name:{src_q_name}.empty():{src_queue.empty()}")
            # logger.debug(f"after while-loop -> src_q_name:{src_q_name}.qsize():{src_queue.qsize()}")
            # logger.debug(f"elemment {element} from src_comp: {comp} src_q:{src_queue}")

            for dst_q_name, dst_comp_name in dst_q_list:
                dst_comp = self._graph.get_component_byname(dst_comp_name)
                ## dst_comp.input_queues and dst_comp.state_queues both need to be considered
                input_state_queues = {**dst_comp.input_queues, **dst_comp.state_queues}
                dst_queue = input_state_queues.get(dst_q_name)
                # if dst_queue_type == "input":
                #     dst_queue = dst_comp.input_queues.get(dst_q_name)
                # elif dst_queue_type == "state":
                #     dst_queue = dst_comp.state_queues.get(dst_q_name)
                # else:                    
                #     logger.debug("dst_queue is none, incorrect queue type")
                #     continue

                if dst_queue is None:
                    logger.error(f"cannot find queue named {dst_q_name} component:{dst_comp.name}")
                assert dst_queue is not None					
                src_shape = src_queue.shape
                ## do deepcopy to handle branches on dataflow
                element_copy = copy.deepcopy(element)
                dst_queue.push(element_copy, src_shape)
                logger.debug(f"input_queue {dst_q_name} size {dst_queue.qsize()} of component {dst_comp_name}")
            
            if src_queue.empty() == True:
                break

            element = src_queue.pop()        
    
    ## deal with edges for BFS, not the queue push/pop
    def ready_queue_push(self, dst_q_list):
        logger = logging.getLogger(__name__)  
        for _ , dst_comp_name in dst_q_list:
            logger.debug(f"component from dst_q_list:{dst_comp_name}")
            dst_comp = self._graph.get_component_byname(dst_comp_name)
            logger.debug(f"dst_comp.status:{dst_comp.component_status}")
            if dst_comp.component_status == ComponentStatus.initialized or \
                dst_comp.component_status == ComponentStatus.running:

                dst_comp.component_status = ComponentStatus.running
				# avoid adding the same component to the _ready_queue multiple times 
                if dst_comp not in self._ready_queue:
                    self._ready_queue.append(dst_comp)
                else:
                    logger.debug("-------- comp existed --------")
                logger.debug(f"pushed component:{dst_comp.name}")
                logger.debug(f"queue len after push:{len(self._ready_queue)}")
            else:
                logger.info("An edge to executed or running component")    		
    
    def execute(self):
        for iter in range(self.iterations):
            self.execute_loop()
            self._ready_queue.clear()
            logger = logging.getLogger(__name__)
            for comp in self._graph.components:
                comp._component_status = ComponentStatus.running
            logger.debug("*" * 25)
    ## if components need to run on another process launch here
    ## and point comp.execute() to the process
    ## comp_process = mp.Process(target=comp.execute(), args=(*args_tuple))
    ## comp_process.start() will be called when its upstream component is done.
    ## comp_process joins after the "while len(self._ready_queue) > 0" loop ends
    def execute_loop(self):
        logger = logging.getLogger(__name__)   
        # seq exec, no branch only a single line
        # We need a BFS here! for component traversal 
        ## BFS's visited == Status.running | Status.paused, as the component is added to _ready_queue 
        ## BFS's !visited == Status.initialized
        ## after a BFS, we re-mark all components as Status.initilized
        ## after the component popped from _ready_queue and execute(*args)
        ## if the source component is completed then we mark components as Status.completed 
        ## rather than Status.paused after Status.running
        
        ## single pass of the graph using BFS
        self._graph.components[0]._component_status = ComponentStatus.running
        # enqueue the first component without thinking
        self._ready_queue.append(self._graph.components[0])
        ## append=push and popleft=pop
        
        ## Runtime with BFS more than once:
        ## The current runtime only visit the whole dataflow graph once
        ## If the input component provides n elements of input, then we either 
        ## 1. batch n elements together optionally 
        ## 2. visit the dataflow graph n times for each element
        ## we assume n is a number can be known before the execution
        ## -> the second option seem to be the correct one

        while len(self._ready_queue) > 0 :
            comp = self._ready_queue.popleft()
            logger.debug(f"comp popped from queue:{comp.name}")
            logger.debug(f"queue len:{len(self._ready_queue)}")
            # print(type(comp))
            # print(len(comp.exec_arg_names))

            ## feed arguments into execute func
            ## the order of (input0, input1, 
            ## ..., state0, state1, ..., output0, output1) is strict
            if len(comp.exec_arg_names) > 0:
                args_tuple = ()
                for input_name in comp.input_names:
                    input_q = comp.input_queues[input_name]
                    logger.debug(f"input_queue name: {input_q.name}")
                    args_tuple = (*args_tuple, input_q)

                for state_name in comp.state_names:
                    state_q = comp.state_queues[state_name]
                    logger.debug(f"state_queue name: {state_q.name}")
                    args_tuple = (*args_tuple, state_q)
                
                for output_name in comp.output_names:
                    output_q = comp.output_queues[output_name]
                    logger.debug(f"output_queue name: {output_q.name}")
                    args_tuple = (*args_tuple, output_q)
              
                if comp.device == "cpu":
                    # FEATURE: iterations aka batching within a component 
                    ## 1: for comp without inputs, use iterations for termination  
                    ## 2: wrap a while loop to make sure the input queue is drained
                    
                    # if len(comp.input_names) == 0:
                    #     assert comp._iterations > 0
                    #     for iter in range(comp._iterations):
                    #         print(f"iter:{iter}")
                    #         comp.execute(*args_tuple)
                    # else:
                    #     for input_name in comp.input_names:
                    #         input_q = comp.input_queues[input_name]
                    #         input_data_still = True
                    #         input_data_still = input_data_still & ~input_q.empty()
                    #         logger.debug(f"before while loop:{input_data_still}")
                    #     while input_data_still:
                    #         comp.execute(*args_tuple)
                    #         for input_name in comp.input_names:
                    #             input_q = comp.input_queues[input_name]
                    #             input_data_still = input_data_still & ~input_q.empty()  
                    #         logger.debug(f"{input_data_still}")  

                    # if self._sequential_execution == False: 
                    if self._use_futures:
                        future = self._executor.submit(comp.execute, *args_tuple)
                        self._futures.append(future)
                        self._future_to_component_map[future] = comp
                    else: 
                        comp.execute(*args_tuple)

                # GPU or FPGA cases here, each should run as a process
                else: 
                    ## TODO: the start() should only be called once
                    ## TODO: A Trigger, which controlled bt this runtime process, to comp.execute() on another process
                    ## trigger needs to be a shared memory variable
                    ## Replace comp.execute with comp.execute_loop with args=(input_q, state_q, output_q, trigger_variable), e.g.                    
                    # def execute_loop(self, input_q, state_q, output_q, trigger):
                    #    while trigger == True:
                    #        input_q.pop() # a blocking pop() on flowqueue input_q
                    #        # do something, the reak work here

                    comp_process = mp.Process(target=comp.execute, args=(input_q, state_q, output_q))
                    comp_process.start()
                    comp._process_handle = comp_process
            else:
                comp.execute() ## stingw: do we really have a case like this?

            if self._use_futures:
                for f in concurrent.futures.as_completed(self._futures):
                    if f.done() == True:
                       comp_by_future = self._future_to_component_map.get(f)
                       logger.info(f"comp_by_future {comp_by_future.name}") 
                       self.output_queues_handler(comp_by_future)
                       self.state_queues_handler(comp_by_future)
                       comp_by_future.component_status = ComponentStatus.paused
                       self._futures.remove(f)

            else:
                comp.component_status = ComponentStatus.paused
                self.output_queues_handler(comp)
                self.state_queues_handler(comp)

        # join other processes launched by us
        for comp in self._graph.components:
            if comp._process_handle is not None:                
                comp._process_handle.join()
                logger.debug(f"comp {comp.name} joined")

    def initialize(self):
        for comp in self._graph.components:
            #print(type(comp))
            #print(comp.component_status)
            #print(len(comp.init_arg_names))            

            ## the order of (state0, state1, ..., param0, param1) is strict
            if len(comp.init_arg_names) > 0:
                args_tuple = ()
                for state_name in comp.state_names:
                    state_q = comp.state_queues[state_name]                    
                    #print(f"state_queue name: {state_q.name}")
                    args_tuple = (*args_tuple, state_q)
                for _, param in comp._parameters.items():
                    args_tuple = (*args_tuple, param)
                comp.initialize(*args_tuple)                
            else:
                comp.initialize()
            comp._component_status = ComponentStatus.initialized                     


