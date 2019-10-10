import logging
import shlex
from subprocess import Popen, PIPE
import sys
import time
import signal, functools
import os
import Progressbar
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
#cmd part
@timeout(300,logger)
def get_exitcode_stdout_stderr(cmd):
	"""
	Execute the external command and get its exitcode, stdout and stderr.
	"""
	args = shlex.split(cmd)

	proc = Popen(args, stdout=PIPE, stderr=PIPE)
	out, err = proc.communicate()
	exitcode = proc.returncode
	#
	return exitcode, out, err

if __name__ == '__main__':
	if len(sys.argv)>1:
		contract_path=sys.argv[1]
		if not contract_path.endswith('/'):
			contract_path+='/'
	else:
		contract_path='/home/iimp/Programs/CODING/top100_contract_run/'
	files=os.listdir(contract_path)
	fh=logging.FileHandler(filename=contract_path+'log.txt',mode='a',encoding=None,delay=False)
	fh.setLevel(logging.ERROR)
	logger.addHandler(fh)
	os.chdir('/root/securify/')
	for file in files:
		if not '0x' in file:
			continue
		log_path=contract_path+file+'/'
		contract_files=os.listdir(log_path)
		for contract_file in contract_files:
			if not contract_file.endswith('.bytecode'):
				continue
			cmd='timeout 300 java -jar /root/securify/build/libs/securify.jar -fh %s --livestatusfile %s'%(log_path+contract_file,log_path+'Securify/result.json')
			if not os.path.exists(log_path+'Securify'):
				os.makedirs(log_path+'Securify')
			logger.removeHandler(fh)
			if os.path.exists(log_path+'Securify/Securify_log.txt'):
				os.remove(log_path+'Securify/Securify_log.txt')
			fh=logging.FileHandler(filename=log_path+'Securify/Securify_log.txt',mode='a',encoding=None,delay=False)
			fh.setLevel(logging.ERROR)
			logger.addHandler(fh)
			try:
				exitcode, out, err=get_exitcode_stdout_stderr(cmd)
			except ValueError:
				bar.move()
				bar.log("Processing")
				pass
			else:
				if exitcode:
					err_message = err.decode('utf-8').splitlines()
					logger.error(err_message)
					print(cmd)
				bar.move()
				bar.log("Processing")
	# for i in range(3):
	# 	logger.removeHandler(fh)
	# 	fh=logging.FileHandler(filename='/home/iimp/Programs/CODING/top100_contract_run/test/%dlog.txt'%i,mode='a',encoding=None,delay=False)
	# 	fh.setLevel(logging.ERROR)
	# 	logger.addHandler(fh)
	# 	try:
	# 		func()
	# 	except:
	# 		pass
	
