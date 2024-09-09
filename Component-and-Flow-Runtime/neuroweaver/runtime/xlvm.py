"""XLVM Runtime
"""
import threading
import logging
import os
import argparse
import time
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

from qfdfg.util import write_to, read_protobuf
from qfdfg.qfdfg_pb2 import Component, Flow, Graph
from runtime.task_manager import TaskManager
from runtime.engine_manager import EngineManager

from definitions import ENGINE_SET_PBFILE


class XLVM(object):

    def __init__(self, qfdfg, engine_set, qfdfg_pb=None, verbose=False):
        self.task_manager = TaskManager(qfdfg)
        self.engine_manager = EngineManager(engine_set)
        self.verbose = verbose
        self.qfdfg_pb = qfdfg_pb
        
        # Data structure to lookup queues between Components
        self.queue_table = {}
        self.init_queue_table()

        # Data structure for producer consumer channels for streaming between Components
        self.channel_table = {}
        self.init_channel_table()

        # Data structure to lookup states for each Component
        self.state_table = {}
        self.init_state_table()

        # Keep track of task execution counts
        self.task_iter_counts = {}
        for comp in self.task_manager.qfdfg.components:
            self.task_iter_counts[comp.name] = 0

        self.task_manager.start()
        self.engine_manager.start()

        self.logname = "[XLVM] "
        self.thread_pool_size = 8

        self.global_variables = {}
        self.producer_consumer_table = {}
        self.engine_name_map = {'default'    : 'DefaultEngine',
                                'tensorflow' : 'TensorflowEngine',
                                'cuda'       : 'CUDAEngine',
                                'sklearn'    : 'SklearnEngine',
                                'numpy'      : 'NumpyEngine',
                                'dnnweaver'  : 'DnnweaverEngine',
                                'tabla'      : 'TablaEngine',
                                'genesys'    : 'GenesysEngine'}

    def init_channel_table(self):
        for component in self.task_manager.qfdfg.components:
            if component.engine_name == 'default':
                for channel in component.channels:
                    if channel not in self.channel_table:
                        self.channel_table[channel] = Queue()

    def init_queue_table(self):
        for comp in self.task_manager.qfdfg.components:
            for dest_comp_name in comp.outputs:
                flowlist = comp.outputs[dest_comp_name].flows
                for flow in flowlist:
                    #self.queue_table[comp.name, dest_comp_name, flow.info.fid] = Queue()
                    self.queue_table[flow.info.fid] = Queue()

    def init_state_table(self):
        for comp in self.task_manager.qfdfg.components:
            self.state_table[comp.name] = Queue()

    def store(self, src_component, dst_component, flow, data):
        '''Store data being sent from source to destination component.'''
        #queue_map = self.queue_table[src_component.name, dst_component.name]
        if data is None:
            return
        flow_id = flow.info.fid
        # print('store() from {} to {} with Flow {}: value = {}'.format(src_component.name,
        #                                                               dst_component.name,
        #                                                               flow_id,
        #                                                               data))
        #queue = self.queue_table[src_component.name, dst_component.name, flow_id]
        queue = self.queue_table[flow_id]

        # self.queue_table_lock.acquire()
        # if flow_id in queue_map:
        #     queue = queue_map[flow_id]
        # else:
        #     queue = Queue()
        #     queue_map[flow_id] = queue
        # self.queue_table_lock.release()
        begin = time.time()
        queue.put(data)
        if self.verbose:
            print(f'debug: STORE {src_component.name} -> {dst_component.name}, {list(queue.queue)}, queue id: {id(queue)}')
        end = time.time()
        #print((end - begin) * 1000)

    def load(self, src_component, dst_component, flow):
        '''Load data being sent from source component and returns the data.'''
        #queue_map = self.queue_table[src_component.name, dst_component.name]
        flow_id = flow.info.fid
        #queue = self.queue_table[src_component.name, dst_component.name, flow_id]
        queue = self.queue_table[flow_id]

        # # TODO quick fix: busy waiting
        # while True:
        #     self.queue_table_lock.acquire()
        #     if flow_id in queue_map:
        #         self.queue_table_lock.release()
        #         break
        #     self.queue_table_lock.release()

        #queue = queue_map[flow_id]
        begin = time.time()
        data = queue.get()
        #print('load() from {} to {}: value = {}'.format(src_component.name, dst_component.name, data))
        if self.verbose:
            print(f'debug: LOAD {src_component.name} -> {dst_component.name}, {list(queue.queue)}, queue id: {id(queue)}, data: {data}')
        end = time.time()
        #print((end - begin) * 1000)
        return data

    def store_state(self, component, data):
        queue = self.state_table[component.name]
        queue.put(data)

    def load_state(self, parent_component, component, flow):
        '''Load state data for given component.'''
        if self.task_iter_counts[component.name] == 0:
            data = self.load(parent_component, component, flow)
        else:
            queue = self.state_table[component.name]
            data = queue.get()
        if self.verbose:
            print('Load State aquired data!')
        return data

    def read_inputs(self, component):
        #print('read_inputs from {}'.format(component.name))
        input_data = []
        for var in component.input_names:
            for parent_comp_name in component.inputs:

                parent_comp = self.get_component_by_name(parent_comp_name)
                if not parent_comp:
                    raise Exception('Component {} not found.'.format(parent_comp_name))
                in_flows = component.inputs[parent_comp_name].flows
                for flow in in_flows:
                    # if flow is state:
                    #     continue
                    if flow.info.var_name == var:
                        if var in component.state_args:
                            data = self.load_state(parent_comp, component, flow)
                        else:
                            data = self.load(parent_comp, component, flow)
                        input_data.append(data)
        return input_data

    def write_outputs(self, component, outdata):
        # TODO quick fix
        #i = 0
        for i, var in enumerate(component.output_names):
            for dest_comp_name in component.outputs:
                #print('dest comp name: ' + dest_comp_name)
                dest_comp = self.get_component_by_name(dest_comp_name)
                if not dest_comp:
                    raise Exception('Component {} not found.'.format(dest_comp_name))
                flowlist = component.outputs[dest_comp_name].flows
                for flow in flowlist:
                    #print('flow: ')
                    #print(flow)
                    if flow.info.var_name == var:
                        #print('FLAG')
                        #print(component.name)
                        data = outdata[i]
                        #print(data)
                        self.store(component, dest_comp, flow, data)
                    #i += 1
        # for dst, data in zip(dst_names, outdata):
        #     print(dst, type(data))
        #     dst_component = self.get_component_by_name(dst)
        #     if not dst_component:
        #         raise Exception('Component {} not found.'.format(name))
        #     self.send(component, dst_component, data)

    def get_component_by_name(self, name):
        for comp in self.task_manager.qfdfg.components:
            if comp.name == name:
                return comp
        return None

    def _run(self, task, iter_count=None, infinite=False):
        if self.verbose:
            print(self.logname + f" Executing _run for {task.name} with engine {task.engine_name}")
        #while self.task_manager.has_tasks_left():
            #task = self.task_manager.dequeue_task()
        engine_name = task.engine_name
        channel_queues = {}
        for x in task.channels:
            channel_queues[x] = self.channel_table[x]
        if self.engine_manager.engine_available(engine_name):
            if engine_name == 'default':
                engine = self.engine_manager.open(engine_name, 'DefaultEngine', task.name, self.qfdfg_pb)
            else:
                engine = self.engine_manager.open(engine_name, self.engine_name_map[engine_name], task.name)
        else:
            raise Exception(f'Engine {engine_name} is unavailable!')
        # Set task iter_count if provided at runtime for application
        if iter_count is not None:
            task.iter_count = iter_count
        count = 0
        print("Will run task now")
        while count < task.iter_count:
            if self.verbose:
                print(f"Task: {task.name}, Engine: {engine_name}, iter count: {count}\n")
            input_data = self.read_inputs(task)
            #print(self.logname)
            #print(f"Input data = {input_data}\n")
            #print("length of input data = " + str(len(input_data)))
            self.engine_manager.write(engine, input_data)
            metadata = {'outputs': task.outputs,
                        'output_vals': task.output_vals,
                        'obj_filename': task.obj_filename,
                        'channel_queues': channel_queues}

            self.engine_manager.compute(engine, task.name, metadata)
            data = self.engine_manager.read(engine)
            if self.verbose:
                print(f"Output data = {data}")
            self.write_outputs(task, data)
            self.task_iter_counts[task.name] += 1
            if self.verbose:
                print(f"Task {task.name} iter count {count} complete!")
                print("*" * 64)
            if not infinite:
                count += 1
        return task.name

    def handle_sync_primitives(self):
        # for all components, query the respective engines to find what
        # shared resources each component produces
        for component in self.task_manager.qfdfg.components:
            component_engine_impl = self.engine_name_map[component.engine_name]
            engine = self.engine_manager.open(component.engine_name, component_engine_impl , component.name, self.qfdfg_pb)

    def run(self, iter_count=None, run_tasks_infinitly=False):
        futures = []
        with ThreadPoolExecutor(max_workers=self.thread_pool_size) as executor:
            for task in self.task_manager.ready_queue.queue:
                future = executor.submit(self._run, task, iter_count, run_tasks_infinitly)
                futures.append(future)
            for future in concurrent.futures.as_completed(futures):
                data = future.result()
                if self.verbose:
                    print(f'Task {data} done')
        if self.verbose:
            print("All tasks complete!")


def run_project(qfdfg, engine_set=ENGINE_SET_PBFILE, iter_count=None, run_tasks_infinitely=False, verbose=False):
    graph = Graph()
    read_protobuf(qfdfg, graph)

    xlvm = XLVM(graph, engine_set, qfdfg_pb=qfdfg, verbose=verbose)
    #xlvm.handle_sync_primitives()
    xlvm.run(iter_count, run_tasks_infinitely)



def main(args):
    graph = Graph()
    read_protobuf(args.qfdfg, graph)

    xlvm = XLVM(graph, args.engine_set)
    xlvm.run()


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='''XLVM Runtime.
        Executes QF-DFG and manages data communication among components.''')
    argparser.add_argument('qfdfg',
                           help='Queued Fractalized Dataflow Graph (.pb).')
    argparser.add_argument('-e', '--engine_set',
                           default=ENGINE_SET_PBFILE,
                           help='Engine system file (.pb). Default: esa/engine_system.pb')
    args = argparser.parse_args()

    main(args)
