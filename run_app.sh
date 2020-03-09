#!/bin/bash

## This should grab the IP address of the RPi and display - Heath
RPiIP=$(hostname -I) || true
if [ "$RPiIP" ]; then
  #printf "My IP address is %s\n" "$RPiIP"

python test.py "$RPiIP"

#Eddystone protocol
sudo hcitool -i hci0 cmd 0x08 0x0008 1a 02 01 06 03 03 aa fe 12 16 aa fe 10 00 02 31 37 32 2e 32 30 2e 31 30 2e 33 3a 00 00 00 00 00
#sudo hcitool -i hci0 cmd 0x08 0x0008 1c 02 01 06 03 03 aa fe 14 16 aa fe 10 F4 02 31 39 32 2e 31 36 38 2e 31 2e 31 30 33 3a 00 00 00
#frequency of advertisements
sudo hcitool -i hci0 cmd 0x08 0x0006 A0 00 A0 00 03 00 00 00 00 00 00 00 00 07 00 
#some with eddystone
sudo hcitool -i hci0 cmd 0x08 0x000a 01

export FLASK_APP=~/Documents/CSI4999/SmartLock
export FLASK_ENV=development
export DEBUG=1
export FLASK_RUN_PORT=5000
printenv
flask run -h 172.20.10.3
#flask run -h 192.168.1.103

fi
