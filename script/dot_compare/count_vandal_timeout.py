import os
import sys
contracts = os.listdir(sys.argv[1])
cnt = 0
for contract in contracts:
	if not '0x' in contract:
		continue
	filep = sys.argv[1]+'/'+contract+'/Vandal/Vandal_log.txt'
	if not os.path.exists(filep):
		continue
	with open(filep,'r') as f:
		lines = f.read()
		if '300s' in lines:
			cnt += 1
		else:
			print(lines)
print("Timeout: ",cnt)

