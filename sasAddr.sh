#!/bin/bash

FILE1=$1
FILE2=$2

sudo sg_ses --descriptor=$FILE2 $FILE1 | grep "SAS address" > /home/joshua/pocketKnife/dump.txt 
sed '1d' /home/joshua/pocketKnife/dump.txt > /home/joshua/pocketKnife/addr.txt
awk '{print $3}' /home/joshua/pocketKnife/addr.txt > sasAddr.txt
rm /home/joshua/pocketKnife/dump.txt /home/joshua/pocketKnife/addr.txt
