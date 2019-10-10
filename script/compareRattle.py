import os
import sys
target_path = sys.argv[1]
#ori_path = '/root/2019Dapps/contracts/'
ori_path = '/root/test2019/contracts/'
successAttack = 0
type1 = []
type2 = []
type3 = []
type4 = []
folders = os.listdir(target_path)
for folder in folders:
	if not '0x' in folder:
		continue
	if not os.path.exists(ori_path+folder+'/Rattle/output'):
		type1.append(folder)
		continue
	files1 = os.listdir(ori_path+folder+'/Rattle/output')
	if files1 == []:
		type1.append(folder)
		continue
	if not os.path.exists(target_path+folder+'/Rattle/output'):
		type2.append(folder)
		continue
	files2 = os.listdir(target_path+folder+'/Rattle/output')
	if files2 == []:
		type2.append(folder)
		continue
	if '_fallthrough.png' in files1:
		files1.remove('_fallthrough.png')
	if '_fallthrough.png' in files2:
		files2.remove('_fallthrough.png')
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
