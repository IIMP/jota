import os
import sys
i=0
success=0
target_path=sys.argv[1]
if not target_path.endswith('/'):
	target_path+='/'
path='/root/2017Dataset/contracts/'
folders=os.listdir(path)
type1=[]#Failed without modification
type2=[]#Failed after modification
type3=[]#Completed after modification with wrong results
type4=[]#Totally successful
for folder in folders:
	if not '0x' in folder:
		continue
	if not os.path.exists(path+folder+'/Eraystemp/'):
		type1.append(folder)
		continue
	origin_files=os.listdir(path+folder+'/Eraystemp/')
	if origin_files == ['Erays_log.txt']:
		type1.append(folder)
		continue
	if not os.path.exists(target_path+folder+'/Eraystemp/'):
		type2.append(folder)
		continue
	target_files=os.listdir(target_path+folder+'/Eraystemp/')
	if target_files ==['Erays_log.txt']:
		type2.append(folder)
		continue
	if target_files != origin_files:
		type3.append(folder)
	else:
		type4.append(folder)
print("Type1:",len(type1))
print("Type2:",len(type2))
print("Type3:",len(type3))
print("Type4:",len(type4))
print("=================Type1=========================\n",type1)
print("=================Type2=========================\n",type2)
print("=================Type3=========================\n",type3)
print("=================Type4=========================\n",type4)
