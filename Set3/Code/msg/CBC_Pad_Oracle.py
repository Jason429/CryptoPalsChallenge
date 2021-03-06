#! usr/bin/python3
# Import from builtins

from random import choice, randint
from base64 import b64decode
from sys import path

# Import from custom
# ##### To correct import for testing and live #####
if 'msg' in path[0]:
    from .AES import encryptMsgCBC as emCBC
    from .AES import decryptMsgCBC as deCBC
    from .padding import padtest, pkcs7
else:
    from msg.AES import encryptMsgCBC as emCBC
    from msg.AES import decryptMsgCBC as deCBC
    from msg.funcs.padding import padtest, pkcs7

# Strings given to randomly pick from

string_list = ["MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
               "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
               "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
               "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
               "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
               "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
               "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
               "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
               "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
               "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"]


def choose(string):
    """Return a random string in bytes from base64"""

    # picked = string_list[2]# choice(string)
    picked = choice(string)
    picked = b64decode(picked)
    # print(picked)
    return picked


def random_key(blocksize):
    """Generates a random key or iv to use."""

    key = bytearray()
    for i in range(blocksize):
        key.append(randint(0, 255))
    return key


class Oracle_Server(object):
    """This is a class to take an example of a server, checking if the padding is correct, 
for anything that is sent to it.  It will either return VALID or INVALID padding response."""

    def __init__(self, blocksize):
        # self.key = bytearray(b'q\xeb6\xfc\xf3\xc9\x18b\xd8E\xe5\x94\x0en\xf1\xee')#random_key(blocksize)
        # self.iv =
        # bytearray(b'\xc7Q%\x8fG\x83s\xb08\x9a\xd4\xa7v\xa7\xf2\xa7')#random_key(blocksize)
        self.key = random_key(blocksize)
        self.iv = random_key(blocksize)
        # Need to choose and properly pad the string
        string = choose(string_list)
        l = len(string)
        for i in [x * blocksize for x in range(100)]:
            if i > l:
                l = i
                break
        to_encrypt = pkcs7(string, l)
        self.string = to_encrypt
        self.encrypted = emCBC(to_encrypt,
                               self.key,
                               self.iv)       \
            #  makeblock = 128)
        print("Server created.  Have fun!!!")

    def cipher_iv(self):
        """Simple function that returns the encrypted msg and iv."""

        return (self.encrypted, self.iv)

    def test_padding(self, mod_encrypt, key, iv):
        """Returns a check on the padding of the cypher text, VALID or INVALID.
Only for AES-128 currently."""
        decrypt = deCBC(mod_encrypt, key, iv, makeblock=128)
        return padtest(decrypt, 16)

    def print_string_list(self):
        """This will print the string_list used to verify"""

        for i in string_list:
            print(b64decode(i))

    def breakblock(self, e_block, iv_block, blocksize):
        """Manual test.
        This function will return a block that has been found.
        e_block = the encryption that you are seeking to break
        iv_block = the block that will XOR the result
        blocksize = in bytes the block size"""

        # Set registers
        working_on = []
        completed = [False for i in range(blocksize)]
        known = bytearray(blocksize)
        test = bytearray(blocksize)

        for i in range(-1, (blocksize * -1) - 1, -1):
            working_on.append(i)

            for j in working_on:
                if completed[j] == True:
                    test[j] = iv_block[j] ^ known[j] ^ (i * -1)
                else:
                    for bit_test in range(0, 256):
                        # print(bit_test)
                        test[j] = iv_block[j] ^ (i * -1) ^ bit_test
                        result = self.test_padding(e_block, self.key, test)
                        if result == "VALID":
                            known[j] = bit_test
                            completed[j] = True
                            # print(known)
                            break
                if completed[j] != True:
                    print("Something failed")
                    print("working_on", working_on)
                    print("completed", completed)
                    print("test", test)
                    print("result", result)
        return known

    def work(self, test, blocks, i, j, msg):
        """This is to attempt to bypass intermittent bug in Python.
        (Sometimes it doesn't come up with a valid number on the test)"""
        possible = []
        server_calls = 0
        for bit_test in range(0, 256):
            test[j] = blocks[msg - 1][j] ^ (i * -1) ^ bit_test
            result = self.test_padding(blocks[msg], self.key, test)
            server_calls += 1
            #print("Result", type(result), result)
            #print("Possible", type(possible), possible)
            if result == "VALID":
                possible.append(bit_test)
                break

        if possible == []:
            possible = None

        return possible, server_calls

if __name__ == '__main__':
    pass
