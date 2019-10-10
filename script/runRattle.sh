#/bin/sh
for i in $(find $1 -name "*.bytecode");
do 
	cat $i | xxd -r -ps > $i.rattle;
	echo $i.rattle
done

for i in $(find $1 -name "*.rattle");
do
	mkdir ${i%/*rattle}/Rattle/
	timeout 300 python3 /root/rattle/rattle-cli.py --input $i --cfg ${i%/*rattle}/Rattle/
done
