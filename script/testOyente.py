import logging
import shlex
from subprocess import Popen, PIPE
import sys
import time
import signal, functools
import os


# os.chdir('/home/iimp/repository/oyente-master/oyente/')
# def get_exitcode_stdout_stderr(cmd):
#	 """
#	 Execute the external command and get its exitcode, stdout and stderr.
#	 """
#	 args = shlex.split(cmd)

#	 proc = Popen(args, stdout=PIPE, stderr=PIPE)
#	 out, err = proc.communicate()
#	 exitcode = proc.returncode
#	 #
#	 return exitcode, out, err

# cmd="python3 oyente.py --bytecode -s /home/iimp/Programs/CODING/top100_contract_run/0x209c4784ab1e8183cf58ca33cb740efbf3fc18ef/0x209c4784ab1e8183cf58ca33cb740efbf3fc18ef.forSecurify -g"
# exitcode, out, err=get_exitcode_stdout_stderr(cmd)
# print(exitcode)
# if exitcode:
# 	print(err)
# 	print(out)
sys.path.append('/home/iimp/repository/oyente-master/oyente/')
from oyente import *
import logging
import shlex
from subprocess import Popen, PIPE
import sys
import time
import signal, functools
import os
import Progressbar3
bar=Progressbar3.ProgressBar(total=100,width=200)
successRate=0
#timeout part
class TimeoutError(Exception):pass 
logger=logging.getLogger()
def timeout(seconds,logger=logging.getLogger(),error_message="Timeout Error: the cmd 300s have not finished."):
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
				logger.error(e)
			finally:
				signal.alarm(0)
				return result
			return result
 
		return functools.wraps(func)(wrapper)
 
	return decorated
#cmd part
@timeout(300)
def OyenteFunc(source,logger,successRate):
	try:
		out_bytes=subprocess.check_output(['python3','/home/iimp/Programs/CODING/top100_contract_run/OyenteSubprogress.py',log_path+contract_file])
		successRate+=1
	except subprocess.CalledProcessError as e:
		out_bytes=e.output
		code=e.returncode
		print(out_bytes)
		logger.error(out_bytes)
	except Exception as e:
		print(e)
		logger.error(e)
	return successRate

if __name__ == '__main__':
	contract_path='/home/iimp/Programs/CODING/top100_contract_run/'
	files=os.listdir(contract_path)
	fh=logging.FileHandler(filename='/home/iimp/Programs/CODING/top100_contract_run/test/log.txt',mode='a',encoding=None,delay=False)
	fh.setLevel(logging.ERROR)
	logger.addHandler(fh)
	os.chdir('/home/iimp/repository/oyente-master/oyente/')
	for file in files:
		if not file.startswith('0x'):
			continue
		log_path=contract_path+file+'/'
		contract_files=os.listdir(log_path)
		for contract_file in contract_files:
			if not contract_file.endswith('forSecurify'):
				continue
			print("Processing %s"%contract_file)
			source = log_path+contract_file
			if not os.path.exists(log_path+'Oyente'):
				os.makedirs(log_path+'Oyente')
			logger.removeHandler(fh)
			fh=logging.FileHandler(filename=log_path+'Oyente/Oyente_log.txt',mode='a',encoding=None,delay=False)
			fh.setLevel(logging.ERROR)
			logger.addHandler(fh)
			try:
				successRate = OyenteFunc(source,logger,successRate)
			except TimeoutError as t:
				logger.error(t)
				print(t)
			except Exception as e:
				logger.error(e)
				print(e)
			finally:
				bar.move()
				bar.log("Processing")
	print("Successrate is %d"%successRate)