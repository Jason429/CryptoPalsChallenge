#!/usr/bin/python3.2mu

##----This module is to convert msgs to bytes, hex, base64, etc ----##

# Type checking constants #
import sys
import os.path      # To check if file exists
import base64

__tstr = str(type(' '))
__tint = str(type(5))
__tfloat = str(type(5.43))
__tbytes = str("<class 'bytes'>")
__tbytearray = str("<class 'bytearray'>")
workingmsg = ""
bit8 = (128, 64, 32, 16, 8, 4, 2, 1)
bit16 = (32768, 16384, 8192, 4096, 2048,
         1024, 512, 256, 128, 64, 32, 16,
         8, 4, 2, 1)


def byte_binary(num, byte):
    """Number and byte iter"""
    result = []
    join = ''
    for f in byte:
        if num >= f:
            result.append(1)
            num = num - f
        else:
            result.append(0)
    for i in result:
        join = join + str(i)
    return join


def convert_binary(msg, byte):
    """Message needs to be iterable ints.
byte bit8 or bit16"""
    msgb = ""
    for i in msg:
        if byte == 'bit8':
            msgb = msgb + byte_binary(i, bit8)
        if byte == 'bit16':
            msgb = msgb + byte_binary(i, bit16)
    return msgb


def msg_to_raw(msg, override=None):
    """This is to convert msgs to raw format to work on.
It will check the type and convert accordingly with an option to override

Below are lists in override
For strings -
    """

    if str(type(msg)) == __tstr:
        if override == None:
            msg = msg.encode()
            return msg
        elif override == 'hex':
            if msg[0:2] == '0x':
                msg = msg[2:]
            if msg[-1] == '\n':
                msg = msg[:-1]
            msg = bytes.fromhex(msg)
            return msg
        elif override == 'base64':
            msg = base64.b64decode(msg)
            return msg
    elif str(type(msg)) == __tint:
        pass
    elif str(type(msg)) == __tfloat:
        print('You fed me a float!!!\n\n'
              'What am I supposed to do with that?')
        return
    elif str(type(msg)) == __tbytes:
        # print('Msg is already in bytes')
        return msg
    elif str(type(msg)) == __tbytearray:
        print('Msg is a bytearray')
        return msg
    else:
        print('Unable to understand the type.\nWas It Empty???"')
        return


def raw_to_hexstr(msg):
    """This is to convert raw to a hex string.
0x will be placed at the beginning of the string"""
    j = ''
    for i in msg:
        if i < 16:          # To add padding to bytes
            j += '0' + (hex(i)[2:])
        else:
            j += hex(i)[2:]
    j = '0x' + j
    return j


def check_for_file(file):
    """This function is to check to see if a file exists and is readable"""
    return os.path.isfile(file)


if __name__ == '__main__':
    try:
        m = sys.argv[1]
        n = msg_to_raw(m)
        print(n)
    except:
        print("Something went wrong.  Exiting....")
