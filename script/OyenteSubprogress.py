import sys
sys.path.append('/home/iimp/repository/oyente-master/oyente/')
from oyente import *

if __name__ == '__main__':
	source = sys.argv[1]
	result = build_cfg(source)
	print(result)
	exit(0)
