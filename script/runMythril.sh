#!/bin/sh
contract_path=$1
echo $contract_path
for i in $(find $contract_path -name "*.bytecode");
do
	echo $i
	pppp=${i%/*bytecode}
	mkdir $pppp/Mythril/
	myth -f $i --execution-timeout 300 -g $pppp/Mythril/graph.html --bin-runtime >$pppp/Mythril/log 2>$pppp/Mythril/errorlog
done
