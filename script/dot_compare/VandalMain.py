import sys
from readDot import *
import networkx as nx
import networkx.algorithms.isomorphism as iso
import os
target_folder = sys.argv[1]#Complete path
path = '/root/2017Dataset/contracts/'
import multiprocessing
type_num = list(0 for i in range(5))


class Node:
	def __init__(self,name):
		self.name = name
		self.children = []
		self.parents = []
		self.in_degree = 0
		self.out_degree = 0
		self.label = None

	def __eq__(self,other):
		return int(self.name.strip('"'),16) == int(other.name.strip('"'),16)
	def __lt__(self,other):
		return int(self.name.strip('"'),16) < int(other.name.strip('"'),16)
def get_graph(nodes,edges):
	G = nx.DiGraph()

	for node in nodes:
		name = get_node_name(node)
		G.add_node(name)
	for edge in edges:
		source,destination = get_edge_from_to(edge)
		G.add_edge(source,destination)
	return G
def main():
	contracts = os.listdir(target_folder)
	pool = multiprocessing.Pool(100)
	results = []
	for contract in contracts:
		results.append(pool.apply_async(compare_contract,args=(contract,)))
	pool.close()
	pool.join()
	for i in results:
		num = i.get()
		type_num[num] += 1
	for i,j in enumerate(type_num):	
		print("type",i,":",j)

def compare_contract(contract):
	if not '0x' in contract:
		return 0
	if not os.path.exists(path+contract+'/Vandal/cfg.dot'):
		return 1
	if not os.path.exists(target_folder+contract+'/Vandal/cfg.dot'):
		if os.path.exists(target_folder+contract+'/Vandal/Vandal_log.txt'):
			with open(target_folder+contract+'/Vandal/Vandal_log.txt','r') as f:
				lines = f.read()
				if '300s' not in lines:
					print(str(lines))
				else:
					print("Timeout!")
		return 2
	nodes_ori,edges_ori = getDot(path+contract+'/Vandal/cfg.dot')
	graph_ori =  get_graph(nodes_ori,edges_ori)
	nodes_gen,edges_gen = getDot(target_folder+'/'+contract+'/Vandal/cfg.dot')
	graph_gen = get_graph(nodes_gen,edges_gen)
	if nx.is_isomorphic(graph_ori,graph_gen):
		print(contract)
		return 4
	else:
		print("Not isomorphic:",contract)
		return 3


if __name__ == '__main__':
	main()
