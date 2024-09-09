import argparse
import os
import random

from collections import deque, OrderedDict
from qfdfg_pb2 import Component, Flow, Graph
from util import write_to, read_protobuf

from definitions import GRAPH_VIS_JPEG, GRAPH_VIS_DOT


class DotGenerator:
    header = 'digraph G {' + '\n'
    footer = '}' + '\n'
    subgraph_templ = '''subgraph cluster_{} {{
    label="{}";
    style="rounded";
    {}
    }}\n'''
    subgraph_id = 0

    nodes = []

    def gendot(self, dfg):
        str_list = []
        str_list.append(self.header)

        subgraph_dotcode = ''
        for component in dfg.components:
            for subgraph in component.sub_components:
                subgraph_dotcode += self.gendot_graph(subgraph)
            subgraph_dotcode += self.gendot_graph(component)
            #print(subgraph_dotcode)

        str_list.append(subgraph_dotcode)

        edges = self.genedges(dfg.components)
        str_list.append(edges)

        str_list.append(self.footer)
        dot_code = ''.join(str_list)
        return dot_code

    def gendot_graph(self, dfg):
        subgraph_code = ''

        #if not dfg.has_sub_component():
        if len(dfg.sub_components) == 0:
            label = self.genlabel(dfg) + '\n'
            return label

        for subgraph in dfg.sub_components:
            subgraph_code += self.gendot_graph(subgraph)
        dotcode = self.subgraph_templ.format(str(self.subgraph_id),
                                             dfg.name,
                                             subgraph_code)
        self.subgraph_id += 1
        return dotcode

    def genedges(self, dfg):

        edge_code = ''
        #for subgraph in dfg.sub_components:
        for component in dfg:
            # for subgraph in component.sub_components:
            #    edge_code += self.genedges(subgraph)
            edge_code += self.genedges(component.sub_components)

            left = self.genlabel(component)
            #print(left)
            for child in component.outputs:
                #print(child)
                flowlist = component.outputs[child]
                for flow in flowlist.flows:
                    info = flow.info
                    right = '{"' + str(info.child_cid) + '" [label="' + child + '"]' + '}'
                    # TODO
                    # right = '{' + \
                    #     '"{}" [label="{}\\n{}"]'.format(info.child_cid,
                    #                                     child,
                    #                                     ) + \
                    #     '}'

                    #print(right)
                    edgelabel = ''
                    edge_code += str.format('{} -> {} [label="{}"];\n', left, right, edgelabel)

            # for child in dfg.children:
            #     right = self.genlabel(child)
            #     edge = dfg.get_outedge(child)
            #     if isinstance(edge, list):
            #         for e in edge:
            #             edgelabel = e.name
            #             flow = str.format('{} -> {} [label="{}"];\n', left, right, edgelabel)
            #             edge_code += flow
            #     else:
            #         edgelabel = edge.name
            #         flow = str.format('{} -> {} [label="{}"];\n', left, right, edgelabel)
            #         edge_code += flow
        return edge_code


    # def gendot(self, dfg):
    #     strList = []
    #     strList.append(self.header)

    #     engine_to_nodes ={}
    #     for node in dfg:
    #         if node.is_src or node.is_sink:
    #             continue
    #         engine_name = node.engine
    #         if engine_name not in engine_to_nodes:
    #             engine_to_nodes[engine_name] = [node]
    #         else:
    #             engine_to_nodes[engine_name].append(node)

    #     subgraph_list = []
    #     for engine in engine_to_nodes:
    #         subgraph = Subgraph(engine)
    #         for node in engine_to_nodes[engine]:
    #             subgraph.add_node(node)
    #         subgraph_list.append(subgraph.__str__())
    #     strList += subgraph_list

    #     self.bfs(dfg, strList)

    #     # append rank here
    #     # rank = genrank(cycle2id)
    #     # strList.append(rank)

    #     strList.append(self.footer)
    #     dotCode = ''.join(strList)
    #     return dotCode

    def bfs(self, dfg, strList):
        #initnodes = dfg.get_nodes_in_cycle(0)
        for node in dfg:
            strList.append(self.genlabel(node) + ';\n')

        idDict = {}  # node to dot label dictionary
        for node in dfg:
            idDict[node] = self.genlabel(node)

        # for k in idDict:
        #     print(k)

        initnodes = [dfg.pop(0)]  # source node
        queue = deque(initnodes)
        visitedList = set([])

        # for node in initnodes:
        #     idDict[node] = self.genlabel(node)
        #idDict['Sink'] = '"sink"'
        while len(queue) > 0:
            currNode = queue.popleft()

            # if currNode.capability == 'convert':
            #     print('convert!')
            # Connecting currNode with children
            left = idDict[currNode]
            for child in currNode.get_children():
                if child not in visitedList and child != 'Sink':
                    queue.append(child)
                    visitedList.add(child)

                # Child node doesn't have dot label
                if child not in idDict:
                    idDict[child] = self.genlabel(child)
                right = idDict[child]

                edgelabel = currNode.get_outedge(child)
                # flow is a line in dot file
                flow = str.format('{} -> {} [label="{}"];\n', left, right, edgelabel)
                strList.append(flow)
            visitedList.add(currNode)

        # for k in idDict:
        #     print(k)
        # for node in dfg:
        #     if node not in visitedList:
        #         print(node.to_dict())

        # temporary fix
        unvisited_nodes = []
        for node in dfg:
            if node not in visitedList:
                unvisited_nodes.append(node)

        for node in unvisited_nodes:
            left = idDict[node]
            for child in node.get_children():
                right = idDict[child]
                edgelabel = node.get_outedge(child)
                flow = str.format('{} -> {} [label="{}"];\n', left, right, edgelabel)
                strList.append(flow)

    def genlabel(self, graph):
        # if node.pe is not None:
        #     label = '{"' + str(node.id) + '" [label="' + node.op + ' ' + str(node.pe.id) +'"]' + '}'
        # else:
        #     label = '{"' + str(node.id) + '" [label="' + node.op +'"]' + '}'
        #label = '{"' + str(graph.cid) + '" [label="' + graph.name + '"]' + '}'
        label = '{' + \
            '"{}" [label="{}\\n{}"]'.format(graph.cid, graph.name, graph.engine_name) + \
            '}'
        return label

    def gen_subgraph(self):
        pass

    def genrank(self, cycle2id):
        rankCode = ''
        rankSink = '{rank = sink; "sink";};\n'

        # cycle2id is a dictionary of cycle to node id list
        for cycle in cycle2id:
            rankTempl = '{rank = same; '
            idList = cycle2id[cycle]
            sameRankIds = ''
            for id in idList:
                sameRankIds += '"' + str(id) + '"' + '; '
            rankTempl += sameRankIds + '};\n'
            rankCode += rankTempl
        rankCode += rankSink
        return rankCode

    def write_to(self, filename, dotcode):
        with open(filename, 'w') as f:
            f.write(dotcode)


class Subgraph:
    colors = ['red', 'green', 'blue', 'yellow', 'cyan']
    count = 0

    def __init__(self, engine):
        #self.color = random.choice(self.colors)
        self.color = self.colors[self.count]
        self.label = engine
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def __str__(self):
        nodes_list = []
        for node in self.nodes:
            nodes_list.append('"' + str(node.id) + '";\n')
        nodes_string = ''.join(nodes_list)
        string = 'subgraph cluster_' + str(Subgraph.count) + '{\n' \
                 + 'color=' + self.color + ';\n'\
                 + 'label=' + self.label + ';\n'\
                 + nodes_string + '\n'\
                 + '}\n'
        Subgraph.count += 1
        return string


def gendot(dfg, filename):
    dotgen = DotGenerator()
    dotcode = dotgen.gendot(dfg)
    dotgen.write_to(filename, dotcode)



def main(args):
    graph = Graph()
    read_protobuf(args.qfdfg, graph)

    gendot(graph, args.output_file)

    dot_command = f"dot -T jpeg -o {GRAPH_VIS_JPEG} {args.output_file}"
    os.system(dot_command)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='QF-DFG visualizer')
    argparser.add_argument('qfdfg',
                           help='QF-DFG protobuf file.')
    argparser.add_argument('-o', '--output_file',
                           default=GRAPH_VIS_DOT,
                           help='Generated dot file. Default: out.dot')
    args = argparser.parse_args()

    main(args)
