import os
import sys
import psycopg2
if len(sys.argv)>1:
	path=sys.argv[1]
else:
	path='/home/iimp/Programs/CODING/top100_contract_run/'
if not os.path.exists(path+'testTx'):
	os.mkdir(path+'testTx')
if not os.path.exists(path+'hashCodes'):
	os.mkdir(path+'hashCodes')
conn= psycopg2.connect(database="blockchain", user="gpadmin", password="123456", host="127.0.0.1", port="5432")#server
cursor=conn.cursor()
contracts=os.listdir(path)
folders=('PUSHADD','JUMPDEST','SWARM','SIGNATURE','START')



for contract in contracts:
	if not contract.startswith('0x'):
		continue
	#===============GetTxs================
	sql="select hash from transaction where to_address=lower('%s') and block_number<7122500 order by hash limit 10000;"%contract
	cursor.execute(sql)
	txhashes=cursor.fetchall()
	with open(path+'testTx/'+contract,'w') as w:
		for txhash in txhashes:
			w.write(txhash[0]+'\n')
	#==============generateCode============
	with open(path+contract+'/'+contract+'.forSecurify','r') as f:
		ocode=f.read()
	with open(path+'hashCodes/'+contract,'w') as w:
		s=contract+':'+ocode
		w.write(s)
	for folder in folders:
		with open(path+folder+'/'+contract+'/'+contract+'.forSecurify','r') as f:
			mcode=f.read()
		with open(path+'hashCodes/'+contract+'.'+folder,'w') as w:
			s=contract+':'+mcode
			w.write(s)

