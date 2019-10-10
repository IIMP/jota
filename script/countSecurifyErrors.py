import os
import sys
path = sys.argv[1]
folders = os.listdir(path)
error_cnt = 0
for folder in folders:
	if not '0x' in folder:
		continue
	if not os.path.exists(path+folder+'/Securify/output.json'):
		error_cnt += 1
		continue
	if not os.path.exists(path+folder+'/Securify/Securify_log.txt'):
		print("No logs found!")
		error_cnt += 1
		continue
	with open(path+folder+'/Securify/Securify_log.txt','r') as f:
		lines = f.read()
	if lines:
		print(lines)
		print(folder)
		error_cnt += 1
print("ErrorRate:",error_cnt)
