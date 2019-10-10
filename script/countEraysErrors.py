import os 
import sys
if len(sys.argv)>1:
	path=sys.argv[1]
else:
	path='/home/iimp/Programs/CODING/top100_contract_run/'
folders=os.listdir(path)
i=0
for folder in folders:
	if not '0x' in folder:
		continue
# #===================Erays==================================
	files=os.listdir(path+folder+'/Eraystemp/')
	print(files)
	if len(files)>1:
		i+=1
print("success rate:%d"%(i))
# #===========================================================
# 	if not os.path.exists(path+folder+'/Vandal/'):
# 		print(folder)
# 	else:
# 		files=os.listdir(path+folder+'/Vandal/')
# 		if 'cfg.dot' in files:
# 			i+=1
# 		else:
# 			with open(path+folder+'/Vandal/Vandal_log.txt') as f:
# 				a=f.read()
# 				print(a)
# print("success rate:%d"%(i))
# =============================================================
#	files=os.listdir(path+folder)
#	if 'OyenteSucessed' in files:
#		print(folder)
#		i+=1
#print("success rate:%d"%(i))
# # ===========================================================
# 	files=os.listdir(path+folder+'/Mythril/')
# 	with open(path+folder+'/Mythril/Mythril_log.txt') as f:
# 		a=f.read()
# 		if a:
# 			print(a)
# 		else:
# 			i+=1
# print("success rate:%d"%(i))
# # #======================Octopus============================
# 	files=os.listdir(path+folder+'/Octopus/')
# 	cnt=0
# 	for file in files:
# 		if file=='Octo_log.txt':
# 			continue
# 		cnt+=1
# 	if cnt!=0:
# 		i+=1
# print("success rate:%d"%(i))
#=======================Securify=================================
# 	files=os.listdir(path+folder+'/Securify/')
# 	cnt=0
# 	for file in files:
# 		if file=='output.json':
# 			cnt+=1
# 	if cnt!=0:
# 		i+=1
# print("success rate:%d"%(i))
# =============================================================
# files = os.listdir(path + folder)
# noBytecode=0
# if not folder+'.forSecurify' in files:
# 	noBytecode+=1
# print(i)
