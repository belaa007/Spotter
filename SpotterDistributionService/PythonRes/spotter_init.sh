﻿#!/bin/bash

#chdir
cd /home/elteple_spotter

#fping install
sudo yum -y --nogpgcheck install fping

#get-pip download
wget -N https://raw.github.com/pypa/pip/master/contrib/get-pip.py

#pip install
sudo python get-pip.py

#bottle install
sudo pip install bottle

#cherrypy install
sudo pip install cherrypy

#download spotter
wget -N https://raw.github.com/belaa007/Spotter/master/SpotterDistributionService/PythonRes/spotter.py

#download config
rm config.txt
wget https://raw.github.com/belaa007/Spotter/master/SpotterDistributionService/PythonRes/config.txt

#get hostname
hostname >> config.txt

#get ip
curl http://checkip.dyndns.org | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' >> config.txt

#start spotter
python spotter.py >> spotter.log
