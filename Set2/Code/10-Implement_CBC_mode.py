#! /usr/bin/python3
import base64

import msg.AES as AES


# from msg import padding

# Hardcoded key
key = b'YELLOW SUBMARINE'

# HARDCODED file
f = open('/home/jason/Projects/Crypto/cryptopals.com/2/cryptopals.com/static/challenge-data/10.txt', 'r')

# Copy msg to memory in whole and remove newline
original = ''
for i in f:
    original += i.strip('\n')
f.close()

# Now convert base64 to bytes
original = base64.b64decode(original)
block_size_bits = 128

AES._sizetest(original, 16)
iv = bytearray(16)
iv = bytearray([26 for x in range(16)])
result = AES.decryptMsgCBC(original, key, iv, makeblock=128)
print(result.decode())
