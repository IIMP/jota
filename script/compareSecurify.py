import os
import sys
import json
import multiprocessing
path = '/root/test2019/contracts/'
target_path = sys.argv[1]
folders = os.listdir(path)
type_num = list(0 for i in range(5))

def main():
	pool = multiprocessing.Pool()
	results = []
	for contract in folders:
		results.append(pool.apply_async(compare_contract,args = (contract,)))
	pool.close()
	pool.join()
	for i in results:
		num = i.get()
		type_num[num]+=1
	for i,j in enumerate(type_num):
		print("type",i,":",j)

def compare_contract(contract):
	if not '0x' in contract:
		return 0
	if not os.path.exists(path+contract+'/Securify/result.json') or os.path.getsize(path+contract+'/Securify/result.json')== 0:
		return 1
	if not os.path.exists(target_path+contract+'/Securify/result.json') or os.path.getsize(target_path+contract+'/Securify/result.json') == 0:
		return 2
	fff = contract+'/Securify/result.json'
	with open(path+fff) as f:
		content_ori = json.load(f)
	with open(target_path + fff) as f:
		content_gen = json.load(f)
	if not content_ori['securifyErrors']:
		return 1
	if content_gen['securifyErrors']['errors'] != [] or content_gen['patternResults'] == {}:
		print(contract)
		print(content_gen['securifyErrors']['errors'])
		return 2
	content_ori = content_ori['patternResults']
	content_gen = content_gen['patternResults']
	flags = ['hasConflicts','hasViolations','hasWarnings','hasSafe']
	for k,v in content_ori.items():
		if not k in content_gen.keys():
			print("==========",content_gen)
		for flag in flags:
			if not v[flag] == content_gen[k][flag]:
				return 3
	return 4

if __name__ == '__main__':
	main()
