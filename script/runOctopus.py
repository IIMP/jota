#=====================Decorator============================
import sys
sys.path.append('/root/octopus')
from octopus.platforms.ETH.cfg import EthereumCFG
from octopus.analysis.graph import CFGGraph
import logging
PLATFORM = 'eth-evm'
import os
from datetime import datetime
import threading
import signal, functools
import time
start_time = time.time()
result = ""
if len(sys.argv)>1:
	contract_path=sys.argv[1]
	if not contract_path.endswith('/'):
		contract_path+='/'
else:
	contract_path='/home/iimp/Programs/CODING/top100_contract_run/'
class TimeoutError(Exception):pass 
 
def timeout(seconds,logger=logging.getLogger(), error_message="Timeout Error: the cmd 300s have not finished."):
	def decorated(func):
		result = ""
 
		def _handle_timeout(signum, frame):
			global result
			result = error_message
			raise TimeoutError(error_message)
 
		def wrapper(*args, **kwargs):
			global result
			signal.signal(signal.SIGALRM, _handle_timeout)
			signal.alarm(seconds)
 
			try:
				result = func(*args, **kwargs)
			except Exception as e:
				print(e)
				logger.error(e)
			finally:
				signal.alarm(0)
				return result
			return result
 
		return functools.wraps(func)(wrapper)
 
	return decorated
#===========================MainBody================================
logger=logging.getLogger()
fh=logging.FileHandler(filename=contract_path+'log.txt',mode='a',encoding=None,delay=False)
fh.setLevel(logging.ERROR)
logger.addHandler(fh)
count=0
@timeout(300,logger)
def octo_func(line,addr):
	print("1111111111Creating CFG1111111111")
	octo_cfg = EthereumCFG(line)
	print("2222222222Creating Graph2222222222")
	octo_graph = CFGGraph(octo_cfg,addr=addr)
	print("3333333333Creating PDF3333333333")
	octo_graph.view(simplify=True, ssa=True,view=False)


files=os.listdir(contract_path)# files=os.walk(contract_path)
for file in files:# next(files)
	if not '0x' in file:
		continue
	log_path=contract_path+file+'/'
	contract_files=os.listdir(log_path)
	for contract_file in contract_files:
		if not contract_file.endswith('.bytecode'):
			continue
		if not os.path.exists(log_path+'Octopus'):
			os.mkdir(log_path+'Octopus')
# for addr,nll,bytecodeFiles in files:
# 	print("Dealing with %s"%addr)
# 	if not addr.startswith(contract_path+'0x'):
# 		print("Not a contract folder")
# 		continue
# 	if addr.endswith('temp'):
# 		print("It is a 'temp' folder= =")
# 		continue
# 	count+=1
# 	have_bytecode=False
# 	for i in bytecodeFiles:
# 		if i.endswith('forSecurify'):
# 			print("====BYTECODE FOUND====")
# 			input_file=open(addr+'/'+i,'r')
# 			have_bytecode=True
# 			break
# 	if not have_bytecode:
# 		raise BaseException('Bytecode not found in %s!'%addr)
# 	line=input_file.read().strip()
# 	# if " " in line:
# 	# 	line = line.split(" ")[1]
# 	input_file.close()
# 	addr=addr+'/'
#	print("oooooooooooooooooooo\n%s\noooooooooooooooooooo"%line)
		logger.removeHandler(fh)
		fh=logging.FileHandler(filename=log_path+'Octopus/Octo_log.txt',mode='a',encoding=None,delay=False)
		fh.setLevel(logging.ERROR)
		logger.addHandler(fh)
		with open(log_path+contract_file,'r') as f:
			print(contract_file)
			line=f.read()
		try:
			octo_func(line,log_path+'Octopus/')
		except Exception as e:
			print(e)


print("Total processed contract amount:%d"%count)
print("Total processing time:%d"%(time.time()-start_time))
