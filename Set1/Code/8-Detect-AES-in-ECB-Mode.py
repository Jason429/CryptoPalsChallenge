#! /usr/bin/python3

from msg import AES

# create holding list variable (for suspected ECB lines)
suspect = []
length = 0
testlist = []
#
f = open('/home/jason/Projects/Crypto/Set1/detectAES.txt','r')
for line in f:
    # strip new line
    line = line.rstrip('\n')
# check length of line
    length = len(line)
# break it up into 16 byte chuncks
    for num in range(0,len(line),16):
        testlist.append(line[num:num+16])
    setlist = set(testlist)
# check is any chuncks are the same
    if len(setlist) != len(testlist):
        suspect.append(line)
    # Reset testlist for next iteration
    testlist = []

print(suspect)

key = b'YELLOW SUBMARINE'

# convert suspect to bytearray
msg = []
# Below assumes one result
for i in range(0,len(suspect[0]),2):
    msg.append(eval('0x'+str(suspect[0][i:i+2])))

msgbytes = bytearray(msg)
result = AES.decryptMsg(msgbytes,key)
