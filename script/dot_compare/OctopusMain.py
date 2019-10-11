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
	for edge in edges:
		source,destination = get_edge_from_to(edge)
		G.add_edge(source,destination)
	return G
def main():
	contracts = os.listdir(target_folder)
	pool = multiprocessing.Pool(100)
	results = []
	TypeContract = list([] for i in range(5))
	for contract in contracts:
		results.append(pool.apply_async(compare_contract,args=(contract,)))
	pool.close()
	pool.join()
	for i in results:
		num,con = i.get()
		TypeContract[num].append(con)
		type_num[num] += 1
	for i,j in enumerate(type_num):
		print("type",i,":",j)
	for i in range(5):
		print("Type%d: "%i,TypeContract[i])
	
	
		
		



def compare_contract(contract):
	if not '0x' in contract:
		return 0,contract
	if not os.path.exists(path+contract+'/Octopus/graph.cfg.gv'):
		return 1,contract
	if not os.path.exists(target_folder+contract+'/Octopus/graph.cfg.gv'):
		#type2.append(contract)
		return 2,contract
	nodes_ori,edges_ori = getDot(path+contract+'/Octopus/graph.cfg.gv')
	graph_ori =  get_graph(nodes_ori,edges_ori)
	nodes_gen,edges_gen = getDot(target_folder+'/'+contract+'/Octopus/graph.cfg.gv')
	graph_gen = get_graph(nodes_gen,edges_gen)
	if nx.is_isomorphic(graph_ori,graph_gen):
		#print("Type 44444:",contract)
		return 4,contract
	else:
		#print("Type 333333:",contract)
		return 3,contract


if __name__=='__main__':
	main()
