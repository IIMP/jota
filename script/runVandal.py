import logging
import shlex
from subprocess import Popen, PIPE
import sys
import time
import signal, functools
import os
import Progressbar
import subprocess
bar=Progressbar.ProgressBar(total=100,width=200)
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
@timeout(300)
def VandalFunc(log_path,contract_file,logger):
	try:
		out_bytes=subprocess.check_output(['timeout','300','./decompile',log_path+contract_file,'-g',log_path+'Vandal/cfg.dot'])
	except subprocess.CalledProcessError as e:
				out_bytes=e.output
				code=e.returncode
				print out_bytes
				logger.error(out_bytes)
	return


if __name__ == '__main__':
	start_time = time.time()
	if len(sys.argv)>1:
		contract_path=sys.argv[1]
		if not contract_path.endswith('/'):
			contract_path+='/'
	else:
		contract_path='/home/iimp/Programs/CODING/top100_contract_run/'
	files=os.listdir(contract_path)
	fh=logging.FileHandler(filename=contract_path+'/log.txt',mode='a',encoding=None,delay=False)
	fh.setLevel(logging.ERROR)
	logger.addHandler(fh)
	os.chdir('/root/vandal/bin/')
	for file in files:
		print file
		if not '0x' in file:
			continue
		log_path=contract_path+file+'/'
		contract_files=os.listdir(log_path)
		for contract_file in contract_files:
			if not contract_file.endswith('.bytecode'):
				continue
			if not os.path.exists(log_path+'Vandal'):
				os.makedirs(log_path+'Vandal')
			logger.removeHandler(fh)
			fh=logging.FileHandler(filename=log_path+'Vandal/Vandal_log.txt',mode='a',encoding=None,delay=False)
			fh.setLevel(logging.ERROR)
			logger.addHandler(fh)
			try:
				VandalFunc(log_path,contract_file,logger)
			except TimeoutError as t:
				logger.error(t)
				print 'Timeout occured'
			finally:
				bar.move()
				bar.log("Processing")
	end_time = time.time()
	print end_time-start_time
