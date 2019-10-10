#=====================Decorator============================
#Usage:python2 runErays contract_path
#==========================================================
import sys
sys.path.append('/root/erays')
import structurer
import logging
import shutil
PLATFORM = 'eth-evm'
import os
from datetime import datetime
import threading
import signal, functools
import Progressbar
import time
bar=Progressbar.ProgressBar(total=100,width=200)
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
            result = error_message
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
#===========================MainBody================================
start_time = time.time()
logger=logging.getLogger()
fh=logging.FileHandler(filename=contract_path+'log.txt',mode='a',encoding=None,delay=False)
fh.setLevel(logging.ERROR)
logger.addHandler(fh)
count=0

@timeout(300,logger)
def erays_func(line,addr):
    # print("1111111111Creating Structurer11111111111")
    a=structurer.Structurer(line)
    output_path=addr
    # print("2222222222Creating PDF222222222222222222")
    a.visualize_functions(output_path)

files=os.listdir(contract_path)# files=os.walk(contract_path)
for file in files:# next(files)
    if not '0x' in file:
            continue
    log_path=contract_path+file+'/'
    contract_files=os.listdir(log_path)
    for contract_file in contract_files:
        if not contract_file.endswith('.bytecode'):
            continue
        if not os.path.exists(log_path+'Eraystemp'):
            os.mkdir(log_path+'Eraystemp')
        else:
            shutil.rmtree(log_path+'Eraystemp')
            os.mkdir(log_path+'Eraystemp')
# files=os.walk(contract_path)
# next(files)
# for addr,nll,bytecodeFiles in files:
#     print("Dealing with %s\n"%addr)
#     if not addr.startswith(contract_path+'0x'):
#         print("Not a contract folder")
#         continue
#     if not addr.split('/')[-1].startswith('0x'):
#         print("It is a 'temp' folder= =")
#         continue
#     count+=1
#     have_bytecode=False
#     for i in bytecodeFiles:
#         if i.endswith('forSecurify'):
#             print("====BYTECODE FOUND====")
#             input_file=open(addr+'/'+i,'r')
#             have_bytecode=True
#             break
#     if not have_bytecode:
#         raise BaseException('Bytecode not found in %s!'%addr)
#     line=input_file.read().strip()
#     line=line.split("0x")[1]
#     if " " in line:
#         line = line.split(" ")[1]
#     input_file.close()
#     addr=addr+'/'
#    print("oooooooooooooooooooo\n%s\noooooooooooooooooooo"%line)
        logger.removeHandler(fh)
        # Create a folder
        fh=logging.FileHandler(filename=log_path+'Eraystemp/Erays_log.txt',mode='a',encoding=None,delay=False)
        fh.setLevel(logging.ERROR)
        logger.addHandler(fh)
        with open(log_path+contract_file,'r') as f:
            line=f.read()
        try:
            erays_func(line,log_path+'Erays')
            count+=1
        except Exception as e:
            print(e)
        finally:
            bar.move()
            bar.log("Progressing:")
end_time = time.time()

print("Total processed contract amount:%d"%count)
print("Total process time:%d"%(end_time-start_time))
