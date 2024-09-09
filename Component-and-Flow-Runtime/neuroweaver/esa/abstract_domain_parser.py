import sys
sys.path.append('/Users/joon/ohai.src/esa')
sys.path.append('/Users/joon/ohai.src/qfdfg')
import argparse

from antlr4 import *
from esa.grammar.abstract_domain.python.AbstractDomainLexer import AbstractDomainLexer
from esa.grammar.abstract_domain.python.AbstractDomainParser import AbstractDomainParser
from esa.grammar.abstract_domain.python.AbstractDomainListener import AbstractDomainListener

from esa.esa_pb2 import AbstractDomainDefinition
from qfdfg.qfdfg_pb2 import Component

from qfdfg.util import write_to


class AbstractDomainPrinter(AbstractDomainListener):
    def __init__(self, domain=None):
        """
        This class gets the abstract domain name from the parse tree.
        """
        self._domain = domain

    def exitDomain_def(self, ctx):
        #print(ctx.ID())
        self._domain = str(ctx.ID())

    @property
    def domain(self):
        return self._domain


class AbstractDomainGenerator(object):
    def __init__(self, tree):
        """
        This class generates the AbstractDomainDefinition data structure by
        walking the parse tree.
        """
        self.printer = AbstractDomainPrinter()
        self.walker = ParseTreeWalker()
        self.tree = tree

    def walk(self):
        self.walker.walk(self.printer, self.tree)
        return self.printer.domain

    def create(self):
        domain = AbstractDomainDefinition()
        domain.name = self.walk()
        return domain


class CapabilityPrinter(AbstractDomainListener):
    def __init__(self):
        """
        This class gets the Component data (e.g. name, flows) from the parse tree.
        """
        self._capability_names = []
        self._components = []

    def exitCapability(self, ctx):
        capability_name = str(ctx.ID())
        #print(capability_name)
        self._capability_names.append(capability_name)

        comp = Component()
        comp.name = capability_name

        params = ctx.params()
        cap_params = self.get_params(params)
        for p in cap_params:
            if p['mem_interface_type'] == 'input':
                comp.input_args.append(p['var'])
            elif p['mem_interface_type'] == 'output':
                comp.output_vals.append(p['var'])
            elif p['mem_interface_type'] == 'state':
                comp.state_args.append(p['var'])
            elif p['mem_interface_type'] == 'param':
                comp.param_args.append(p['var'])
        self._components.append(comp)

    def get_params(self, cap_arg_list):
        #print(dir(cap_arg_list))
        cap_args = []
        if cap_arg_list.getChildCount() > 0:
            rest = self.get_params(cap_arg_list.capability_arg_list())
            cap_args += rest

            arg = cap_arg_list.capability_arg()
            cap_arg = {}
            cap_arg['mem_interface_type'] = str(self._get_interface_type(arg.memory_interface()))
            cap_arg['data_type'] = str(arg.data_type())
            cap_arg['var'] = str(arg.var().var_id().ID())
            cap_args.append(cap_arg)
        return cap_args

    def _get_interface_type(self, interface):
        if not interface.INPUT() is None:
            return interface.INPUT()
        if not interface.OUTPUT() is None:
            return interface.OUTPUT()
        if not interface.PARAM() is None:
            return interface.PARAM()
        if not interface.STATE() is None:
            return interface.STATE()

    @property
    def capability_names(self):
        return self._capability_names

    @property
    def components(self):
        return self._components


class ComponentGenerator(object):
    def __init__(self, tree):
        """
        This class generates the Component data structure by walking the parse tree.
        """
        self.printer = CapabilityPrinter()
        self.walker = ParseTreeWalker()
        self.tree = tree

    def walk(self):
        self.walker.walk(self.printer, self.tree)
        return self.printer.components

    def create(self):
        components = self.walk()
        return components



def parse_abstract_domain(domain_file, output_file="abstract_domain.pb", verbose=False):
    input_stream = FileStream(domain_file)
    lexer = AbstractDomainLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = AbstractDomainParser(stream)
    tree = parser.start()

    # First, generate abstract domain data structure
    domain_gen = AbstractDomainGenerator(tree)
    abstract_domain = domain_gen.create()
    #print(abstract_domain)
    #write_to('abstract_domain_1.pb', abstract_domain)

    # Second, generate Components for each capability in the domain
    comp_gen = ComponentGenerator(tree)
    comps = comp_gen.create()
    #print(comps)

    # Add the Components to the abstract domain data structure
    abstract_domain.capabilities.extend(comps)
    if verbose:
        print(abstract_domain)
    write_to(output_file, abstract_domain)

def main(args):
    input_stream = FileStream(args.domain_file)
    lexer = AbstractDomainLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = AbstractDomainParser(stream)
    tree = parser.start()

    # First, generate abstract domain data structure
    domain_gen = AbstractDomainGenerator(tree)
    abstract_domain = domain_gen.create()
    #print(abstract_domain)
    #write_to('abstract_domain_1.pb', abstract_domain)

    # Second, generate Components for each capability in the domain
    comp_gen = ComponentGenerator(tree)
    comps = comp_gen.create()
    #print(comps)

    # Add the Components to the abstract domain data structure
    abstract_domain.capabilities.extend(comps)
    print(abstract_domain)
    write_to(args.output_file, abstract_domain)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Parse abstract domain definition files.')
    argparser.add_argument('domain_file',
                           help='abstract domain definition file (.domain)')
    argparser.add_argument('-o', '--output_file',
                           default='abstract_domain.pb',
                           help='output protobuf file (.pb). Default: abstract_domain.pb')
    args = argparser.parse_args()

    main(args)
