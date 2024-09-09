import sys
sys.path.append('/Users/joon/ohai.src/esa')
sys.path.append('/Users/joon/ohai.src/qfdfg')
import argparse

from antlr4 import *
from esa.grammar.engine_spec_lang.python.EslLexer import EslLexer
from esa.grammar.engine_spec_lang.python.EslParser import EslParser
from esa.grammar.engine_spec_lang.python.EslListener import EslListener

from esa.esa_pb2 import AbstractDomainDefinition
from esa.esa_pb2 import EngineSpecification
from esa.esa_pb2 import MemoryInterface
from esa.esa_pb2 import CapabilityInfo
from esa.esa_pb2 import MemoryInterfaceWithType
from esa.esa_pb2 import CapabilityImplementation
from esa.esa_pb2 import Value

from qfdfg.qfdfg_pb2 import Component

from qfdfg.util import write_to


class EnginePrinter(EslListener):
    def __init__(self, engine=None):
        """
        This class gets the engine name from the parse tree.
        """
        self._engine = engine

    def exitEngine_def(self, ctx):
        #print(ctx.ID())
        self._engine = str(ctx.ID())

    @property
    def engine(self):
        return self._engine


class DomainPrinter(EslListener):
    def __init__(self):
        """
        This class obtains the abstract domain that this engine implements.
        """
        self._domain = ''

    def exitEngine_def(self, ctx):
        implements = ctx.impl()
        if implements.getChildCount() > 0:
            self._domain = str(implements.ID())

    @property
    def domain(self):
        return self._domain


class EngineSpecGenerator(object):
    def __init__(self, tree):
        """
        This class generates the EngineSpecification data structure by
        walking the parse tree.
        """
        self.printer = EnginePrinter()
        self.domain_printer = DomainPrinter()
        self.walker = ParseTreeWalker()
        self.tree = tree

    def get_engine_name(self):
        self.walker.walk(self.printer, self.tree)
        return self.printer.engine

    def get_domain(self):
        self.walker.walk(self.domain_printer, self.tree)
        return self.domain_printer.domain

    def create(self):
        engine_spec = EngineSpecification()
        engine_spec.name = self.get_engine_name()
        engine_spec.domain_name = self.get_domain()

        return engine_spec


class MemoryInterfaceGenerator(object):
    def __init__(self, tree):
        """
        This class generates the MemoryInterface data structure by
        walking the parse tree.
        """
        self.tree = tree


class CapabilityInfoPrinter(EslListener):
    def __init__(self):
        """

        """
        self._cap_infos = []

    def exitCapability(self, ctx):
        # name = str(ctx.ID())
        # self._name = name
        cap_info = {}
        cap_info['name'] = str(ctx.ID())

        self._cap_infos.append(cap_info)

    @property
    def cap_infos(self):
        return self._cap_infos


class CapabilityInfoGenerator(object):
    def __init__(self, tree):
        """
        This class generates the CapabilityInfo data structure by
        walking the parse tree.
        """
        self.tree = tree
        self.cap_info_printer = CapabilityInfoPrinter()
        self.walker = ParseTreeWalker()

    def get_cap_infos(self):
        self.walker.walk(self.cap_info_printer, self.tree)
        return self.cap_info_printer.cap_infos

    def create(self):
        cap_infos = []

        for cap_info_dict in self.get_cap_infos():
            cap_info = CapabilityInfo()
            cap_info.name = cap_info_dict['name']

            # Generate MemoryInterfaceWithType data structure for this capability
            mem_iface_type_gen = MemoryInterfaceWithTypeGenerator(self.tree, cap_info.name)
            mem_iface_types = mem_iface_type_gen.create()
            cap_info.mem_interfaces.extend(mem_iface_types)

            cap_impl_gen = CapabilityImplementationGenerator(self.tree, cap_info.name)
            cap_impl = cap_impl_gen.create()
            cap_info.impl.CopyFrom(cap_impl)

            cap_infos.append(cap_info)
        return cap_infos


class MemoryInterfaceWithTypePrinter(EslListener):
    def __init__(self, capability_name):
        """

        """
        self.capability_name = capability_name
        self._args = ''

    def exitParams(self, ctx):
        # Only get the params for the given capability name
        curr_capability_name = str(ctx.parentCtx.ID())
        if self.capability_name == curr_capability_name:
            self._args = self.get_args(ctx)

    def get_args(self, capability_arg_list):
        cap_args = []
        if capability_arg_list.getChildCount() > 0:
            rest = self.get_args(capability_arg_list.capability_arg_list())
            cap_args += rest

            arg = capability_arg_list.capability_arg()
            cap_arg = {}
            if arg.memory_interface():
                cap_arg['mem_interface_name'] = str(arg.memory_interface().ID())
                cap_arg['data_type'] = str(arg.data_type().ID())
                cap_arg['var'] = str(arg.var().var_id().ID())
            elif arg.param_interface():
                cap_arg['param_interface_name'] = str(arg.param_interface().ID())
                cap_arg['literal_vals'] = str(self._get_literals())
                cap_arg['var'] = str(arg.ID())
            cap_args.append(cap_arg)
        return cap_args

    def _get_literals(self):
        return []

    @property
    def args(self):
        return self._args


class MemoryInterfaceWithTypeGenerator(object):
    def __init__(self, tree, capability_name):
        """

        """
        self.tree = tree
        self.walker = ParseTreeWalker()
        self.capability_name = capability_name
        self.mem_interface_printer = MemoryInterfaceWithTypePrinter(self.capability_name)

    def get_mem_interface_name(self):
        self.walker.walk(self.mem_interface_printer, self.tree)
        return self.mem_interface_printer.args

    def create(self):
        interfaces = []
        args = self.get_mem_interface_name()
        for arg in args:
            interface = MemoryInterfaceWithType()
            if 'mem_interface_name' in arg:
                interface.mem_interface_name = arg['mem_interface_name']
                interface.dtype_string = arg['data_type']
                interface.var = arg['var']
            elif 'param_interface_name' in arg:
                interface.mem_interface_name = arg['param_interface_name']
                interface.var = arg['var']
            interfaces.append(interface)
        return interfaces


class CapabilityImplementationPrinter(EslListener):
    def __init__(self, capability_name):
        """

        """
        self._specs = []
        self.capability_name = capability_name

    def exitCap_block(self, ctx):
        curr_capability_name = str(ctx.parentCtx.ID())
        if curr_capability_name == self.capability_name:
            specs = ctx.specs()
            self._specs = self.get_specs(specs)

    def get_specs(self, spec_list):
        if spec_list.getChildCount() > 0:
            spec = self.get_specs(spec_list.spec_list())
            attr = spec_list.spec().attr()
            spec_key = self._get_attr_type(attr.attr_id())
            spec_val = self._get_attr_val(spec_list.spec().attr_val())
            spec[spec_key] = spec_val
            return spec
        else:
            return {}

    def _get_attr_type(self, attr):
        if not attr.LANGUAGE() is None:
            return str(attr.LANGUAGE())
        if not attr.FILE() is None:
            return str(attr.FILE())
        if not attr.CODE() is None:
            return str(attr.CODE())
        if not attr.RUNTIME_COST() is None:
            return str(attr.RUNTIME_COST())

    def _get_attr_val(self, attr_val):
        if attr_val.ID() is not None:
            return str(attr_val.ID())
        if attr_val.STRING() is not None:
            return str(attr_val.STRING())
        if attr_val.INTLIT() is not None:
            return str(attr_val.INTLIT())

    @property
    def specs(self):
        return self._specs


class CapabilityImplementationGenerator(object):
    def __init__(self, tree, capability_name):
        """

        """
        self.tree = tree
        self.walker = ParseTreeWalker()
        self.capability_name = capability_name
        self.cap_impl_printer = CapabilityImplementationPrinter(self.capability_name)

    def get_cap_impl(self):
        self.walker.walk(self.cap_impl_printer, self.tree)
        return self.cap_impl_printer.specs

    def create(self):
        impl = CapabilityImplementation()
        specs = self.get_cap_impl()
        print(specs)
        if 'language' in specs:
            impl.language = specs['language']
        if 'file' in specs:
            impl.filepath = specs['file']
        if 'runtime_cost' in specs:
            runtime_cost = specs['runtime_cost']
            impl.runtime_cost = float(runtime_cost)
        return impl


# class CapabilityPrinter(AbstractDomainListener):
#     def __init__(self):
#         """
#         This class gets the Component data (e.g. name, flows) from the parse tree.
#         """
#         self._capability_names = []
#         self._components = []

#     def exitCapability(self, ctx):
#         capability_name = str(ctx.ID())
#         #print(capability_name)
#         self._capability_names.append(capability_name)

#         comp = Component()
#         comp.name = capability_name

#         params = ctx.params()
#         cap_params = self.get_params(params)
#         for p in cap_params:
#             if p['mem_interface_type'] == 'input':
#                 comp.input_args.append(p['var'])
#             elif p['mem_interface_type'] == 'output':
#                 comp.output_vals.append(p['var'])
#             elif p['mem_interface_type'] == 'state':
#                 pass
#             elif p['mem_interface_type'] == 'param':
#                 pass
#         self._components.append(comp)

#     def get_params(self, cap_arg_list):
#         #print(dir(cap_arg_list))
#         cap_args = []
#         if cap_arg_list.getChildCount() > 0:
#             rest = self.get_params(cap_arg_list.capability_arg_list())
#             cap_args += rest

#             arg = cap_arg_list.capability_arg()
#             cap_arg = {}
#             cap_arg['mem_interface_type'] = str(self._get_interface_type(arg.memory_interface()))
#             cap_arg['data_type'] = str(arg.data_type())
#             cap_arg['var'] = str(arg.var().var_id().ID())
#             cap_args.append(cap_arg)
#         return cap_args

#     def _get_interface_type(self, interface):
#         if not interface.INPUT() is None:
#             return interface.INPUT()
#         if not interface.OUTPUT() is None:
#             return interface.OUTPUT()
#         if not interface.PARAM() is None:
#             return interface.PARAM()
#         if not interface.STATE() is None:
#             return interface.STATE()

#     @property
#     def capability_names(self):
#         return self._capability_names

#     @property
#     def components(self):
#         return self._components


# class ComponentGenerator(object):
#     def __init__(self, tree):
#         """
#         This class generates the Component data structure by walking the parse tree.
#         """
#         self.printer = CapabilityPrinter()
#         self.walker = ParseTreeWalker()
#         self.tree = tree

#     def walk(self):
#         self.walker.walk(self.printer, self.tree)
#         return self.printer.components

#     def create(self):
#         components = self.walk()
#         return components

def parse_engine_spec(engine_spec_file, output_file='engine_spec.pb', verbose=False):
    input_stream = FileStream(engine_spec_file)
    lexer = EslLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = EslParser(stream)
    tree = parser.start()

    # First, generate EngineSpecification data structure
    engine_spec_gen = EngineSpecGenerator(tree)
    engine_spec = engine_spec_gen.create()
    #print(engine_spec)

    # Second, generate CapabilityInfo data structure
    cap_info_gen = CapabilityInfoGenerator(tree)
    cap_infos = cap_info_gen.create()

    engine_spec.capabilities.extend(cap_infos)
    write_to(output_file, engine_spec)
    if verbose:
        print(engine_spec)

def main(args):
    input_stream = FileStream(args.engine_spec_file)
    lexer = EslLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = EslParser(stream)
    tree = parser.start()

    # First, generate EngineSpecification data structure
    engine_spec_gen = EngineSpecGenerator(tree)
    engine_spec = engine_spec_gen.create()
    #print(engine_spec)

    # Second, generate CapabilityInfo data structure
    cap_info_gen = CapabilityInfoGenerator(tree)
    cap_infos = cap_info_gen.create()

    engine_spec.capabilities.extend(cap_infos)
    write_to(args.output_file, engine_spec)
    print(engine_spec)

    # Third, generate MemoryInterfaceWithType data structure
    # mem_iface_type_gen = MemoryInterfaceWithTypeGenerator(tree)
    # mem_iface_types = mem_iface_type_gen.create()
    #print(mem_iface_types)

    #
    # cap_info.mem_interfaces.extend(mem_iface_types)
    # print(cap_info)

    # # Second, generate Components for each capability in the domain
    # comp_gen = ComponentGenerator(tree)
    # comps = comp_gen.create()
    # print(comps)

    # # Add the Components to the abstract domain data structure
    # abstract_domain.capabilities.extend(comps)
    # print(abstract_domain)
    # write_to('abstract_domain.pb', abstract_domain)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Parse engine specification files.')
    argparser.add_argument('engine_spec_file',
                           help='Engine specification file (.engine) written in Engine Specification Language.')
    argparser.add_argument('-o', '--output_file',
                           default='engine_spec.pb',
                           help='output protobuf file (.pb). Default: engine_spec.pb')
    args = argparser.parse_args()

    main(args)
