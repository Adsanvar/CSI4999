import sys

print("HELLO FROM PYTHON SCRIPT. ", sys.argv[1])

#Jared

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