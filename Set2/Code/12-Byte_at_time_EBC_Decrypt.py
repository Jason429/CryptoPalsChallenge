#! /usr/bin/python3

# 12 - Using Encryption Oracle
# You will only decrypt the first block.  This is to assume that all we have
# control over is inserting only at the start of the program.

# If this is the case, we then use the plain text from the first solved block
# to figure out the key.  Once that is done, we can decrypt the entire msg.

# If you have the ability to inject in the middle of the unknown string, then
# you can carry on the same way that you decrypted, else you don't know
# then answer.

from msg import AES
from base64 import b64decode
from random import randint


# Grab the unknown msg

unknown_string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
# Convert Msg (base64 to string)
unknown_string = b64decode(unknown_string)

# Generate random key to encrypt (You will be encrypting with AES-128 EBC)
random_key = bytearray()
for i in range(16):
    random_key.append(randint(0, 255))


a = AES.Oracle_Inject(unknown_string, random_key, b'', 'EBC')
# a.result is the final encryption with empty injection (what the system
# would normally do.
answer = a.result
# Feed bytes at beginning , eg. 'A' then 'AA' to find the size of the block
# Remember that padding will be placed if block is short (will be fixed
# multiple)

pad_size = 0
msg_size = len(a.result)
while msg_size == len(a.result):
    a._encrypt(b'A' * pad_size, a.org_msg, a.key)
    pad_size += 1
# Above adds padding until the size of result changes to identify padding
# of msg.


print("Suspected padding size is {}".format(pad_size))

# a.result still holds from the padding above.
# Next is to add block_size until it changes again.
# a.result keeps changing as a variable to the last operation.

block_size = 0
msg_size = len(a.result)
while msg_size == len(a.result):
    a._encrypt(b'A' * (block_size + pad_size), a.org_msg, a.key)
    block_size += 1
print("Cypher size is suspected to be {}".format(block_size))

# Change has happened again

if pad_size == block_size:
    print('Oops, there is no padding')
    pad_size = 0
# Above is if both pad_size and block_size is the same number, then that
# means there was no padding.

# Test for EBC (You did this last challenge)
# Set a.result with padding to test
a._encrypt(b'A' * (block_size * 2 + pad_size), a.org_msg, a.key)
# Pull answer from a.result and test
if a.testForEBC(a.result) == 'EBC':
    print("Encryption is in EBC"
          + "\nWe can decrypt.")
else:
    print("Sorry.  This won't work")
    print("This is a function for decrypting EBC.")

# *************************************************************
#
#  Thought. Inject one block and into second block.  If both blocks
#  are the same after encryption, you have verified that byte.
#
# ************************************************************

lead = b'A' * (block_size - 1)
known_answer = bytes()
b = bytes(range(256))
# Get length of original decrypt
a._encrypt(b'', a.org_msg, a.key)
org_len = len(a.result)
num_blocks = int(org_len / block_size)

# Below injects and then checks last bit.
for outer in range(block_size + 1):   # block_size increase to run to 16
    # This should go through everything in block
    # Inject dictionary then check msg

    # Below checks [lead(AAA... + known) + <bit>] +
    #              [lead(AAA... + known) + start of msg]
    # Size of start msg increases
    test = lead + known_answer
    for i in range(256):
        a._encrypt(test + b[i:i + 1] + lead, a.org_msg, a.key)
        if a.result[0:block_size] == a.result[block_size:2 * block_size]:
            known_answer = known_answer + b[i:i + 1]
            lead = lead[0:len(lead) - 1]
            print(lead, known_answer, flush=True)
            break
    # Once found, known_answer has byte appended and,
    #   lead is shortened by 1

    # Craft inject one byte short of block.  Build dictionary of last byte

# Take what you have decrypted and use that as an oracle to find missing byte
# Then test your first structure to the one you are testing

for blocks in range(1, int(num_blocks)):
    lead = b'A' * (block_size - 1)
    for outer in range(block_size + 1):
        for i in range(256):
            test = known_answer[-15:] + b[i:i + 1] + lead
            a._encrypt(test, a.org_msg, a.key)
            if a.result[0:block_size] == a.result[(block_size * blocks) + block_size:
                                                  ((block_size * blocks) + block_size + block_size)]:

                known_answer = known_answer + b[i:i + 1]
                lead = lead[0:len(lead) - 1]
                print(lead, known_answer, flush=True)
                break

print(known_answer.decode())
