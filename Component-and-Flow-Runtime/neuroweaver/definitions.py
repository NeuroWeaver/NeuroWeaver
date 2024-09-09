import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ESA_DIR = os.path.join(ROOT_DIR, 'esa')
ENGINE_SET_PBFILE = os.path.join(ESA_DIR, 'engine_system.pb')
COMPILER_DIR = os.path.join(ROOT_DIR, 'compiler')
QFDFG_PBFILE = os.path.join(COMPILER_DIR, 'qfdfg.pb')
GRAPH_VIS_JPEG = os.path.join(COMPILER_DIR, 'out.jpeg')
GRAPH_VIS_DOT = os.path.join(COMPILER_DIR, 'out.dot')
