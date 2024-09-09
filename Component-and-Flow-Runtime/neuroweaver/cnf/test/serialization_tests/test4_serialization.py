import sys
sys.path.insert(0, '/Users/joon/ohai.src/qfdfg')
from qfdfg_pb2 import Component, Flow, Graph, FlowInfo
from util import write_to, read_protobuf


comp_A = Component(name='comp_A', cid=0)
comp_A.python_code = ''' import numpy as np
import mymodule
from mymodule import myfunc3

def myfunc(a, b):
    return a + b

def comp_A():
    a = [1, 2, 3]
    b = [4, 5, 6]
    c = np.dot(a, b)
    d = myfunc(b, c)
    e = mymodule.myfunc2(c, d)
    f = myfunc3(d, e)
    return f
'''

comp_B = Component(name='comp_B', cid=1)
comp_B.python_code = ''' import numpy as np
import mymodule
from mymodule import myfunc3

def myfunc(a, b):
    return a + b

def comp_B(f):
    g = f + 10
    return g
'''

f = Flow(info=FlowInfo(fid=0, local_name='comp_A_outflow'))
comp_A.outputs[comp_B.cid].CopyFrom(f)
comp_B.inputs[comp_A.cid].CopyFrom(f)

#print(comp_A)
# print(comp_B)
# write_to('test4_comp_A.pb', comp_A)
# write_to('test4_comp_B.pb', comp_B)

graph = Graph()
graph.components.extend([comp_A, comp_B])
print(graph)

write_to('test4_graph.pb', graph)

graph_deserialized = Graph()
read_protobuf('test4_graph.pb', graph_deserialized)

assert graph_deserialized == graph
