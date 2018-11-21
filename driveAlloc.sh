#!/bin/bash

PWD=$(pwd)
echo "$PWD"

lsscsi -g -t | grep sas | grep disk > /home/joshua/pocketKnife/dump.txt 
awk '{print $3","$4","$5}' /home/joshua/pocketKnife/dump.txt > drives.txt
rm /home/joshua/pocketKnife/dump.txt
