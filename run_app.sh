#!/bin/bash

## This should grab the IP address of the RPi and display - Heath
RpiIp=$(hostname -I)

stringarray=($RpiIp)
ip=${stringarray[0]}

python3 ~/Documents/CSI4999/initialization.py "$ip"

# datum=$(python test.py "$ip" 2>&1 > /dev/null)

#Eddystone protocol
# sudo hcitool -i hci0 cmd 0x08 0x0008 1a 02 01 06 03 03 aa fe 12 16 aa fe 10 00 02 31 37 32 2e 32 30 2e 31 30 2e 33 3a 00 00 00 00 00
# #frequency of advertisements
# sudo hcitool -i hci0 cmd 0x08 0x0006 A0 00 A0 00 03 00 00 00 00 00 00 00 00 07 00 
# #some with eddystone
# sudo hcitool -i hci0 cmd 0x08 0x000a 01

python3 ~/Documents/CSI4999/startBrowser.py "$ip"

export FLASK_APP=~/Documents/CSI4999/SmartLock
export FLASK_ENV=production
export DEBUG=0
export FLASK_RUN_PORT=5000
#printenv
flask run -h $ip