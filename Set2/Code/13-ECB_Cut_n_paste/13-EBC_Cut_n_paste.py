#!/usr/bin/python3

# This is to parse info

# Profile  func("name@someone.com") should return
#{
#  email: 'name@someone.com',
#  uid: 10,
#  role: 'user'
#}

# Encoded as email=name@someone.com&uid=10&role=user

# Using only the user input to profile_for() (as an oracle to generate "valid" ciphertexts)
# and the ciphertexts themselves, make a role=admin profile.


import json
from random import randint
from msg.AES import encryptMsg
from msg.AES import decryptMsg

# Generate random AES key
random_key = bytearray()
for i in range(16):
    random_key.append(randint(0,255))

def to_encode(email):
    """To send msg to encode"""
    # Remove & and = if user added to name
    email.replace('&','')
    email.replace('=','')
    uid = 10
    role = 'user'
    encoded_as = '&'.join(['email='+email,
                           'uid='+str(uid),
                           'role='+role])
    # Debug statement - print(encoded_as)
    return encoded_as.encode()

def profile_for(email, random_key):
    """To follow the naming from the text, profile_for generates encoded msg"""
    return encryptMsg(to_encode(email), random_key)

def decode(msg, random_key):
    """To decode msg"""
    return decryptMsg(msg, random_key)

if __name__ == '__main__':

    # Create encoding
    email = input("Enter your email\n")
    encoding = profile_for(email, random_key)
    print(encoding)

    # Parse object
    d_email,d_uid,d_role = decode(encoding, random_key).decode().split('&')
    print(d_email,d_uid,d_role)


# Must check to find the padding size.  We know that it encodes email=,
#        uid=(string(10)) and role=user

pad_size = 0
msg_size = len(encoding)
while msg_size == len(encoding):
    encoding = profile_for(('A' * pad_size) + email, random_key)
    pad_size += 1
    
# Above adds padding until the size of result changes to identify padding of msg.


print("Suspected padding size is {}".format(pad_size))

block_size = 0
msg_size = len(encoding)
while msg_size == len(encoding):
    encoding = profile_for('A' * (block_size + pad_size) + email, random_key)
    block_size += 1
print("Cypher size is suspected to be {}".format(block_size))

# Final test of the block_size to see if there was no padding

if pad_size == block_size:
    print('Oops, there was no padding')
    pad_size = 0

# Now we move into the heavy lifting
# With the block size known, put that as the email input to work breaking the key.

print ("We are going to attempt to break the key now. Psych.")
print ("There is a better way!!!")
print ("First take the word admin and attach the padding that would normally be at the end of EBC")

padding_required = block_size - len("admin")
cut_block = "admin" + ("{:c}".format(padding_required) * padding_required)

cut_encode = profile_for( ("a" * (block_size - len("email=")) ) + cut_block, random_key)

paste_encode = cut_encode[block_size: block_size * 2]

# Now we have how to paste admin at the end of the encoding.
# Next we find out what we have to input to leave the tail of the 2nd last block
#   to be role=

size_req = 0
total_len = (len("email=" + "uid=10" + "role=" + "&&"))
for i in range(10000): # I know this is excessive.  Won't reach

    if (i + total_len) % block_size == 0:
        print("i is {}".format(i))
        size_req = i

        # Test if what was entered is too short, pad as required.
        
        if len(email) < i:
            email= email + ("a" * (i - len(email)))
            
        # The end is in site.  Throw down the new msg
        # Debug statement - print("Size required is {}".format(size_req))
        
        final = profile_for(email[0:size_req], random_key)

        # Debug statement - print("Decode before cut\n{}".format(decode(final, random_key)))

        final = final[0:-(block_size)] + paste_encode
        print("Below is the encrypted version we are going to decode.\n")
        print(final)
        print("\n")
        
        print("\nNow the test ...")
        
        # Parse the object
        d_email = decode(final, random_key).decode().split('&')
        print(d_email)
        break

print("\nARE WE GOOD NOW?")
print("\nOWN ALL THE THINGS!!!\nl33t!!")

                         
# TODO: The size function is not allowing it to easily create
#   I have to ensure that the email size is 13 characters for admin to work
#   This needs to be figured out to add functionality.
