import sys
sys.path.append('/Users/joon/ohai.src/esa')
sys.path.append('/Users/joon/ohai.src/qfdfg')
import argparse

from esa_pb2 import EngineOrg

from qfdfg.util import read_protobuf


def main(args):
    engine_sys = EngineOrg()
    read_protobuf(args.engine_sys, engine_sys)
    print(engine_sys)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Print engine system to stdout.')
    argparser.add_argument('engine_sys',
                           help='engine system protobuf (.pb)')
    args = argparser.parse_args()

    main(args)
