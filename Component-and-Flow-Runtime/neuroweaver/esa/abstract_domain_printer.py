import sys
sys.path.append('/Users/joon/ohai.src/esa')
sys.path.append('/Users/joon/ohai.src/qfdfg')
import argparse

from esa_pb2 import AbstractDomainDefinition

from qfdfg.util import read_protobuf


def main(args):
    domain = AbstractDomainDefinition()
    read_protobuf(args.domain_pb, domain)
    print(domain)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Print abstract domain definition protobuf to stdout.')
    argparser.add_argument('domain_pb',
                           help='abstract domain definition protobuf (.pb)')
    args = argparser.parse_args()

    main(args)
