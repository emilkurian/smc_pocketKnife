#!/bin/bash

sudo lsscsi -t | grep sas | grep disk > /home/joshua/pocketKnife/dump.txt
awk '{print $3," "$4}' /home/joshua/pocketKnife/dump.txt > /home/joshua/pocketKnife/sastemp.txt
sed 's/^....//' /home/joshua/pocketKnife/sastemp.txt > /home/joshua/pocketKnife/sasDict.txt
rm /home/joshua/pocketKnife/dump.txt /home/joshua/pocketKnife/sastemp.txt
