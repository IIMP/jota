import os
path='/home/iimp/Programs/CODING/top100_contract_run/'
files=os.listdir(path)
for file in files:
	if os.path.isdir(path+file):
		if not file.startswith('0x'):
			continue
		log_path=path+file+'/Mythril/'
		nowfiles=os.listdir(log_path)
		for i in nowfiles:
			if i=='graph.html':
				os.remove(log_path+i)
				continue
			if not i.startswith('Mythril'):
				continue
			if i.endswith('log.txt'):
				os.remove(log_path+i)