#!/bin/sh

#waits for 15s while pi connects to internet
timer=15
echo "Application Will Start In: "
while [$timer != 0]
do
    echo $timer
    sleep 1
    timer=`expr $timer - 1`
done

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

#updates the boot up to run the scrip automatically next time
#sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
sudo grep -qxF '@lxterminal -e "~/Destkop/run_app.sh"'  /etc/xdg/lxsession/LXDE-pi/autostart || echo '@lxterminal -e "~/Destkop/run_app.sh"' >> /etc/xdg/lxsession/LXDE-pi/autostart

export IP_VAR="$ip"
export FLASK_APP=~/Documents/CSI4999/SmartLock
export FLASK_ENV=development
export DEBUG=1
export FLASK_RUN_PORT=5000
#printenv
flask run -h $ip