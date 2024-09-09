import sys
sys.path.insert(0, '/Users/joon/ohai.src/qfdfg')
from qfdfg_pb2 import Component, Flow, Graph, FlowInfo
from util import write_to, read_protobuf


comp_A = Component(cid=0, name='comp_A')
comp_A.python_code = '''def comp_A():
    a = 1 + 2
    b = a + 2
    c = b - 2
    d = comp_B(c)
    e = d + 2
    return e
'''

comp_B = Component(cid=1, name='comp_B')
comp_B.python_code = '''def comp_B(a):
    b = a + 1
    c = b - 10
    return c
'''

comp_A.sub_components.extend([comp_B])
comp_B.super_component.extend([comp_A])

graph = Graph()
graph.components.extend([comp_A])
print(graph)

write_to('test3_serialization.pb', graph)

graph_deserialized = Graph()
read_protobuf('test3_serialization.pb', graph_deserialized)

assert graph_deserialized == graph
