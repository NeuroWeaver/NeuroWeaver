"""XLVM Task Manager
"""
import threading
import logging
import os
import argparse
import time
from queue import PriorityQueue, Queue

from qfdfg.util import write_to, read_protobuf
from qfdfg.qfdfg_pb2 import Component, Flow, Graph


class TaskManager(object):
    def __init__(self, qfdfg, verbose=False):
        """Initializes Task Manager with the given QF-DFG.
        """
        self.qfdfg = qfdfg
        #self.ready_queue = PriorityQueue()
        self.ready_queue = Queue()
        self.running_list = []
        self.verbose = verbose
        self.logname = "[Task Manager] "

    def start(self):
        if self.verbose:
            print("Starting Task Manager")
        self.reverse_topological_sort()
        for component in self.qfdfg.components:
            if self.is_task_ready(component):
                if self.verbose:
                    print(component.name + ' is ready!')
                if len(component.sub_components) == 0:
                   self.enqueue_task(component)
                # self.enqueue_task(component)

        # for component in self.qfdfg.component_defs:
        #     if component.name == 'linear_regression':
        #         self.enqueue_task(component)
        if self.verbose:
            self.print_ready_queue()

    def is_task_ready(self, task) -> bool:
        if self.inputs_ready(task):
            return True

    def inputs_ready(self, task) -> bool:
        """Returns True if all inputs are ready."""
        return True

    def outputs_written(self, task) -> bool:
        """Returns True if all outputs have been written."""
        return True

    def has_tasks_left(self) -> bool:
        return not self.ready_queue.empty()

    def enqueue_task(self, task):
        self.ready_queue.put(task)

    def dequeue_task(self):
        return self.ready_queue.get()

    def reverse_topological_sort(self):
        pass

    def print_ready_queue(self):

        print(self.logname)
        print('Ready Queue:')
        for task in list(self.ready_queue.queue):
            print(task.name)
        print()

    def print_running_tasks(self):
        print(self.running_list)

    def detect_failure(self):
        pass

    def recover(self):
        pass

    def detect_deadlock(self):
        pass


def main(args):
    graph = Graph()
    read_protobuf(args.qfdfg, graph)
    task_manager = TaskManager(graph)
    task_manager.start()


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='''XLVM TaskManager.
        Task Manager for XLVM Runtime.''')
    argparser.add_argument('qfdfg',
                           help='Queued Fractalized Dataflow Graph (.pb)')
    args = argparser.parse_args()

    main(args)
