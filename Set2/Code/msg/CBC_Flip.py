#! /usr/bin/python3

# builtin imports
from random import randint

# Custom imports
from .padding import pkcs7
from .AES import encryptMsgCBC
from .AES import decryptMsgCBC

# This holds 2 functions,
#  1) Inject in-between a pre and append string function
#  2) decrypt and parse, looking for admin=  (returns 2 pair tuple)


def insert(user, block_size):
    #msg = ''
    msg = bytearray(_userinput(user).encode())
    print(msg)

    #padded = ''
    padded = _padmsg(msg, block_size)

    key, iv = _randomize(block_size)

    return (encryptMsgCBC(padded, key, iv), padded, key, iv)


def inspect(encrypted, key, iv):
    """This will return a dictionary of pairs and whether admin was found"""
    decrypted = decryptMsgCBC(encrypted, key, iv)
    print(decrypted, "\n")
    pairs = _parse(decrypted)
    return pairs


def manual_size(userinput, blocksize, change="NO"):
    """Checks the size of the userinput, ensuring that len(input) == blocksize"""
    if change == "NO":
        msg = _strip(userinput)
    else:
        msg = userinput

    if len(msg) == blocksize:
        print("\nYou matched the blocksize first time.\nAwesome\n")
        print("Your msg is [{}]\n".format(msg))
        return msg
    else:
        ret = _resize_msg(msg, blocksize, change)
        return ret


def generateMod(encrypted, original, changeto, location, blocksize):
    """This function will identify the XOR required to produce changeto msg, returning the modified msg.
Returns a bytearray
encrypted - bytearray
changeto - string
location - int
blocksize - int
The key to this function is the 2 for loops.
Loop 1: Takes the XOR of the original msg and the Encrypted msg.
Loop 2: Takes the msg to change to and the results from XOR.
Because the Encrypted msg of block 1 become the iv of block 2,
we are simply changing how it decrypts.  The iv is the last
stage of the decryption.  This destroys the first block but generates
an iv that decodes the second block to what we want. """
    b_change = changeto.encode()
    b_original = original.encode()
    xor_o = encrypted[location:location + blocksize]
    xor_n = bytearray()
    exit_node = bytearray()
    try:
        assert len(changeto) == blocksize
        assert len(original) == blocksize
        assert len(xor_o) == blocksize
    except:
        print("There is a size mismatch with blocksize and change size.")
        print("Failing!!!!!!!!!!!\n\n")
        quit()
    for i in range(len(b_original)):
        exit_node.append(b_original[i] ^ xor_o[i])
    for i in range(len(b_change)):
        xor_n.append(exit_node[i] ^ b_change[i])
    mod = encrypted
    mod[location:location + blocksize] = xor_n

    return mod


def _strip(msg):
    m = msg.replace(';', '')
    m = m.replace('=', '')
    return m


def _resize_msg(userinput, blocksize, change="NO"):
    """This verifies and confirms inject required"""
    msg = userinput
    first = True
    while len(msg) != blocksize:
        if first != True:
            print("Try again.  Doesn't match block size.")
        print("\nYour inject is currently {} characters".format(len(msg)))
        print("[{}]\n".format(msg))
        print("It needs to be {} long.".format(blocksize))
        msg = input("Please enter your msg:\n")
        if change == "NO":
            msg = _strip(msg)
    print("Confirmed\nYour msg is [{}]\n".format(msg))
    return msg


def _parse(msg):
    """This ensures it is a string then creates a dictionary of pairs"""
    holding = msg
    dic = {}
    if not isinstance(holding, bytes):
        if isinstance(holding, bytearray):
            holding = bytes(holding)
        else:
            holding = holding.encode()
    pairs = holding.split(b';')

    for pair in pairs:
        print(pair)
        print(type(pair))
        try:
            dic[pair.split(b'=')[0]] = pair.split(b'=')[1:]
        except:
            dic[pair] = None
    return dic


def _randomize(block_size):
    """This returns both a random key and iv"""
    key = []
    iv = []
    for i in range(block_size):
        key.append(randint(0, 255))
        iv.append(randint(0, 255))
    key = bytearray(key)
    iv = bytearray(iv)
    return key, iv


def _userinput(user):
    """Takes a string of user input and strips out ";" and "="
If I feel fancy, this will also do that with bytearrays"""
    userinput = ''
    userinput = user
    userinput = userinput.replace(";", "")
    userinput = userinput.replace("=", "")
    pre = "comment1=cooking%20MCs;userdata="
    append = ";comment2=%20like%20a%20pound%20of%20bacon"
    return pre + userinput + append


def _padmsg(msg, block_size):
    """This will add padding to the msg.  Block_size needs to be an int"""
    return pkcs7(msg, block_size)


if __name__ == "__main__":
    user = input("Need input <Johnny 5>\n")
    msg = bytearray(_userinput(user).encode())
    print(msg.decode())

    blocksize = input("What is the block size (in bytes)?\n")
    blocksize = int(blocksize)
    msg = pkcs7(msg, blocksize)

    print(msg)
    print("Now encoding under a random CBC AES 128 key...")

    key = []
    iv = []
    for i in range(blocksize):
        key.append(randint(0, 255))
        iv.append(randint(0, 255))
    assert len(key) >= 16
    assert len(iv) >= 16
