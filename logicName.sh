#!/bin/bash

FILE1=$1

sudo lsscsi -stg | grep "$FILE1" > /home/joshua/pocketKnife/dump.txt 
awk '{print $4}' /home/joshua/pocketKnife/dump.txt > logicName.txt
rm /home/joshua/pocketKnife/dump.txt
