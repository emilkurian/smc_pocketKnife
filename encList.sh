#!/bin/bash

lsscsi -g -t | grep encl > dump.txt 
awk '{print $5}' dump.txt > exp.txt
rm dump.txt
