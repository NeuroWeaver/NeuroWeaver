import sys
sys.path.append('/Users/joon/ohai.src/esa')
sys.path.append('/Users/joon/ohai.src/qfdfg')
import argparse

from esa_pb2 import EngineSpecification

from qfdfg.util import read_protobuf


def main(args):
    engine_spec = EngineSpecification()
    read_protobuf(args.engine_pb, engine_spec)
    print(engine_spec)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Print engine spec protobuf to stdout.')
    argparser.add_argument('engine_pb',
                           help='engine protobuf (.pb)')
    args = argparser.parse_args()

    main(args)
