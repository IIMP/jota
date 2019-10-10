import os
import sys
ori_path = '/root/2017Dataset/contracts/'
path = sys.argv[1]
folders = os.listdir(path)
AttackSuccess = 0
type1=[]
type2=[]
type3=[]
type4=[]
for folder in folders:
	if not '0x' in folder:
		continue
	if not os.path.exists(ori_path+folder+'/Vandal'):
		type1.append(folder)
		continue
	files1 = os.listdir(ori_path+folder+'/Vandal/')
	if files1 == ['Vandal_log.txt']:
		type1.append(folder)
		continue
	if not os.path.exists(path+folder+'/Vandal'):
		type2.append(folder)
		continue
	files2 = os.listdir(path+folder+'/Vandal')
	if files2 == ['Vandal_log.txt']:
		type2.append(folder)
		continue
	if files1 != files2:
		type3.append(folder)
		continue
	if files1 == files2:
		type4.append(folder)
print("Type1:",len(type1))
print("Type2:",len(type2))
print("Type3:",len(type3))
print("Type4:",len(type4))
print("=================Type1=========================\n",type1)
print("=================Type2=========================\n",type2)
print("=================Type3=========================\n",type3)
print("=================Type4=========================\n",type4)
