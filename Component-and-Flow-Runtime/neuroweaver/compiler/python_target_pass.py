"""Compilation pass to read the IR and generate Python code for each Component.
"""

import os
import re
import importlib
import inspect
import argparse
import shutil
from collections import deque
import ast


from qfdfg.qfdfg_pb2 import Component, Flow, Graph
from qfdfg.util import write_to, read_protobuf
from compiler.parser import EngineSystemUtil, DomainImportParser

import compiler.parser as parser

from definitions import ENGINE_SET_PBFILE, COMPILER_DIR, QFDFG_PBFILE


class InitGenerator(object):
    body_template = 'self.{var} = {var}'
    init_template = '''def __init__(self{args}):\n{init_body}'''

    def __init__(self, component):
        """
        Given a component, generate Python class instance variable statements.
        """
        self.component = component

    def _generate(self, variable_names, indent=2):
        args = ', '.join(variable_names)
        args = ', ' + args if len(variable_names) > 0 else args

        init_body = ''
        # For terminal Components that are subcomponents of another Component,
        # instantiate the Component in __init__
        if len(self.component.sub_components) == 0:  # If this component is terminal,
            if len(self.component.super_component) > 0:
                print(len(self.component.super_component))
                super_component_name = self.component.super_component[0].name
                init_body += '    ' * indent + super_component_name + '()\n'
        else:
            body = filter_out_subcomponent_body(self.component.body)
            #body = join_body(body)
            body = adjust_indents(body)
            #print('body indents adjusted: ', component.name)
            #print(body)
            # body = indent_body(body)
            # print(body)
            body = list(map(lambda line : '    ' * indent + line, body))
            print(body)

            body = list(map(remove_comp_inst, body))
            print(body)

            body = ''.join(body)
            init_body += body

        init_body += self.gen_var_init(variable_names, indent)
        return InitGenerator.init_template.format(args=args, init_body=init_body)

    def generate(self):
        return self._generate(self.component.state_args)

    def gen_var_init(self, variable_names, indent=1):
        '''
        variable_names: list of variable names
        '''
        indent = '    ' * indent

        if len(variable_names) == 0:
            return indent + 'pass'

        stmts = [InitGenerator.body_template.format(var=var)
                 for var in variable_names]
        def prepend_indent(stmts, indent):
            return map(lambda line : indent + line, stmts)
        indented = prepend_indent(stmts, indent)
        return '\n'.join(indented)


class PyClassGenerator(object):
    template = '''class {class_name}(object):\n{static_vars}\n\n
    {init}\n\n{method}
    '''

    def __init__(self, component):
        """
        Given a component, generate a Python class with a method same name as
        the component name.
        """
        self.component = component
        self.var_gen = InitGenerator(self.component)
        #print(self.var_gen._generate(['weight1', 'weight2']))

    def _generate(self, class_name, static_vars, init, method):
        return PyClassGenerator.template.format(class_name=class_name,
                                                static_vars='',
                                                init=init,
                                                method=method)

    def generate(self):
        class_name = self.component.name
        static_vars = self.gen_static_vars()
        init = self.var_gen.generate()
        method = generate_func(self.component)
        #print('---' * 10)
        #print(method)
        lines = method.split('\n')
        lines = list(map(lambda line : '    ' + line + '\n', lines))

        def replace_with_self(line):
            if len(self.component.state_args) == 0:
                return line
            for arg in self.component.state_args:
                if arg in line:
                    return line.replace(arg, 'self.' + arg)
                else:
                    return line

        lines = list(map(replace_with_self, lines))
        #print(lines)

        def_line = lines[0]
        if len(self.component.input_args) + len(self.component.channels) == 0:
            def_line = def_line.replace('(', '(self')
        else:
            def_line = def_line.replace('(', '(self, ')
        lines[0] = def_line

        #print(lines)

        method = ''.join(lines)
        #print(method)
        #print('---' * 10)
        return self._generate(class_name, static_vars, init, method)

    def gen_static_vars(self, indent=1):
        body = filter_out_subcomponent_body(self.component.body)
        #body = join_body(body)
        body = adjust_indents(body)
        #print('body indents adjusted: ', component.name)
        #print(body)
        # body = indent_body(body)
        # print(body)
        body = list(map(lambda line : '    ' * indent + line, body))
        print(body)

        body = list(map(remove_comp_inst, body))
        print(body)

        body = ''.join(body)
        return body



def gen_filename(function_name):
    #build_dir = '/Users/joon/ohai.src/compiler/build'
    build_dir = COMPILER_DIR + '/build'
    if not os.path.isdir(build_dir):
        os.mkdir(build_dir)
    filename = build_dir + '/' + function_name + '.py'
    return filename

def write_to_python_file(component):
    '''Creates a python file for the given Component.'''
    filepath = component.obj_filename
    python_code = component.obj_code
    preambles_commeneted = prepend_comment_symbol(component.preambles)
    header_commeneted = prepend_comment_symbol(component.header)
    body_commeneted = prepend_comment_symbol(component.body)
    original_code = ''.join(preambles_commeneted) + ''.join(header_commeneted) + ''.join(body_commeneted)
    delimeter_original_begin = '### SECTION C&F ORIGINAL CODE BEGIN ###\n'
    delimeter_original_end = '### SECTION C&F ORIGINAL CODE END ###\n'
    delimeter_python_begin = '### SECTION PYTHON CODE BEGIN ###\n'
    delimeter_python_end = '### SECTION PYTHON CODE END ###\n'
    with open(filepath, 'w') as f:
        f.write(delimeter_python_begin)
        f.write(python_code)
        f.write(delimeter_python_end)
        f.write('\n')
        f.write(delimeter_original_begin)
        f.write(original_code)
        f.write(delimeter_original_end)

def prepend_comment_symbol(lines):
    commented = []
    for line in lines:
        comment = '# ' + line
        commented.append(comment)
    return commented

def generate_func_template(component):
    input_args = [x for x in component.input_args]
    input_args += [x for x in component.channels]
    if input_args != []:
        inputs = ', '.join(input_args)
    else:
        inputs = ''



    if component.output_vals != []:
        return_vals = component.output_vals

        # If top-level while loop is present,
        num_indents = 1
        for line in component.body:
            if 'while True' in line:
                num_indents += 1

        #return_vals = '    return ' + ', '.join(return_vals) + '\n'
        return_vals = '    ' * num_indents +  'return ' + ', '.join(return_vals) + '\n'
    else:
        return_vals = ''

    function_template = 'def {name}({inputs}):\n{{body}}\n{return_vals}'.format(name=component.name,
                                                                                inputs=inputs,
                                                                                body='body',
                                                                                return_vals=return_vals)
    return function_template

#build_dir = '/Users/joon/ohai.src/compiler/build'
build_dir = COMPILER_DIR + '/build'
ohai_domain_dir = build_dir + '/ohai'

def setup_dir(cnf_source, dependencies):
    if not os.path.isdir(build_dir):
        os.mkdir(build_dir)
    if not os.path.isdir(ohai_domain_dir):
        os.mkdir(ohai_domain_dir)
    src_dir = '/'.join(cnf_source.split('/')[0:-1])
    files = os.listdir(src_dir)
    for f in files:
        for d in dependencies:
            if f == d + '.py' or f == d:
                print(f)
                if f.endswith('.py'):
                    try:
                        shutil.copy(src_dir + '/' + f, build_dir)
                    except FileExistsError:
                        continue
                else:
                    try:
                        shutil.copytree(src_dir + '/' + f, build_dir + '/' + f)
                    except FileExistsError:
                        continue



def find_sync_primitives(component):
    producer_resources = []
    consumer_resources = []
    assignedValues = {}
    lines = []
    # Find resources that a component produces / consumes
    # Currently supports explicit name of resource as string, like:
    # componentProduce('name', data)
    # TODO: Modify implementation to support for example:
    # a = 'name'
    # componentProduce(a, data)
    # TODO: evaluate 'a' to generate the resource name
    for i, line in enumerate(component.body):
        lines.append(line)
        if 'componentProduce' in line or 'componentConsume' in line:
            for l in lines:
                if ":" not in l:
                    tree = ast.parse(l.lstrip())
                if '=' in l and '=='not in l and "componentConsume" not in l:
                    if len(tree.body)==0:
                        continue
                    try:
                        if isinstance(tree.body[0], ast.Assign):
                        #to do if assigned to operation say a = a+b
                            print(line)
                            result = eval(l[l.find('=')+1:],globals(), assignedValues)
                            if len(tree.body[0].targets)>1:
                                for target in tree.body[0].targets:
                                    assignedValues[target.id] = result[j]
                                    j+=1
                        else:
                            assignedValues[tree.body[0].targets[0].id] = result
                    except Exception:
                        pass
            lines = []
            if isinstance(tree.body[0].value, ast.Call):
                call = tree.body[0].value
                value = 0
                if isinstance(call.args[0], ast.Name):
                    value = assignedValues[call.args[0].id]
                else:
                    value = ast.literal_eval(call.args[0])
                print("value is",value)
                if call.func.id == 'componentProduce':
                    producer_resources.append((value, i))
                elif call.func.id == 'componentConsume':
                    consumer_resources.append((value, i))

    return producer_resources, consumer_resources


def generate_python(graph, engine_system):
    '''Given IR as input, generate a python module for each Component.'''
    # Handle sync primitives
    for component in graph.components:
        producer_resources, consumer_resources = find_sync_primitives(component)
        # Insert queues for producer consumer
        if component.engine_name == 'default':
            for resource, line_number in producer_resources:
                if resource not in component.channels:
                    component.channels.append(resource)
                modify_function_call = re.sub('componentProduce\((.*), (.*)\)', resource + '.put(\\2)', component.body[line_number])
                component.body[line_number] = modify_function_call
            for resource, line_number in consumer_resources:
                if resource not in component.channels:
                    component.channels.append(resource)
                modify_function_call = re.sub('componentConsume(.*)', resource + '.get()', component.body[line_number])
                component.body[line_number] = modify_function_call

    for component in graph.components:
        # Check if this component is an abstract domain capability
        if component.domain_name == '':
                component.obj_filename = gen_filename(component.name)
                classgen = PyClassGenerator(component)
                class_str = classgen.generate()
                component.obj_code = generate_preambles(component) + '\n' + class_str
                write_to_python_file(component)
        else:
            dest_filename = ohai_domain_dir + '/' + component.domain_name + '.py'
            with open(dest_filename, 'a') as f:
                f.write('')
    # TODO quick fix
    for component in graph.components:
        if component.engine_name == 'default':
            component.obj_filename = gen_filename(component.name)
            component.obj_code = generate_preambles(component) + '\n' + generate_func(component)
        else:
            dest_filename = ohai_domain_dir + '/' + component.domain_name + '.py'
            with open(dest_filename, 'a') as f:
                f.write('')
            if component.domain_name is not None and component.domain_name != '':
                engine = engine_system.get_engine_for_domain_by_name(component.engine_name, component.domain_name)
            else:
                engine = engine_system.get_engine_by_name(component.engine_name)
            capability_info = engine_system.get_capability_info(engine, component.name)
            engine_wrapper_filepath = capability_info.impl.filepath[1:-1]
            component.obj_filename = engine_wrapper_filepath
    func = 'import numpy as np\ndef fft(data_in):\n\treturn np.fft.fft(data_in)\n'
    dest_filename = ohai_domain_dir + '/digital_signal_processing.py'
    with open(dest_filename, 'a') as f:
        f.write(func)

def generate_preambles(component):
    preambles =  ''.join(component.preambles)
    if len(component.sub_components) == 0:  # If this component is terminal:
        if len(component.super_component) > 0:  # TODO ad-hoc
            super_component_name = component.super_component[0].name
            import_statement = f'from {super_component_name} import {super_component_name}'
            preambles += '\n' + import_statement + '\n'

    # for comp in component.sub_components:
        # TODO quick fix
        # if comp.domain_name == '':
        #     import_statement = 'from {module} import {component}'.format(module=comp.name, component=comp.name)
        #     preambles += '\n' + import_statement + '\n'
        #print(import_statement)
    return preambles

def generate_func(component):
    '''Given a Component, generate a Python function with same name as the Component .'''
    # TODO Fix this function to return a list of strings instead of a formatted string.
    body = filter_out_subcomponent_body(component.body)
    body = adjust_indents(body)
    body = list(map(lambda line : '    ' + line, body))
    body = list(map(replace_comp_inst, body))
    body = ''.join(body)
    func_template = generate_func_template(component)
    func = func_template.format(body=body)

    print(func)
    return func

def adjust_indents(body):
    first_line = body[0]
    default_indent = get_indent(first_line)
    body = map(lambda line : line[default_indent:], body)
    return list(body)

def indent_body(body, indent_level=1):
    #print(body)
    # #indented = body.replace('\n', '\n    ')
    # indented = line.replace('\n', '\n    ')
    # indented = '    ' + indented
    indent = '    ' * indent_level

    return body

def get_indent(line):
    return len(line) - len(line.lstrip())

def filter_out_subcomponent_body(body):
    '''Given a body, filter out lines that belong to subcomponent definition.'''
    filtered_body = []
    #print('*'*80)
    #print(body)
    first_line = body[0]
    default_indent = get_indent(first_line)
    # TODO quick fix
    subcomp_header_stack = []

    for line in body:
        #print(line)
        if 'with Component' in line:
            subcomp_header_stack.append(line)
            continue
        if get_indent(line) > default_indent and len(subcomp_header_stack) > 0:
            continue
        filtered_body.append(line)
    return filtered_body

def replace_comp_inst(line):
    '''Replace component call with component class instantiation and method invocation.'''

    global domains
    global aliases

    if line[-2:] == ":\n":
        return line
    comp = parser.get_component_by_name(line, graph.component_defs, domains, aliases)
    if comp and comp.state_args != []:
        method_call = '.{method_name}({args})'.format(method_name=comp.name,
                                                      args=gen_args(comp))
        # get rid of newline and append method call
        line  = line[:-1] + method_call + '\n'

        if len(comp.input_args) > 0:
            for arg in comp.input_args:
                # TODO: TOO DIRTY
                if line[line.index(arg) + len(arg)] == ',':
                    line = line.replace(arg + ',', '')
                else:
                    line = line.replace(arg, '')

        #print(line)
        return line
    else:
        return line

def remove_comp_inst(line):
    global domains
    global aliases
    if line[-2:] == ":\n":
        return line
    comp = parser.get_component_by_name(line, graph.component_defs, domains, aliases)
    if comp:
        return ''
    else:
        return line

def gen_args(component):
    args = component.input_args
    return ', '.join(args)


graph = Graph()

domains = ''
aliases = ''

def compile_target(cnf_source, qfdfg, engine_system=ENGINE_SET_PBFILE, output_file=QFDFG_PBFILE):
    global graph
    global domains
    global aliases

    # TODO why do we need this?
    graph = Graph()
    read_protobuf(qfdfg, graph)

    # TODO quick fix
    #engine_system = EngineSystemUtil(engine_system)

    domain_import_parser = DomainImportParser(cnf_source, engine_system)
    dependencies = domain_import_parser.filter_dependencies()
    domains, aliases = domain_import_parser.parse()

    setup_dir(cnf_source, dependencies)
    generate_python(graph, EngineSystemUtil(engine_system))
    print(graph)
    write_to(output_file, graph)
    return output_file

def main(args):
    global graph
    global domains
    global aliases

    # TODO why do we need this?
    graph = Graph()
    read_protobuf(args.qfdfg, graph)

    # TODO quick fix
    engine_system = EngineSystemUtil(args.engine_system)

    domain_import_parser = DomainImportParser(args.cnf_source, args.engine_system)
    domains, aliases = domain_import_parser.parse()

    generate_python(graph, engine_system)
    print(graph)
    write_to(args.output_file, graph)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='''Compile pass to generate Python target.
        Generates Python target for each component in build/ directory.''')
    argparser.add_argument('qfdfg',
                           help='Queued Fractalized Dataflow Graph (.pb)')
    argparser.add_argument('cnf_source',
                           help='C&F source program embedded in Python (.py)')
    argparser.add_argument('-o', '--output_file',
                           default=QFDFG_PBFILE,
                           help='Updated QF-DFG with Python target generated for each component. Default: qfdfg.pb')
    argparser.add_argument('-e', '--engine_system',
                           default=ENGINE_SET_PBFILE,
                           help='Engine system file (.pb). Default: esa/engine_system.pb')
    args = argparser.parse_args()

    main(args)
