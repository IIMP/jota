import json
import psycopg2
import os
conn = psycopg2.connect(database = "ethereum",user="gpadmin",password="123456",host="192.168.1.2",port="5432")

path = '/root/2017Dataset/'



if not os.path.exists(path):
	os.mkdir(path)
with open('/root/2017Dataset.json','r') as f:
	contracts = json.load(f)
cnt = 0
for contract in contracts:
	addr = contract[0]
	cursor = conn.cursor()
	sql = "select code from code where address =\'%s\'"%addr
	cursor.execute(sql)
	try:
		code = cursor.fetchall()[0][0]
		contract_path = '%s%02d-%s/'%(path,cnt,addr)
		if not os.path.exists(contract_path):
			os.mkdir(contract_path)
	except Exception as e:
		print(e)
		continue
	if code.startswith('0x'):
		code = code[2:]
	with open(contract_path+'%02d-%s.bytecode'%(cnt,addr),'w') as w:
		w.write(code)
	cursor.close()
	cnt+=1
		
	
