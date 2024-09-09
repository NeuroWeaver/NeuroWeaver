"""Front-end of the compiler that takes C&F source program as input and
generates an intermediate representation (QF-DFG) which is serialized to protobuf."""

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
import tokenize
from six.moves import StringIO, cStringIO
# from qfdfg_pb2 import Component, Flow, Graph
# from util import write_to, read_protobuf
# from esa_pb2 import EngineOrg

from definitions import ENGINE_SET_PBFILE, QFDFG_PBFILE


DEBUG = True

class ComponentStack:
    def __init__(self):
        self.stack = deque()

    def push(self, component):
        self.stack.append(component)

    def get_default(self):
        return self.stack[-1] if len(self.stack) >= 1 else None

    def pop(self):
        self.stack.pop()

    def isempty(self):
        return len(self.stack) == 0


class ParseCall(ast.NodeVisitor):
    def __init__(self):
        self.ls = []
    def visit_Attribute(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        self.ls.append(node.attr)
    def visit_Name(self, node):
        self.ls.append(node.id)


class FindFuncs(ast.NodeVisitor):
    def visit_Call(self, node):
        p = ParseCall()
        p.visit(node.func)
        #print( ".".join(p.ls))
        ast.NodeVisitor.generic_visit(self, node)
        self.func = ".".join(p.ls)


component_id = 0

def generate_cid():
    global component_id

    cid = component_id
    component_id += 1
    return cid

flow_id = 0

def generate_fid():
    global flow_id
    fid = flow_id
    flow_id += 1
    return fid

def readlines(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines

def is_component_definition(line):
    if 'with Component' in line:
        return True
    return False

def create_component(line):
    '''Given a Component definition line, create a corresponding Component.'''
    pattern = r'Component\((.*)\) as (.*)'
    match = re.search(pattern, line)
    if match:
        matched = match.groups()
        name = matched[1][:-1]
        component = Component(name=name)
        #component.header = line
        component.header.append(line)
        line = trim(line)
        #print(line)
        args = parse_arguments(line)
        #print(args)

        # TODO: handle connectivity
        if 'inputs' in args:
            component.input_args.extend(args['inputs'])
        if 'outputs' in args:
            component.output_vals.extend(args['outputs'])
        if 'state' in args:
            component.state_args.extend(args['state'])

        return component
    else:
        raise Exception('Invalid Component definition!')

def trim(line):
    start = line.index('Component')
    end = line.index('as ')
    trimmed = line[start:end]
    return trimmed

def parse_arguments(line):
    p = parse(line)
    args = {}
    for node in p.body:
        for line in walk(node):
            if isinstance(line, Call):
                for arg in line.args:
                    # TODO: temporary solution
                    #args.append(line.args[0].s)
                    args['instance_name'] = line.args[0].s
                for keyword in line.keywords:
                    for kwarg in keyword.value.elts:
                        keyword_arg = keyword.arg
                        arg_name = kwarg.id
                        if keyword_arg in args:
                            args[keyword_arg].append(arg_name)
                        else:
                            args[keyword_arg] = [arg_name]
    return args

def get_function_call(line):
    tree = ast.parse(line.lstrip())
    visitor = FindFuncs()
    visitor.visit(tree)
    if hasattr(visitor, 'func'):
        return visitor.func
    else:
        return None

def get_component_by_name(line, components, domains=None, aliases=None, verbose=False):
    #if "Component" not in line:
    #    return None
    try:
        func = get_function_call(line)
        if verbose:
            print(f'debug: {func}')
        if not func:
            return None
        for comp in components:
            if func == comp.name:
                return comp

        if domains != None and aliases != None:
            capability = lookup_capability(line, domains, aliases)
            if capability:
                return capability

        # for alias in aliases:
        #     alias_call = alias + '.'
        #     if alias_call in line:
        #         start_index = line.index(alias_call)
        #         end_index = line.index('(')
        #         comp_str = line[start_index + len(alias_call) : end_index]
        #         print(comp_str)

        return None
    except SyntaxError as e:
        print('syntax error:')
        # TODO: Need a better fix
        print(line[-2:])
        raise RuntimeError(f"Syntax error: {e}")
    except IndentationError:
        raise RuntimeError(f'indentation error:{line}')
        # print(line)
        # pass

# def extract_components(lines):
#     components = []
#     component_stack = ComponentStack()
#     prev_indents = 0

#     for line in lines:
#         #print(component_stack.stack)
#         if is_component_definition(line):
#             component = create_component(line)
#             components.append(component)
#             component_stack.push(component)
#         elif component_stack.get_default() is None:
#             continue
#         else:
#             curr_indents = count_indents(line)
#             #print(curr_indents, prev_indents)
#             if curr_indents < prev_indents and not component_stack.isempty():
#                 component_stack.pop()
#             if not component_stack.isempty():
#                 curr_component = component_stack.get_default()
#                 prev_indents = curr_indents
#                 curr_component.python_code += line

#                 # handle subcomponents
#                 comp = get_component_by_name(line, components)
#                 if comp:
#                     curr_component.sub_components.extend([comp])
#                     comp.super_component.extend([curr_component])

#     return components

def count_indents(line):
    # Count based on whether src code is written with spaces or tabs for indent
    if line.startswith('\t'):
        chars_per_indent = 1
    else:
        chars_per_indent = 4
    indents = (len(line) - len(line.lstrip())) / chars_per_indent
    return int(indents)

def trim_indent(component):
    indent = component.header.index('with ')
    component.header = component.header[indent:]

def set_preambles(preambles, components):
    for component in components:
        component.preambles.extend(preambles)

def is_empty_line(line):
    if line.strip() == '':
        print('line is empty!')

components = []

def is_complete_statement(line):
    """
    Checks if the lines form a complete python statment.
    """
    if line[-2:] == ":\n":
        return False
    else:
        return True

def generate_ir(cnf_source, domains, aliases, verbose=False):
    '''Parse the given C&F source file, generate the IR, and serialize it to
    protobuf.
    '''
    lines = readlines(cnf_source)
    # TODO: Move to a parser class instead of using global variables all over the place?
    global components_instantiated
    global components
    components_instantiated = []
    components = []
    component_stack = ComponentStack()
    prev_indents = 0
    preambles = []

    comp_instantiation_stmts = []

    for line in lines:
        if verbose:
            print(line)

        if is_component_definition(line):
            component = create_component(line)
            components.append(component)
            component_stack.push(component)
            comp_scope_indent = count_indents(line) + 1
        elif component_stack.get_default() is None:
            # This corresponds to component instantiations
            if len(components) > 0:  # If we have already encountered component defs
                comp_instantiation_stmts.append(line)
                #parse_line(line, domains, aliases)
            else:
                preambles.append(line)
        else:
            curr_indents = count_indents(line)
            # Done with nested component definition??
            if curr_indents < prev_indents and not component_stack.isempty() and curr_indents < comp_scope_indent:
                component_stack.pop()
            if not component_stack.isempty():
                curr_component = component_stack.get_default()
                if is_complete_statement(line):
                    # handle subcomponents
                    comp = get_component_by_name(line, components, domains, aliases, verbose=verbose)
                    if comp:
                        #print(f'debug: {comp.name}')
                        curr_component.sub_components.extend([comp])
                        comp.super_component.extend([curr_component])

                        # TODO is this needed?
                        curr_component.body.extend(comp.header)
                        curr_component.body.extend(comp.body)

                        # quick fix
                        parse_line(line.lstrip(), domains, aliases, verbose=verbose)

                    # Check if current line calls an abstract domain capability
                    capability = lookup_capability(line, domains, aliases)
                    if capability:
                        components.append(capability)
                        #components_instantiated.append(capability)
                        curr_component.sub_components.extend([capability])

                curr_component.body.append(line)
            prev_indents = curr_indents

    parse_comp_instantiation_stmts(comp_instantiation_stmts, domains, aliases)

    set_preambles(preambles, components)
    set_preambles(preambles, components_instantiated)

    graph = Graph()
    #graph.components.extend(components)
    graph.components.extend(components_instantiated)
    graph.component_defs.extend(components)
    return graph


def lookup_capability(line, domains, aliases):
    component = None
    try:
        func = get_function_call(line)
        if func:
            #print(func)
            namespace = func.split('.')
            if len(namespace) == 1:
                return None
            elif len(namespace) >= 2:
                domain = namespace[0]
                capability = namespace[1]
                # print(domain, capability)
                if domain in domains:
                    #raise Exception('Domain {} not imported.'.format(domain))
                    capabilities = domains[domain]
                    if capability in capabilities:
                        #raise Exception('Capability {} not specified in {} abstract domain.'.format(capability, domain))
                        component = capabilities[capability]
                        parse_comp_instantiation_stmts([line.strip()], domains, aliases)
                        component.domain_name = aliases[domain]
            # TODO not a long term solution
            # p = parse(line.lstrip())
            # for node in p.body:
            #     if isinstance(node, ast.Assign):
            #         comp_name = get_component_call_name(node)
            #         print(comp_name)
    except SyntaxError:
        pass
    except IndentationError:
        pass
        #print(func)
    return component

# list to keep tract of all instantiated components
components_instantiated = []

# symbol table; key: output var name, value: reference to component
output_name_table = {}

def parse_line(line, domains, aliases, iter_count=1, verbose=False):
    '''Go through each line and generate graph connectivity.'''
    p = parse(line)
    for node in p.body:
        if isinstance(node, ast.Assign) or isinstance(node, ast.Expr):
            component_name, domain_name = get_component_call_name(node)
            output_names = get_output_names(node)
            input_names = get_input_names(node)

            connect_components(component_name, input_names, output_names, domain_name, domains, aliases, iter_count, verbose=verbose)
            save_output_names(component_name, output_names)
            save_input_names(component_name, input_names)


def parse_comp_instantiation_stmts(stmts, domains, aliases):
    code = ''.join(stmts)
    tree = ast.parse(code)

    for node in tree.body:
        if isinstance(node, ast.For):
            iter_count = _parse_iter_count(node)
            for body in node.body:
                _parse_body(body, domains, aliases, iter_count)
        elif isinstance(node, ast.Assign) or isinstance(node, ast.Expr):
            _parse_body(node, domains, aliases)


def _parse_iter_count(ast_node):
    for n in ast.walk(ast_node):
        if isinstance(n, ast.Num):
            #print('iter count: ', n)
            return n.n


def _parse_body(ast_node, domains, aliases, iter_count=1):
    component_name, domain_name = get_component_call_name(ast_node)
    output_names = get_output_names(ast_node)
    input_names = get_input_names(ast_node)

    connect_components(component_name, input_names, output_names, domain_name, domains, aliases, iter_count)
    save_output_names(component_name, output_names)
    save_input_names(component_name, input_names)


def connect_components(component_name, input_names, output_names, domain_name, domains, aliases, iter_count, verbose=False):
    comp = lookup_component(component_name, domain_name, domains, aliases)
    if comp:
        comp_instance = Component()
        comp_instance.CopyFrom(comp)
        comp_instance.cid = generate_cid()
        components_instantiated.append(comp_instance)

        # Set iteration count
        comp_instance.iter_count = iter_count

        for in_name in input_names:
            if in_name in output_name_table:
                parent_comp = output_name_table[in_name]
                #f = FlowList()
                # comp_instance.inputs[parent_comp.name] = f
                # parent_comp.outputs[comp_instance.name] = f
                flowlist = comp_instance.inputs.get_or_create(parent_comp.name)
                #flows.CopyFrom(f)
                flow = Flow()
                flow.info.fid = generate_fid()
                flow.info.src_comp_name = parent_comp.name
                flow.info.dst_comp_name = component_name
                flow.info.var_name = in_name
                flow.info.child_cid = comp_instance.cid
                flowlist.flows.extend([flow])

                flowlist = parent_comp.outputs.get_or_create(comp_instance.name)
                #flows.CopyFrom(f)
                # flow = Flow()
                # flow.info.fid = generate_fid()
                flowlist.flows.extend([flow])
        for outname in output_names:
            if outname not in output_name_table:
                output_name_table[outname] = comp_instance
            # TODO: Should we raise an exception here?
            else:
                pass
            if verbose:
                print(f'output name table: {output_name_table}')
    else:
        #print('connecting components: ', component_name)
        # Allow interleaving of python code and component calls
        pass
        #raise Exception('Instantiation of undefined Component: {}'.format(component_name))

def save_output_names(component_name, output_names):
    comp = None
    # TODO: change the data structure from list to dict
    for component in components_instantiated:
        if component.name == component_name:
            comp = component
    if comp:
        comp.output_names.extend(output_names)

def save_input_names(component_name, input_names):
    comp = None
    for component in components_instantiated:
        if component.name == component_name:
            comp = component
    if comp:
        comp.input_names.extend(input_names)

def get_input_names(assign_node):
    component_call = assign_node.value
    inputs = []
    for name in component_call.args:
        if isinstance(name, ast.Name):
            inputs.append(name.id)
        elif isinstance(name, ast.Num):
            inputs.append(name.n)
    return inputs

def get_component_call_name(node):
    if isinstance(node, ast.Assign):
        component_call = node.value
    elif isinstance(node, ast.Expr):
        component_call = node.value

    # TODO ad-hoc
    if isinstance(component_call.func, ast.Attribute):
        domain_name = component_call.func.value.id
        #print(domain_name)
        capability = component_call.func.attr
        #print(capability)
        return capability, domain_name

    return component_call.func.id, None

def get_output_names(node):
    if isinstance(node, ast.Expr):
        return []
    outputs = node.targets[0]
    if isinstance(outputs, ast.Tuple):
        output_vals = outputs.elts
        return [val.id for val in output_vals]
    else:
        return [outputs.id]

def lookup_component(name, domain_name, domains, aliases):
    if domain_name is None:
        for comp in components:
            if name == comp.name:
                return comp
    else:
        capabilities = domains[domain_name]
        component = capabilities[name]
        component.domain_name = aliases[domain_name]
        return component

    return None


class DomainImportParser(object):
    def __init__(self, cnf_source, engine_system_file):
        """
        Class to filter domain import statements and generate component definitions
        for imported domains.
        """
        # C&F source file
        self.cnf_source = cnf_source
        # Engine system data structure
        self.engine_system = EngineSystemUtil(engine_system_file)
        # All import statements
        self.all_imports = self.filter_all_imports()
        # Verbatim string list of import statements for abstract domains
        self.domain_import_stmts = self.filter_domain_imports()
        # Abstract domains imported; Key: domain name. Value: AbstractDomainDefinition
        self.domains = {}
        # Aliases used in import statements
        self.aliases = {}

    def filter_all_imports(self):
        '''Obtain all import statements.'''
        lines = readlines(self.cnf_source)
        lines = [x.lstrip() for x in lines]
        imports = []
        is_multiline_comment = False
        for line in lines:
            if not is_multiline_comment:
                if line.startswith('import') or (line.startswith('from') and 'import' in line):
                    imports.append(line)
            if '"""' in line:
                is_multiline_comment = not is_multiline_comment

        return imports

    def filter_dependencies(self):
        dependencies = []
        for line in self.all_imports:
            parsed_line = ast.parse(line)
            if isinstance(parsed_line.body[0], ast.Import):
                for name_object in parsed_line.body[0].names:
                    dependencies.append(name_object.name.split('.')[0])
            elif isinstance(parsed_line.body[0], ast.ImportFrom):
                module = parsed_line.body[0].module
                dependencies.append(module.split('.')[0])
            else:
                raise Exception(f'All statements should be an import or import from statement. Found {line}')
        return dependencies

    def filter_domain_imports(self):
        '''Filter ohai domain imports from all import statements.'''
        lines = []
        for line in self.all_imports:
            if 'ohai' in line:
                lines.append(line)
        #self.domain_import_stmts += lines
        return lines

    def parse(self):
        if self.domain_import_stmts == []:
            return self.domains, self.aliases

        for line in self.domain_import_stmts:
            begin = line.index('ohai')
            line = line[begin:]
            alias = ''
            if 'as ' in line:
                end = line.index('as ')
                alias = line[end + len('as '):].strip()
                line = line[:end]
            # In most cases there should be only two items
            namespace = line.split('.')
            root = namespace[0].strip()
            domain = namespace[1].strip()

            capabilities = self.engine_system.get_capabilities_by_domain_name(domain)
            if alias != '':
                self.domains[alias] = capabilities
            else:
                self.domains[domain] = capabilities

            if alias != '':
                self.aliases[alias] = domain

        return self.domains, self.aliases


class EngineSystemUtil(object):
    def __init__(self, engine_system_file):
        """
        Utility class for engine system functions.
        """
        self.engine_system_file = engine_system_file
        self.engine_system = self.init_engine_system()

    def init_engine_system(self):
        '''Read engine_system.pb file and populate EngineOrg data structure'''
        if not os.path.exists(self.engine_system_file):
            raise Exception('Engine System file does not exist.')
        engine_system = EngineOrg()
        read_protobuf(self.engine_system_file, engine_system)
        return engine_system

    def find_domain_by_name(self, domain_name):
        for domain in self.engine_system.domains:
            if domain.name == domain_name:
                return domain
        raise RuntimeError(f"Unable to find {domain_name} in domains. Supported domains:\n"
                           f"{self.engine_system.domains}")

    def get_capabilities_by_domain_name(self, domain_name):
        '''Returns a dict of Components (capabilities) for the given domain.'''
        abstract_domain = self.find_domain_by_name(domain_name)
        #print('FLAG', abstract_domain)
        capabilities = {}
        for component in abstract_domain.capabilities:
            capabilities[component.name] = component
        return capabilities

    def get_default_engine(self, domain_name):
        '''Returns default engine for the given domain.'''
        domain = self.find_domain_by_name(domain_name)
        for engine in domain.engines:
            return engine

    def get_capability_info(self, engine, capability_name):
        '''Returns capability info for the given engine and capability name'''
        for capability_info in engine.capabilities:
            if capability_info.name == capability_name:
                return capability_info

    def get_engine_by_name(self, engine_name):
        """Go through every domain and search for the engine with the given name"""
        for domain in self.engine_system.domains:
            for engine in domain.engines:
                if engine.name == engine_name:
                    return engine

    def get_engine_for_domain_by_name(self, engine_name, domain_name):
        """In given domain search for the engine with the given name"""
        domain = self.find_domain_by_name(domain_name)
        for engine in domain.engines:
            if engine.name == engine_name:
                return engine

    def get_engines_by_domain_capability(self, domain_name, capability_name):
        '''Return a list of engines that support the given capability in the domain'''
        engines = []
        domain = self.find_domain_by_name(domain_name)
        for engine in domain.engines:
            for capability_info in engine.capabilities:
                if capability_info.name == capability_name:
                    engines.append(engine)
        return engines

def parse_program(cnf_source, output_file=QFDFG_PBFILE, engine_system=ENGINE_SET_PBFILE,verbose=False):
    # Parse abstract domain import statements (e.g. import ohai.deep_learning)
    domain_import_parser = DomainImportParser(cnf_source, engine_system)
    domains, aliases = domain_import_parser.parse()
    if verbose:
        print('domains: ', domains)
        print('aliases:', aliases)

    qfdfg = generate_ir(cnf_source, domains, aliases, verbose=verbose)

    write_to(output_file, qfdfg)
    if verbose:
        print('*' * 16 + ' QFDFG Protobuf ' + '*' * 16)
        print(qfdfg)

    # Check QF-DFG is correctly serialized
    graph_deserialized = Graph()
    read_protobuf(output_file, graph_deserialized)
    assert graph_deserialized == qfdfg
    return output_file

def main(args):
    # Parse abstract domain import statements (e.g. import ohai.deep_learning)
    domain_import_parser = DomainImportParser(args.cnf_source, args.engine_system)
    domains, aliases = domain_import_parser.parse()
    if DEBUG:
        print('domains: ', domains)
        print('aliases:', aliases)

    qfdfg = generate_ir(args.cnf_source, domains, aliases)
    write_to(args.output_file, qfdfg)
    print('*' * 16 + ' QFDFG Protobuf ' + '*' * 16)
    print(qfdfg)

    # Check QF-DFG is correctly serialized
    graph_deserialized = Graph()
    read_protobuf(args.output_file, graph_deserialized)
    assert graph_deserialized == qfdfg


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='C&F source parser which generates a Queued Fractalized Dataflow Graph.')
    argparser.add_argument('cnf_source',
                           help='C&F source program embedded in Python (.py)')
    argparser.add_argument('-o', '--output_file',
                           default=QFDFG_PBFILE,
                           help='Queued Fractalized Dataflow Graph file (.pb). Default: qfdfg.pb')
    argparser.add_argument('-e', '--engine_system',
                           default=ENGINE_SET_PBFILE,
                           help='Engine system file (.pb). Default: esa/engine_system.pb')
    args = argparser.parse_args()

    main(args)
