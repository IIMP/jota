import psycopg2
import os
conn = psycopg2.connect(database = "ethereum",user = "gpadmin",password = "123456",host = "192.168.1.2",port = "5432")
with open('/root/2019Dapps.txt','r') as f:
	lines = f.read().split('\n')[:-1]
for line in lines:
	sql = "select code from code where address = '%s';"%line
	print(sql)
	cursor = conn.cursor()
	cursor.execute(sql)
	code = cursor.fetchone()
	if not code:
		continue
	else:
		code = code[0]
	if code.startswith('0x'):
		code = code[2:]
	if not os.path.exists('/root/2019Dapps/%s'%line):
		os.mkdir('/root/2019Dapps/%s'%line)
	with open('/root/2019Dapps/%s/%s.bytecode'%(line,line),'w') as f:
		f.write(code)
	cursor.close()
