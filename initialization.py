#Get RPI serial number off of CPU -Jared
#The following "getserial()" function is referenced from: 
#https://www.raspberrypi-spy.co.uk/2012/09/getting-your-raspberry-pi-serial-number-using-python/
import http.client

def getserial():
  serialNum = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        serialNum = line[10:26]
    f.close()
  except:
    serialNum = "ERROR000000000"
 
  return serialNum

#Set the serial number to a variable
rpi_serial = getserial()
print(rpi_serial)

# conn = http.client.HTTPConnection("localhost",5000)
# conn.request("GET", '/setActive/124')
# r1 = conn.getresponse()
# print(r1.read())