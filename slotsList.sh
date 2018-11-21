#!/bin/bash

FILE1=$1

sudo sg_ses --page=ED $FILE1 | grep Slot > /home/joshua/pocketKnife/dump.txt 
awk '{print $4}' /home/joshua/pocketKnife/dump.txt > slots.txt
rm /home/joshua/pocketKnife/dump.txt
