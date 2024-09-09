import os
import re
import ast
import importlib
import inspect
from collections import deque
import argparse
from ast import parse, Call, walk, FunctionDef

from qfdfg.qfdfg_pb2 import Component, Flow, Graph
from qfdfg.util import write_to, read_protobuf
from esa.esa_pb2 import EngineOrg
from compiler.parser import EngineSystemUtil

from definitions import ENGINE_SET_PBFILE, QFDFG_PBFILE


class EngineSelector(object):
    def __init__(self, qfdfg, engine_set, verbose=False):
        self.qfdfg = qfdfg
        self.engine_set = engine_set
        self.verbose = verbose

    def select_default_engines(self):
        if self.verbose:
            print("Default engine selection")
        for component in self.qfdfg.components:
            if component.domain_name == '':
                component.engine_name = 'default'
                if self.verbose:
                    print(f'Set default engine to {component.name} component')
            else:
                pass

    def greedy_selection(self):
        '''This should run after default engine selection has been run.'''
        if self.verbose:
            print("Greedy selection")
        for component in self.qfdfg.components:
            if component.engine_name != 'default':
                if self.verbose:

                    print(f"For node: {component.name}")
                engines = self.engine_set.get_engines_by_domain_capability(component.domain_name, component.name)
                if self.verbose:
                    print(engines)
                min_cost_engine = engines[0]
                min_cost = self.engine_set.get_capability_info(min_cost_engine, component.name).impl.runtime_cost
                for engine in engines:
                    capability_info = self.engine_set.get_capability_info(engine, component.name)
                    runtime_cost = capability_info.impl.runtime_cost
                    if runtime_cost < min_cost:
                        min_cost = runtime_cost
                        min_cost_engine = engine
                if self.verbose:
                    print(f"Engine selected: {min_cost_engine.name}")
                    print(f"Engine cost: {min_cost}")
                component.engine_name = min_cost_engine.name
        # for node_id in nx.topological_sort(graph):
        #     node = nodes[node_id]
        #     for engine in self.engine_set:
        #         if engine.capability == node.capability:
        #             node.engine = engine

    def node_fusion(self):
        if self.verbose:
            print("Node fusion")
        self.fusion_time = 0
        start = time()

        fused_graph = graph

        while self._can_be_fused(fused_graph):
            edge = list(fused_graph.edges())[0]
            node_from = nodes[edge[0]]
            node_to = nodes[edge[1]]
            # print(edge[0], edge[1])
            #if node_from.engine == node_to.engine:
            fused_graph = nx.contracted_nodes(fused_graph, edge[0], edge[1], self_loops=False)
            if node_from.engine is not None and node_to.engine is not None:
                node_from.engine.comp_time += node_to.engine.comp_time
            elif node_from.engine is not None and node_to.engine is None:
                node_from.engine.comp_time += node_to.time
            elif node_from.engine is None and node_to.engine is not None:
                node_from.time += node_to.engine.comp_time
            else:
                node_from.engine.comp_time += node_to.time
            # print('Engine to node assignment after fusing:')
            # for node in fused_graph.nodes():
            #     print('node {}, engine {}'.format(nodes[node].id, nodes[node].engine.id))

    def _can_be_fused(self, graph):
        for edge in graph.edges():
            node_from = nodes[edge[0]]
            node_to = nodes[edge[1]]
            if node_from.engine is not None and node_to.engine is not None:
                if node_from.engine == node_to.engine:
                    #print('nodes {} and {} can be fused!'.format(edge[0], edge[1]))
                    return True
        return False

    def dp_selection(self):
        if self.verbose:
            print("Dynamic Programming selection")
        cost = {}
        # Initialize engine assignment to each node
        # for node in graph.nodes():
        #     nodes[node].engine = self.engine_set.get_min_compute_engine()
        for node_id in nx.topological_sort(graph):
            node = nodes[node_id]
            for engine in self.engine_set:
                if engine.capability == node.capability:
                    node.engine = engine
        for node in nx.topological_sort(graph):
            cost[node] = math.inf
            for engine in self.engine_set:
                compute_time = engine.comp_time
                new_cost = compute_time
                for pred in graph.predecessors(node):
                    new_cost += \
                        self.engine_set.get_comm_cost(nodes[pred].engine, engine) + \
                        self.engine_set.get_trans_cost(nodes[pred].engine, engine)
                        #cost[pred]
                if new_cost < cost[node]:
                    cost[node] = new_cost
                    nodes[node].engine = engine

def select_engine(qfdfg, engine_system=ENGINE_SET_PBFILE, output_file=QFDFG_PBFILE, verbose=False):
    graph = Graph()
    read_protobuf(qfdfg, graph)

    engine_set = EngineSystemUtil(engine_system)
    engine_selector = EngineSelector(graph, engine_set, verbose=verbose)

    engine_selector.select_default_engines()
    engine_selector.greedy_selection()
    write_to(output_file, engine_selector.qfdfg)
    return output_file

def main(args):
    graph = Graph()
    read_protobuf(args.qfdfg, graph)

    engine_set = EngineSystemUtil(args.engine_system)
    engine_selector = EngineSelector(graph, engine_set)

    engine_selector.select_default_engines()
    engine_selector.greedy_selection()
    write_to(args.output_file, engine_selector.qfdfg)

    #print(engine_selector.qfdfg)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Engine Selector')
    argparser.add_argument('qfdfg',
                           help='Input QF-DFG. Default: qfdfg.pb')
    argparser.add_argument('-e', '--engine_system',
                           default=ENGINE_SET_PBFILE,
                           help='Engine system file (.pb). Default: esa/engine_system.pb')
    argparser.add_argument('-o', '--output_file',
                           default=QFDFG_PBFILE,
                           help='Updated QF-DFG with engines selected. Default: qfdfg.pb')
    args = argparser.parse_args()

    main(args)
