from ast import literal_eval
import bs4
import os
import networkx as nx
import sys
target_path = sys.argv[1]
path = '/root/test2019/contracts/'
import multiprocessing
type_num = list(0 for i in range(5))
type_list = list([] for i in range(5))

def main():
	contracts = os.listdir(path)
	pool = multiprocessing.Pool(100)
	results = []
	for contract in contracts:
		results.append(pool.apply_async(compare_contract,args = (contract,)))
	pool.close()
	pool.join()
	for i in results:
		num = i.get()
		type_num[num]+=1
	for i,j in enumerate(type_list):
		print("type",i)
		print(j)
	for i,j in enumerate(type_num):
		print("type",i,":",j)


def compare_contract(contract):
	if not '0x' in contract:
		return 0
	if not os.path.exists(path+contract+'/Mythril/graph.html'):
		return 1
	if not os.path.exists(target_path + contract + '/Mythril/graph.html'):
		print("type2:",contract)
		return 2
	with open(path+contract+'/Mythril/graph.html','r') as f:
		lines = f.read()
	G1 = get_graph(lines)
	with open(target_path+contract+'/Mythril/graph.html','r') as f:
		lines = f.read()
	G2 = get_graph(lines)
	if nx.is_isomorphic(G1,G2):
		print("type4:",contract)
		return 4
	else:
		print("type3",contract)
		return 3

def get_graph(lines):
	soup = bs4.BeautifulSoup(lines,'html.parser')
	tags = soup.find_all('script')[1]
	temp = str(tags).strip('</script>')
	temp = temp[temp.find('var edges'):]
	temp = temp[:temp.find(';')]
	temp = temp[temp.find('['):]
	mlist = literal_eval(temp)
	G = nx.DiGraph()
	for i in mlist:
		fr = i['from']
		to = i['to']
		G.add_edge(fr,to)
	return G
	

if __name__ == '__main__':
	main()
