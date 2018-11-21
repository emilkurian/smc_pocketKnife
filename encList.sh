#!/bin/bash

lsscsi -g -t | grep encl > /home/joshua/pocketKnife/dump.txt 
awk '{print $5}' /home/joshua/pocketKnife/dump.txt > exp.txt
rm /home/joshua/pocketKnife/dump.txt
