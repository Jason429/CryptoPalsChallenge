#!/usr/bin/python3

import base64
from sys import getdefaultencoding
from msg.convert import convert_binary as cb
#from random import choice
from msg.defs import hamming_distance_test
#from msg.defs import skip_gen
#from msg.defs import insert_gen
#from msg.defs import DCRYPT
#from msg.defs import character_check
#from msg.defs import englishtest
#from msg.defs import xor as func_xor
from msg.defs import single  # main xor test with language check
from msg.defs import xor_iter

# Variables
maxkeysize = 80   # max keysize iteration
ENCODING = getdefaultencoding()
maxhammingiter = 4

keysizerange = range(2, maxkeysize + 1)
keysizes = []
for i in keysizerange:
    keysizes.append(i)

f = open('/home/jason/Projects/Crypto/Set1/It\'sOnFile.txt', 'r')

# Copy msg to memory in whole and remove newline
original = ''
for i in f:
    original += i.strip('\n')
f.close()
# Now convert base64 to bytes
original = base64.b64decode(original)
boriginal = cb(original, 'bit8')
h_test, best_val = hamming_distance_test(boriginal, maxkeysize,
                                         maxhammingiter)

# With likely answer of keysize, testkeysize
# Add code to allow other test
testkeysize = 0
for i in h_test.items():
    if i[1] == best_val[0]:
        testkeysize = i[0]

# List best testkeys to try and give option to attempt
# different xor size
keysize_order = []
for i in h_test:
    keysize_order.append((h_test[i], i))
keysize_order.sort()

for i in range(0, 5):
    print("Keysize: " + str(keysize_order[i][1]) +
          "  Score : " + str(keysize_order[i][0]))
print("Lower is better ---------------")
keysizetest = input("Select the keysize (bits) to test for message [" + str(keysize_order[0][1])
                    + "] ")
if keysizetest == '':
    keysizetest = keysize_order[0][1]
try:
    keysizetest = int(keysizetest)
    if testkeysize == 1 or testkeysize == 0:
        print("One or zero received.")
        print("This won't work......")
        print("Exiting .....")
        quit()
except:
    print("This needs to be an int value")
    print("Could not translate to int.  Failure")
    print("Exiting .........."
          )
    quit()

# Now that you probably know the KEYSIZE
#: break the ciphertext into blocks of KEYSIZE length.
# numblockbytes = number of bytes before iterates
numblockbytes = int(int(keysizetest) / 8)
# blocks will hold segments to maniplate
blocks = {}
encryptor = {}
answer = {}
# create dictionary of original blocks and manipulation
for i in range(0, numblockbytes):
    blocks[i] = []
    encryptor[i] = []
    answer[i] = []
# parse msg into dictionary
count = 0
for i in original:
    blocks[count].append(i)
    count += 1
    if count == numblockbytes:
        count = 0

# blocks now holds the message broken up by groupings

#  Solve each block as if it was single-character XOR.
# You already have code to do this

xor_list = xor_iter()
temp = {}
for key in blocks.keys():
    b_array = bytearray(blocks[key])
    temp = single(b_array, xor_list, char_weight=1, eng_weight=100)
    for i in temp.keys():
        encryptor[key].append(i)
        answer[key].append(temp[i][1])

endmsg = bytearray()
endxor = bytearray()
temp = []
for i in range(0, numblockbytes):
    for j in encryptor[i][0]:
        temp.append(j)
    endxor.append(temp[0])
    temp = []

try:
    for i in range(len(answer[0][0])):
        for key in range(len(answer)):
            endmsg.append(answer[key][0][i])
except IndexError:
    pass

print(endxor)
print('**************************************')
# print(endmsg) # Comment out to remove raw
print(endmsg.decode(encoding='utf-8'))
