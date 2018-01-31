#!/usr/bin/python3

# 14 - Byte-at-a-time ECB decryption (Harder)

# Take your oracle function from #12. Now generate a random count of random
# bytes and prepend this string to every plaintext. You are now doing:

# AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)

# Same goal: decrypt the target-bytes. 

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
    random_key.append(randint(0,255))

# Generate a random pre-pend of bytes

pre = bytearray()
for i in range(randint(0,255)):
    pre.append(randint(0,255))

# Inject is using bytes or bytearray for message injection

a = AES.Oracle_Inject(pre + unknown_string, random_key, b'', 'EBC')

# a.result is the final encryption with empty injection (what the system would normally do.

answer = a.result

# A little monkey patching to keep unknown_string

a.unknown_string = unknown_string

# Identify pad size

pad_size = 0
msg_size = len(a.result)
while msg_size == len(a.result):
    pad_size += 1
    a._encrypt(pre + (b'A' * pad_size), a.unknown_string, a.key)

pad_size -= 1  # Once it changes the msg does padding show.
#                This is why we subtract 1

print("Suspected padding size is {}".format(pad_size))

# Identify block size

block_size = 0
msg_size = len(a.result)
while msg_size == len(a.result):
    block_size += 1
    a._encrypt(pre + (b'A' * pad_size) + (b'A' * block_size), a.unknown_string, a.key)

block_size -=1 # Same as padding issue

# Check if padding was required

if pad_size == block_size:
    print('Oops, there was no padding!\nContinuing')
    pad_size = 0

# Before we test for EBC mode, we need to make sure that the random
#   prefix is in place.  We don't care about padding here.

# block_size - 1 is used because we don't know how large the prepend is.

test_inject = b"A" * (block_size * 2) + b"A" * (block_size - 1)

# Test for EBC mode.  Factor in the random prefixed bytes

a._encrypt(pre + test_inject, a.unknown_string, a.key)

# Pull answer from a.result and test
# Exit if it is not an CBC.

if a.testForEBC(a.result) == 'EBC':
    print("Encryption is in EBC\nWe can decrypt.")
else:
    print("Sorry.  This won't work.")
    print("This is a function that only decrypts EBC.")
    print("Exiting .........\n")
    print("Block size {}".format(block_size))
    print("Padding size {}".format(pad_size))
    quit()


print("Block size {}".format(block_size))
print("Padding size at end of msg is {}".format(pad_size))
print("Inject block is {}".format(a.inject_loc_block))
print("Len of pre % 16 is {}".format(len(pre) % 16))

# Find padding.  If correct, the padding plus block_size *2 will
#   still pass the EBC test.

ibstart = a.inject_loc_block * block_size


pre_pad = 0
for i in range(0,block_size):
    test_inject = (b"A" * (block_size * 2)) + (b"A" * i)
    a._encrypt(pre + test_inject, a.unknown_string, a.key)
    if a.result[ibstart:ibstart + block_size] == \
       a.result[ibstart + block_size:ibstart + (2 * block_size)]:
        pre_pad = i
        break

print("Pre_padding required is {}".format(pre_pad))    
    
if a.testForEBC(a.result) == 'EBC':
    print("The padding was correct!")
else:
    print("No joy.  The padding idea didn't work.\n\n")

# Find which block we are injecting into.

a.locationEBC(a.result, block_size) # This goes into a.EBCBlock
print("a.EBCBlock is ", a.EBCBlock)
input("Pause")

known_answer = bytes()
b = bytes(range(256)) # Set of bytes

# Find the length of the target msg without the prepend
# Use this to figure out how many iterations you will need to go through

num_blocks = int(len(a.result[a.EBCBlock * block_size:]) // block_size) - 2

print("Injection block is located at {}".format(a.EBCBlock))

finished_list = []
for block_id in range (1, num_blocks + 1):
    start_pt = a.EBCBlock * block_size
    lead = b'A' * (block_size - 1)
    for size in range(block_size):
        for i in range(256):
            test = (b'A' * pre_pad) + lead + known_answer + b[i:i+1] + lead
            a._encrypt(pre + test, unknown_string, a.key)
            if a.result[start_pt + (block_id * block_size) - block_size: \
                        start_pt + (block_id * block_size)]              \
                ==                                                       \
                a.result[start_pt + ((block_id * 2) * block_size) - block_size : \
                         start_pt + ((block_id * 2) * block_size)]:

                known_answer = known_answer + b[i:i+1]
                lead = lead[0:len(lead) -1]
                print(lead, known_answer, flush=True)
                break

print(known_answer.decode())
                                    
