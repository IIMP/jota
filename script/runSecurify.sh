#!/bin/sh
find $1 -name "*bytecode" | parallel timeout 300 java -jar /root/securify/build/libs/securify.jar -fh {} --livestatusfile {//}/Securify/result.json
