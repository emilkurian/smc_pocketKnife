#!/bin/bash

FILE1=$1

sudo sg_ses --page=ED $FILE1 | grep Slot > dump.txt 
awk '{print $4}' dump.txt > slots.txt
rm dump.txt
