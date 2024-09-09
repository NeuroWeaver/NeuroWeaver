from testing_components import Brain_posix_mq, SignalToStimulation_posix_mq, SingalSink_posix_mq, StimulationSink
from testing_components import AllQueueTypesSink, AllQueueTypesSource
import multiprocessing as mp
import posix_ipc
import pickle, os
import numpy as np
from time import sleep
import logging
from qfdfg.graph import Graph
from collections import deque
from qfdfg.component import Component, ComponentStatus
from runtime.process_runtime import PPRuntime

# logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#     level=logging.INFO)

def run_split():
    print("run_split")

def run_closed_loop():
    print("run_closed_loop")

def run_all_types_edges():
    two_comp_graph = Graph("two_component_test_all_types_edges")
    o2i_queue = "output2input"
    o2s_queue = "output2state"
    s2s_queue = "state2state"
    s2i_queue = "state2input"

    source = AllQueueTypesSource()
    source.set_output(o2i_queue, (2,3), is_process_parallel=True)
    source.set_output(o2s_queue, (2,3), is_process_parallel=True)
    source.set_state(s2s_queue, (2,3), is_process_parallel=True)
    source.set_state(s2i_queue, (2,3), is_process_parallel=True)

    sink = AllQueueTypesSink()
    sink.set_input(o2i_queue,(2,3), is_process_parallel=True)
    sink.set_input(s2i_queue,(2,3), is_process_parallel=True)
    sink.set_state(s2s_queue,(2,3), is_process_parallel=True)
    sink.set_state(o2s_queue,(2,3), is_process_parallel=True)

    two_comp_graph.add_component(source)
    two_comp_graph.add_component(sink)

    two_comp_graph.add_flow("output2input", source ,"output2input", sink)
    two_comp_graph.add_flow("output2state", source ,"output2state", sink)
    two_comp_graph.add_flow("state2state", source ,"state2state", sink)
    two_comp_graph.add_flow("state2input", source ,"state2input", sink)

    runtime = PPRuntime(two_comp_graph)
    runtime._iterations = 128
    runtime.initialize()
    runtime.execute()
    

def run_three_comp():
    three_comp_graph = Graph("three_component_graph_using_process")
    brain = Brain_posix_mq()
    signal_queue = "brain_signal"
    stimu_queue = "stimulation"

    brain.set_output(signal_queue, (2,3), is_process_parallel=True)
    
    singal2stimu = SignalToStimulation_posix_mq()
    singal2stimu.set_input(signal_queue, (2,3), is_process_parallel=True)
    singal2stimu.set_output(stimu_queue, (2,3), is_process_parallel=True)
    #singal2stimu.set_state("component_state", (1,), is_process_parallel=True)

    sink = StimulationSink()
    sink.set_input(stimu_queue, (2,3), is_process_parallel=True)     

    three_comp_graph.add_component(brain)
    three_comp_graph.add_component(singal2stimu)
    three_comp_graph.add_component(sink)

    ## add_flow here but we don't create the queues yet
    three_comp_graph.add_flow(signal_queue, brain, signal_queue, singal2stimu)
    three_comp_graph.add_flow(stimu_queue, singal2stimu, stimu_queue, sink)

    runtime = PPRuntime(three_comp_graph)
    runtime._iterations = 128
    runtime.initialize() ## visit the graph and create all the posix msq_queues 
    runtime.execute()

def run_two_comp():
    two_comp_graph = Graph("two_component_graph_using_process")

    brain = Brain_posix_mq()
    brain_q_name = "brain_signal"
    brain.set_output(brain_q_name, (2,3), is_process_parallel=True)
    sink_q_name = brain_q_name # this implies the edge 
    sink = SingalSink_posix_mq()
    sink.set_input(sink_q_name, (2,3), is_process_parallel=True)     
    #logger.debug(sink.__dict__)

    two_comp_graph.add_component(brain)
    two_comp_graph.add_component(sink)

    ## add_flow here but we don't create the queues yet
    two_comp_graph.add_flow(brain_q_name, brain, sink_q_name, sink)

    runtime = PPRuntime(two_comp_graph)
    runtime._iterations = 128
    runtime.initialize() ## visit the graph and create all the posix msq_queues 
    runtime.execute()

logger = logging.getLogger(__name__)
#run_two_comp()
#run_three_comp()
run_all_types_edges()
