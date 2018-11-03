#!/bin/bash

PWD=$(pwd)
echo "$PWD"

lsscsi -g > /home/joshua/pocketKnife/dump.txt 
awk '{print $4"\t"$6"\t"$7"\t"$8}' /home/joshua/pocketKnife/dump.txt > /home/joshua/pocketKnife/data.txt
column -t /home/joshua/pocketKnife/data.txt > /home/joshua/pocketKnife/drives.txt
rm /home/joshua/pocketKnife/data.txt /home/joshua/pocketKnife/dump.txt







