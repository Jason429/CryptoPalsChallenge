#! /usr/local/bin/python3

from collections import defaultdict
from base64 import b64decode
from random import randint

from msg.CTR import ctr_crypt
from msg.defs import single

WORDS = []             # List of words to look for
WORD_FILE = "./msg/top_1000_words.txt"

# Word file for final testing

with open(WORD_FILE, 'r') as f:
    WORDS = tuple([bytes(x.rstrip('\n').lower(), encoding='utf8')
                   for x in f.readlines()])

# b_strings will hold the messages decoded
# Encode it first to test
strings = []
with open('20_input_file.txt', 'r') as f:
    for line in f.readlines():
        j = line.rstrip('\n')
        strings.append(j)

b_strings = [b64decode(x) for x in strings]
cipher_key = bytes()
# b_strings is not encrypted!!!  Encrypt with random

for i in range(16):
    cipher_key += bytes([randint(0, 255), ])

result = [ctr_crypt(x, cipher_key) for x in b_strings]

# result is the final encoding

xor = bytearray()
for i in range(0, 256):
    xor = xor + bytearray([i, ])

# #################### Done Setup ####################

max_size = max((len(x) for x in result))
hold = []
for i in range(0, max_size):
    org = [j for j in enumerate((x[i:i + 1] for x in result))]
    msg = b"".join([x[i:i + 1] for x in result])
    ans = single(msg, xor)

    # Modify so it only takes first answer

    for k, v in ans.items():
        ans = v[1]

    to_hold = b''
    point = 0
    for j in org:
        if j[1] == b'':
            to_hold += b' '
        else:
            to_hold += ans[point: point + 1]
            point += 1
    hold.append(to_hold)

d = defaultdict(list)

for i in range(len(hold)):
    for j in range(len(hold[i])):
        d[j].append(hold[i][j])

for x in range(len(d)):
    print(b"".join((i.to_bytes(1, 'big') for i in d[x])))

# ##### This would be where we would stop for only the shortest size #####
# ########## I think we can make this better ##########
