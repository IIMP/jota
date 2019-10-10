import os
import csv
path='/home/iimp/Programs/CODING/top100_contract_run/'
csv_file='top100.csv'
contracts={}
with open(path+csv_file,'r') as f:
    top100_reader=csv.reader(f)
    for row in top100_reader:
        addr,bytecode=row[0].split('\t')
        #print("%s has bytecode:%s"%(addr,bytecode))
        contracts[addr]=bytecode
for addr,bytecode in contracts.items():
    os.makedirs(path+addr)
    with open(path+addr+'/'+addr+'.bytecode','w') as w:
        w.write(bytecode)
