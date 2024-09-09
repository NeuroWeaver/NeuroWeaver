import sys
sys.path.append('/Users/joon/ohai.src/qfdfg')
import argparse
import os

from qfdfg.util import read_protobuf, write_to
from esa.esa_pb2 import AbstractDomainDefinition
from esa.esa_pb2 import EngineOrg

def add_domain(domain_files='abstract_domain_with_engine.pb', remove_domain=None,output_file='engine_system.pb', verbose=False):
    engine_system = EngineOrg()
    if os.path.exists(output_file):
        read_protobuf(output_file, engine_system)
    domain_index_map = {}
    for i, d in enumerate(engine_system.domains):
        if d.name == remove_domain:
            del engine_system.domains[i]
    for i, d in enumerate(engine_system.domains):
        domain_index_map[d.name] = i
    if isinstance(domain_files, str):
        domain_files = [domain_files]
    for domain_file in domain_files:
        domain = AbstractDomainDefinition()
        read_protobuf(domain_file, domain)
        if domain.name in domain_index_map:
            for i, d in enumerate(engine_system.domains):
                if d.name == domain.name:
                    del engine_system.domains[i]
        engine_system.domains.append(domain)
    if verbose:
        print(engine_system)
    write_to(output_file, engine_system)

def main(args):
    domains = []
    for domain_file in args.domain_files:
        domain = AbstractDomainDefinition()
        read_protobuf(domain_file, domain)
        domains.append(domain)

    engine_system = EngineOrg()
    if os.path.exists(args.output_file):
        read_protobuf(args.output_file, engine_system)

    # TODO: Add a sanity check to prevent adding same domain multiple times
    if not args.remove_domain:
        engine_system.domains.extend(domains)
    else:
        for i, d in enumerate(engine_system.domains):
            if d.name == args.remove_domain:
                del engine_system.domains[i]

    print(engine_system)

    write_to(args.output_file, engine_system)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Pass to add domain(s) to engine system.')
    argparser.add_argument('domain_files',
                           nargs='+',
                           default='abstract_domain_with_engine.pb',
                           help='Abstract domain definition file.')
    argparser.add_argument('-o', '--output_file',
                           default='engine_system.pb',
                           help='Hierarchical organization of domains and engines. (default: engine_system.pb)')
    argparser.add_argument('-r', '--remove_domain',
                               help='Name of domain to be removed.')
    args = argparser.parse_args()

    main(args)
