#!/bin/bash

FILE1=$1

sudo lsscsi -stg | grep "$FILE1" > dump.txt 
sudo awk '{print $4}' dump.txt > logicName.txt
rm dump.txt
