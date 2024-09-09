import sys
# sys.path.insert(0, '/Users/joon/neuroweaver/qfdfg')
# sys.path.insert(0, '/Users/joon/neuroweaver/compiler')
# sys.path.insert(0, '/Users/joon/neuroweaver/esa')
import threading
import logging
import os
import argparse
import time
from queue import Queue

from esa import NEUROWEAVER_PATH
import compiler.parser as parser

from qfdfg.util import write_to, read_protobuf
from qfdfg.qfdfg_pb2 import Component, Flow, Graph
from compiler.parser import EngineSystemUtil


from esa.engines.engine import Engine

from definitions import COMPILER_DIR


class DefaultEngine(Engine):
    def __init__(self, qfdfg_pb=f'{NEUROWEAVER_PATH}/compiler/qfdfg.pb'):
        super(DefaultEngine, self).__init__('default')
        self.varcount = 0
        self.output_data = []

        # Dirty
        from qfdfg.qfdfg_pb2 import Component, Flow, Graph
        from qfdfg.util import write_to, read_protobuf
        self.graph = Graph()
        read_protobuf(qfdfg_pb, self.graph)

    def __str__(self):
        s = f"Default engine (Python)"
        return s

    def open(self):
        print("Opening default engine (Python)")

    def read(self):
        # TODO check self.output_data is set
        return self.output_data

    def write(self, *args):
        self.data = args[0]
        #print(self.data)

    def compute(self, capability: str, metadata):
        component = None
        for comp in self.graph.component_defs:
            if comp.name == capability:
                component = comp
        input_vars = self.gen_args(component)
        for i, input_arg in enumerate(component.input_args):
            globals()[input_arg] = self.data[i]

        for channel_name, channel_queue in metadata['channel_queues'].items():
            globals()[channel_name] = channel_queue
        state_args = ''
        if component.state_args != []:
            args = component.state_args
            state_args = ', '.join(args)

        output_vars = ''
        if component.output_vals != []:
            return_vals = component.output_vals
            output_vars = ', '.join(return_vals)

        executable = self.gen_python_func_call(metadata['obj_filename'], input_vars, output_vars, capability, metadata['outputs'], state_args)

        # exec() does not return a value; only used for side effects.
        compiled_executable = compile(executable, '<string>', 'exec')
        exec(compiled_executable, globals())
        # eval() returns the value.
        if output_vars != '': # Dirty (just the if statement)
            self.output_data = self.eval_output_vars(output_vars)
        if state_args != '':
            state_data = self.eval_state_args(state_args)
            self.output_data.extend(state_data)
        # else:
        #     self.output_data = None


    def close(self):
        pass

    def gen_python_func_args(self, input_data) -> str:
        invals = ''
        if input_data == ([],):
            return invals

        in_variables = {}
        for data in input_data:
            var = self.gen_variable()
            in_variables[var] = data
            globals()[var] = data
        invals = ', '.join(in_variables.keys())
        return invals

    def gen_python_func_return_vars(self, outputs, output_vals) -> str:
        if len(outputs) > 0:
            varlist = []
            for out_var in output_vals:
                varlist.append(self.gen_variable())
            variables = ', '.join(varlist)
        else:
            # TODO fix this
            flag = 'None'
            variables = flag
        return variables

    def gen_variable(self):
        var = f"var{self.varcount}"
        self.varcount += 1
        return var

    def gen_python_func_call(self, obj_filename, input_vars, output_vars, capability, outputs, state_args) -> str:
        obj_dir = COMPILER_DIR + '/build'
        # if component.domain_name == '':
        #     # print('debug:')
        #     # print(component)
        #     module = os.path.basename(component.obj_filename)[:-3]
        # else:
        #     module = 'ohai.' + component.domain_name
        module = os.path.basename(obj_filename)[:-3]

        imports = ('sys.path.insert(0, "{dir}")\n' +
                   'from {module} import {comp}\n').format(dir=obj_dir,
                                                           module=module,
                                                           comp=capability)

        output_vars = '{} = '.format(output_vars) if len(outputs) > 0 else ''

        # Dirty
        if state_args != '':
            state_args = ', ' + state_args

        # Do we need inputs here for comp instansiation?
        comp_call = '{assign}{comp}({inputs}{states})'.format(assign=output_vars,
                                                              comp=capability,
                                                              #inputs=input_vars,
                                                              inputs='',
                                                              states=state_args)

        print(comp_call)
        comp_call = self.replace_comp_inst(comp_call)

        print(comp_call)
        executable = imports + comp_call
        return executable

    def replace_comp_inst(self, line):
        comp = parser.get_component_by_name(line, self.graph.components)
        method_call = '.{method_name}({args}{channels})'.format(method_name=comp.name,
                                                      args=self.gen_args(comp), channels=', '.join(comp.channels))
        line  = line + method_call + '\n'
        return line

    def gen_args(self, component):
        args = component.input_args
        return ', '.join(args)

    def eval_output_vars(self, output_vars: str):
        print(f'eval_output_vars(): {output_vars}')

        outdata_list = []
        output_vars = output_vars.split(', ')
        for var in output_vars:
            outdata = eval(var)
            outdata_list.append(outdata)

        #print(outdata_list)
        return outdata_list

    def eval_state_args(self, state_args: str):
        print(f'eval_state_args(): {state_args}')
        outdata_list = []
        state_args = state_args.split(', ')
        for var in state_args:
            outdata = eval(var)
            outdata_list.append(outdata)
        return outdata_list

    # Returns the resources that
    def get_producer_resources(self):
        pass

    def get_consumer_resources(self):
        pass