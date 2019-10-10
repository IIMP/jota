import logging
import shlex
from subprocess import Popen, PIPE
import sys
import time
import signal, functools
import os
import Progressbar
import shutil
import subprocess
bar=Progressbar.ProgressBar(total=100,width=200)
#timeout part
class TimeoutError(Exception):pass 
logger=logging.getLogger()
def timeout(seconds,logger=logging.getLogger(),error_message="Timeout Error: the cmd 300s have not finished."):
	def decorated(func):
		global result
		result = ''
 
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
def OyenteFunc(log_path,contract_file,logger):
	try:
		os.chdir(log_path)
		out_bytes=subprocess.check_output(['nice','python','/home/iimp/repository/oyente-master/oyente/oyente.py','-s',log_path+contract_file,'-j','-g','-db','-t','600000'])
	except subprocess.CalledProcessError as e:
		out_bytes=e.output
		code=e.returncode
		if out_bytes=='True\n':
			with open(log_path+'OyenteSucessed','w') as w:
				w.write("Yes")
		logger.error(out_bytes)
	except Exception as e:
		print e
		logger.error(e)
	return


if __name__ == '__main__':
	if len(sys.argv)>1:
		contract_path=sys.argv[1]
		if not contract_path.endswith('/'):
			contract_path+='/'
	else:
		contract_path='/home/iimp/Programs/CODING/top100_contract_run/'
	files=os.listdir(contract_path)
	fh=logging.FileHandler(filename='/home/iimp/Programs/CODING/top100_contract_run/test/log.txt',mode='a',encoding=None,delay=False)
	fh.setLevel(logging.ERROR)
	logger.addHandler(fh)
	for file in files:
		if not file.startswith('0x'):
			continue
		log_path=contract_path+file+'/'
		contract_files=os.listdir(log_path)
		for contract_file in contract_files:
			if not contract_file.endswith('forSecurify'):
				continue
			if not os.path.exists(log_path+'Oyente'):
				os.makedirs(log_path+'Oyente')
			else:
				shutil.rmtree(log_path+'Oyente')
				os.makedirs(log_path+'Oyente')
			logger.removeHandler(fh)
			fh=logging.FileHandler(filename=log_path+'Oyente/Oyente_log.txt',mode='a',encoding=None,delay=False)
			fh.setLevel(logging.ERROR)
			logger.addHandler(fh)
			# OyenteFunc(log_path,contract_file,logger)
			try:
				OyenteFunc(log_path,contract_file,logger)
			except TimeoutError as t:
				logger.error(t)
				print 'Timeout occured'
			except Exception as e:
				logger.error(e)
				print e
	# 		finally:
	# 			bar.move()
	# 			bar.log("Processing")
	# 			print("Total success num:%d"%cnt)
	