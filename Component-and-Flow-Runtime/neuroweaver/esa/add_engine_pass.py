import sys
sys.path.append('/Users/joon/neuroweaver/qfdfg')
import argparse

from qfdfg.util import read_protobuf, write_to
from esa.esa_pb2 import AbstractDomainDefinition
from esa.esa_pb2 import EngineSpecification


def is_engine_impl(engine, domain):
    '''Checks if given engine implements given domain.'''
    return engine.domain_name == domain.name

def add_engine(engine_file='engine_spec.pb',
               remove_engine=None,
               domain_file='abstract_domain.pb',
               output_file='abstract_domain_with_engine.pb',
               verbose=False):
    domain = AbstractDomainDefinition()
    engine = EngineSpecification()
    read_protobuf(domain_file, domain)
    read_protobuf(engine_file, engine)

    if not remove_engine:
        if is_engine_impl(engine, domain):
            domain.engines.extend([engine])
    else:
        for i, e in enumerate(domain.engines):
            if e.name == remove_engine:
                del domain.engines[i]
    if verbose:
        print(domain)

    write_to(output_file, domain)

def main(args):
    domain = AbstractDomainDefinition()
    engine = EngineSpecification()
    read_protobuf(args.domain_file, domain)
    read_protobuf(args.engine_file, engine)


    if not args.remove_engine:
        if is_engine_impl(engine, domain):
            domain.engines.extend([engine])
    else:
        for i, e in enumerate(domain.engines):
            if e.name == args.remove_engine:
                del domain.engines[i]


    print(domain)

    write_to(args.output_file, domain)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Pass to add engine to abstract domain.')
    argparser.add_argument('engine_file',
                           default='engine_spec.pb',
                           help='Engine specification file (.pb)')
    # TODO: Remove this option and instead have this pass automatically figure out
    # which domain file to look up.

    argparser.add_argument('-d', '--domain_file',
                           default='abstract_domain.pb',
                           help='Abstract domain definition file (.pb). Default: abstract_domain.pb')
    argparser.add_argument('-o', '--output_file',
                           default='abstract_domain_with_engine.pb',
                           help='Updated domain file with engine spec (.pb). Default: abstract_domain_with_engine.pb')
    argparser.add_argument('-r', '--remove_engine',
                               help='Name of engine to be removed from this domian.')
    args = argparser.parse_args()

    main(args)
