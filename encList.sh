#!/bin/bash

lsscsi -g -t | grep encl > /home/joshua/pocketKnife/dump.txt 
awk '{print $5}' /home/joshua/pocketKnife/dump.txt > /home/joshua/pocketKnife/exp.txt
rm /home/joshua/pocketKnife/dump.txt
