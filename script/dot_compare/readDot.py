import pydot 
def getDot(path)->"nodes,edges":
	graph = pydot.graph_from_dot_file(path)[0]
	return graph.get_nodes(),graph.get_edges()

def get_node_name(node)->str:
	return node.get_name()

def get_edge_from_to(edge)->"from,to":
	return edge.get_source(),edge.get_destination()
