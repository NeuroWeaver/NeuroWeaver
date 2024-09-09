import sys
sys.path.insert(0, '/Users/joon/ohai.src/qfdfg')
from qfdfg_pb2 import Component, Flow, Graph, FlowInfo
from util import write_to, read_protobuf


comp_A = Component(cid=0, name='comp_A')
comp_A.python_code = '''def comp_A():
    a = 1 + 2
    b = a + 2
    c = b - 2
    return c
'''

comp_B = Component(cid=1, name='comp_B')
comp_B.python_code = '''def comp_B(a):
    b = a + 1
    c = b - 10
    print(c)
'''

flow = Flow(info=FlowInfo(fid=0, local_name='comp_A_outflow'))
comp_A.outputs[comp_B.cid].CopyFrom(flow)
comp_B.inputs[comp_A.cid].CopyFrom(flow)

graph = Graph()
graph.components.extend([comp_A, comp_B])
print(graph)

write_to('test2_serialization.pb', graph)

graph_deserialized = Graph()
read_protobuf('test2_serialization.pb', graph_deserialized)

assert graph_deserialized == graph
