#!/bin/bash

sudo lsscsi -t | grep sas | grep disk > dump.txt
awk '{print $3," "$4}' dump.txt > sastemp.txt
sed 's/^....//' sastemp.txt > sasDict.txt
rm dump.txt sastemp.txt
