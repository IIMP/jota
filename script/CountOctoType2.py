import os
import sys
path = '/root/2017Dataset/'
target = sys.argv[1]
folders = os.listdir(path+target)
timeoutCount = 0
for folder in folders:
    if not '0x' in folder:
        continue
    with open(path+target+'/'+folder+'/Octopus/Octo_log.txt','r') as f:
        lines = f.read()
        if lines.replace('\r|\n','') == '':
            continue
        if '300s' in lines:
            timeoutCount += 1
            print(folder)
print("timeoutCount: ",timeoutCount)
