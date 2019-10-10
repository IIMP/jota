import psycopg2
import json
conn = psycopg2.connect(database = "ethereum",user="gpadmin",password="123456",host = "192.168.1.2",port = "5432")
cursor = conn.cursor()
sql = "select code.address,count(*) from transaction,code where transaction.to_address = code.address and transaction.block_number between 2910455 and 4799998 group by code.address order by count(*) desc limit 100;"
cursor.execute(sql)
tmp = cursor.fetchall()
with open('/root/2017Dataset.json','w') as f:
	json.dump(tmp,f)
