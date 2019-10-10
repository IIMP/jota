import networkx as nx
from readDot import *
octo_file = '/root/test2019/contracts/00-0xeba02cfc36c01acbe10f6bcb909b76749e54956a/Octopus/graph.cfg.gv'
vandal_file = '/root/test2019/contracts/00-0xeba02cfc36c01acbe10f6bcb909b76749e54956a/Vandal/cfg.dot'
nodes_octo , edges_octo = getDot(octo_file)
nodes_vandal, edges_vandal = getDot(vandal_file)
def get_graph(nodes,edges):
        G = nx.DiGraph()

        for node in nodes:
                name = get_node_name(node)
                G.add_node(name)
        for edge in edges:
                source,destination = get_edge_from_to(edge)
                G.add_edge(source,destination)
        return G
Go = get_graph(nodes_octo,edges_octo)
Gv = get_graph(nodes_vandal,edges_vandal)
print(nx.is_isomorphic(Go,Gv))


