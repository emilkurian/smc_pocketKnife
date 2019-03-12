#!/bin/bash

FILE1=$1
FILE2=$2

sudo sg_ses --descriptor=$FILE2 $FILE1 | grep "SAS address" > dump.txt 
sudo sed '1d' dump.txt > addr.txt
sudo awk '{print $3}' addr.txt > sasAddr.txt
rm dump.txt addr.txt
