#! /usr/bin/python3

import base64
from msg import AES


cipher_block_size = 128
# HARDCODED KEY
key =b'YELLOW SUBMARINE'

# HARDCODED file
f = open('/home/jason/Projects/Crypto/Set1/AESFile.txt','r')

# Copy msg to memory in whole and remove newline
original = ''
for i in f:
    original += i.strip('\n')
f.close()
# Now convert base64 to bytes
original = base64.b64decode(original)
block_size_bits = 128

# Check if padding is required
if len(original) % 16 != 0:
    print('This is not a perfect group of 16')
    print('Padding is required')
    print('Quiting ....')
    quit()

# Initialize final decrypted message
decrypted_msg = bytearray()
# Loop break number of times required
for start_of_next_block in range(0,len(original),16):
    # print(start_of_next_block)
# Break original msg into 16 byte block
    msg = AES.make128block(original[start_of_next_block:(start_of_next_block + 16)])
    keyblock = AES.make128block(key)
                           
# Create block for key

# Send to be decrypted
    result = AES.decryptAES(msg,keyblock)
    result = AES.deBlock(result)
    decrypted_msg.extend(result)
# Take result and place in decrypt msg (in order)
print(decrypted_msg.decode())



