#! /usr/local/bin/python3

# Global imports

import struct
from sys import path

# Package imports
# ##### This is for testing and ensuring import is run correct #####
if path[0] == '/home/jason/Projects/Crypto/Set3/Code/msg':
    from AES import encryptMsg
else:
    from .AES import encryptMsg


def _xor(n, m):
    return bytes((n ^ m,))


def _nonce_generator(nonce):
    """
Generator that iterates through the nonce.
Currently uses '<QQ' from struct pack.

Return struct bytes result

Future: Change to allow different nonce patterns

"""
    max_8 = 18446744073709551615  # Max uint in a long long (8 bytes)

    def convert(no):
        return no // (max_8 + 1), no % (max_8 + 1)

    b, s = convert(nonce)
    yield struct.pack('<QQ', b, s)
    n = nonce
    while True:
        n += 1
        b, s = convert(n)
        yield struct.pack('<QQ', b, s)


def ctr_crypt(bstring, bkey, nonce=0, block='AES'):
    """
ctr_crypt(bstring, bkey, nonce=0, ) -> bytes

This function will take a byte or bytearray string (bstring) with a
byte key (bkey).
nonce is the start of the counter
block is the type of encryptor

Returns a bytes of the decrypted msg
"""
    if block == 'AES':
        chunks = (bstring[x:x + 16] for x in range(0, len(bstring), 16))
        counter = _nonce_generator(nonce)
        ret = list()
        for chunk in chunks:
            c = next(counter)
            block = encryptMsg(c, bkey)
            # ret.append(list(zip(chunk, block)))
            ret.append(b"".join((_xor(x, y) for x, y in zip(chunk, block))))
        return b"".join(ret)

if __name__ == '__main__':

    import argparse

    from base64 import b64decode
    from sys import argv

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        help="Input binary from a file")
    parser.add_argument('-o', '--output',
                        help="Output binary to a file")
    parser.add_argument('-t', '--test', dest='test',
                        action='store_true',
                        help="This is to run the standard test")

    args = parser.parse_args()

    if len(argv) == 1:
        parser.print_help()

    if args.test:
        string = b"L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu" + \
                 b"/6/kXX0KSvoOLSFQ=="
        bstring = b64decode(string)
        print(ctr_crypt(bstring, b"YELLOW SUBMARINE"))

    if args.input:
        with open(args.input, 'rb') as f:
            t = f.read()
            if args.output:
                with open(args.output, 'wb') as w:
                    w.write((ctr_crypt(t, b'YELLOW SUBMARINE')))
            else:
                print(ctr_crypt(t, b'YELLOW SUBMARINE'))
