#! /usr/bin/python3

# orig = original string
# prod = should be the end product

import base64

# Msgs and result below
orig = r'49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
prod = r'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

b = bytes.fromhex(orig)

print("Below is the actual UTF-8 text")
print(b)

b = base64.b64encode(b)

print("Running a test to see if base64 encoding works and matches. \n")

if b.decode() == prod:
    print ("WooHoo!!  They match ... \n")
    print (b)

print("\n\nAbove is lyrics from Vannila ICE,ICE Baby\n\n")
