#Get RPI serial number off of CPU -Jared
#The following "getserial()" function is referenced from: 
#https://www.raspberrypi-spy.co.uk/2012/09/getting-your-raspberry-pi-serial-number-using-python/
import http.client, os, sys

#################################
#			Step One			#
#################################

#Gets serial number from rpi
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

#################################
#			Step Two			#
#################################

#Tell the system that this RPI is Active
conn = http.client.HTTPConnection("adsanvar.pythonanywhere.com")
conn.request("GET", '/setActive/'+rpi_serial)
r1 = conn.getresponse()
print(r1.read())

#################################
#			Step Three			#
#################################

# Collect the IP Address and Start the Eddystone Beacon

ip = sys.argv[1]

#Splits the IP address string into a word array
wordString = ip.split('.')

#Initializes all of the arrays
octet1array = []
octet2array = []
octet3array = []
octet4array = []
octet1hex = []
octet2hex = []
octet3hex = []
octet4hex = []

#Changed to stack for better performance -Adrian
#look at eddystone datum for more details on the bytes
p_stack = []
p_stack.append('0x08')
p_stack.append('0x0008')
p_stack.append('0') #length of remaining bytes
p_stack.append('02')
p_stack.append('01')
p_stack.append('06')
p_stack.append('03')
p_stack.append('03')
p_stack.append('aa')
p_stack.append('fe')
p_stack.append('0') #length of remaining bytes
p_stack.append('16')
p_stack.append('aa')
p_stack.append('fe')
p_stack.append('10')
p_stack.append('F4')
p_stack.append('02')

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
#modified to add to overall stack -Adrian
for k in octet1hex:
	"{:0>2}".format(k)
	p_stack.append(k[2:])

p_stack.append('2e')

for k in octet2hex:
	"{:0>2}".format(k)
	p_stack.append(k[2:])

p_stack.append('2e')

for k in octet3hex:
	"{:0>2}".format(k)
	p_stack.append(k[2:])

p_stack.append('2e')

for k in octet4hex:
	"{:0>2}".format(k)
	p_stack.append(k[2:])

#Sets the values of the lengths in the Eddystone Datum
#converts length of stack to hex and sets it to the index
#len -> hex -> remove first two chars '0x'
p_stack[2] = hex(len(p_stack[3:]))[2:]
p_stack[10] = hex(len(p_stack[11:]))[2:]

#Adds remaining 00's to stack -Adrian
for i in range(len(p_stack), 34):
    p_stack.append('00')

payload = ' '.join(p_stack)

#Starts the Eddystone Beacon -Adrian
os.system('sudo hcitool -i hci0 cmd ' + payload)
os.system('sudo hcitool -i hci0 cmd 0x08 0x0006 A0 00 A0 00 03 00 00 00 00 00 00 00 00 07 00')
os.system('sudo hcitool -i hci0 cmd 0x08 0x000a 01')