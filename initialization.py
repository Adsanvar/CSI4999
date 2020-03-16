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

#000000009ae4879e

conn = http.client.HTTPConnection("adsanvar.pythonanywhere.com", 80)
conn.request("GET", '/setActive/'+rpi_serial)
r1 = conn.getresponse()
print(r1.read())

#Jared
import string

RpiIP = '172.20.10.2'

#Splits the IP address string into a word array
wordString = RpiIP.split('.')

#Initializes all of the arrays
octet1array = []
octet2array = []
octet3array = []
octet4array = []
octet1hex = []
octet2hex = []
octet3hex = []
octet4hex = []
formattedOct1 = []
formattedOct2 = []
formattedOct3 = []
formattedOct4 = []

#Breaks the wordstring array into separate arrays based on the IP address octets
octet1 = wordString[0]
for i in octet1:
	octet1array.append(i)
octet2 = wordString[1]
for i in octet2:
	octet2array.append(i)
octet3 = wordString[2]
for i in octet3:
	octet3array.append(i)
octet4 = wordString[3]
for i in octet4:
	octet4array.append(i)

#Converts the octet based array objects into ASCII and then into hexadecimal
for j in octet1array:
	octet1hex.append(hex(ord(j)))
for j in octet2array:
	octet2hex.append(hex(ord(j)))
for j in octet3array:
	octet3hex.append(hex(ord(j)))
for j in octet4array:
	octet4hex.append(hex(ord(j)))

#Formats the hex arrays by removing the "0x" prefix
for k in octet1hex:
	"{:0>2}".format(k)
	formattedOct1.append(k[2:])
for k in octet2hex:
	"{:0>2}".format(k)
	formattedOct2.append(k[2:])
for k in octet3hex:
	"{:0>2}".format(k)
	formattedOct3.append(k[2:])
for k in octet4hex:
	"{:0>2}".format(k)
	formattedOct4.append(k[2:])

#Joins each object within the array to form a complete string
octBytesA = ' '.join(formattedOct1)
octBytesB = ' '.join(formattedOct2)
octBytesC = ' '.join(formattedOct3)
octBytesD = ' '.join(formattedOct4)

#Creates a string using static payload values for the packet header which should not change
#and dynamic values for the variable rpi IP address
payload = '0x08 0x0008 18 02 01 06 03 03 aa fe 10 16 aa fe 10 00 ' + octBytesA + ' 2e ' + octBytesB + ' 2e ' + octBytesC + ' 2e ' + octBytesD

#Creates a padding of payload bytes at the end of the beacon packet
while len(payload) < 107:
	payload = payload + ' 00'

print(payload)