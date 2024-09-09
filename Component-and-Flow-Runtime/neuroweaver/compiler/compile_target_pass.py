"""Compilation pass to generate target for each component.
"""
import argparse

from qfdfg_pb2 import Component, Flow, Graph
from util import write_to, read_protobuf
from dnnweaver_compiler import DnnweaverCompiler


engine_compiler_table = {
    'dnnweaver': DnnweaverCompiler()
}


def main(args):
    graph = Graph()
    read_protobuf(args.qfdfg, graph)

    # Iterate through QF-DFG. For each target engine, call the respective compiler.
    for component in graph.components:
        #print(component.engine_name)
        if component.engine_name in engine_compiler_table:
            engine_compiler = engine_compiler_table[component.engine_name]
            inst_array = engine_compiler.compile(component.name)
            #print(inst_array)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='Compile pass to generate target for each component.')
    argparser.add_argument('qfdfg',
                           help='Queued Fractalized Dataflow Graph (.pb)')
    argparser.add_argument('-o', '--output_file',
                           default='qfdfg.pb',
                           help='Updated QF-DFG with Python target generated for each component. Default: qfdfg.pb')
    argparser.add_argument('-t', '--target',
                           default='Python',
                           help='Default target (Python)')
    args = argparser.parse_args()

    main(args)
