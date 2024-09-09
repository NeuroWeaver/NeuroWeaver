import sys
sys.path.insert(0, '/Users/joon/ohai.src/qfdfg')
from qfdfg_pb2 import Component, Flow, Graph
from util import write_to, read_protobuf


comp_A = Component(cid=0, name='comp_A')
comp_A.python_code ='''def comp_A():
a = 1 + 2;    b = a + 2;    c = b - 2'''

# print(comp_A)
# write_to('test1.pb', comp_A)

# component = Component()
# read_protobuf('test1.pb', component)

# assert comp_A == component

graph = Graph()
graph.components.extend([comp_A])
print(graph)

write_to('test1_graph.pb', graph)

graph_deserialized = Graph()
read_protobuf('test1_graph.pb', graph_deserialized)

assert graph_deserialized == graph
