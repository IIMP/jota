import logging
import shlex
from subprocess import Popen, PIPE
import sys
import time
import signal, functools

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
@timeout(2,logger)
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
	fh=logging.FileHandler(filename='/home/iimp/Programs/CODING/top100_contract_run/test/log.txt',mode='a',encoding=None,delay=False)
	fh.setLevel(logging.ERROR)
	logger.addHandler(fh)
	# for i in range(3):
	# 	logger.removeHandler(fh)
	# 	fh=logging.FileHandler(filename='/home/iimp/Programs/CODING/top100_contract_run/test/%dlog.txt'%i,mode='a',encoding=None,delay=False)
	# 	fh.setLevel(logging.ERROR)
	# 	logger.addHandler(fh)
	# 	try:
	# 		func()
	# 	except:
	# 		pass
	cmd='python3 whileTrue.py'
	try:
		exitcode, out, err=get_exitcode_stdout_stderr(cmd)
	except ValueError:
		pass
	else:
		if exitcode:
			err_message = err.decode('utf-8').splitlines()
			logger.error(err_message[-1])