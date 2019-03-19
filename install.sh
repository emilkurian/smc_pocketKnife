#!/bin/bash

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install python3-pip git -y
pip3 install npyscreen
wget "sg.danny.cz/sg/p/sg3-utils_1.44-0.1_amd64.deb"
wget "sg.danny.cz/sg/p/libsgutils2-2_1.44-0.1_amd64.deb"
sudo dpkg -i libsgutils2-2_1.44-0.1_amd64.deb
sudo dpkg -i sg3-utils_1.44-0.1_amd64.deb

rm libsgutils2-2_1.44-0.1_amd64.deb sg3-utils_1.44-0.1_amd64.deb

echo "Packages installed"
