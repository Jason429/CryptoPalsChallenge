#!/usr/bin/python3

from msg import defs    # Import modules for XORs
from msg import convert # Import msg converter
import time             # Import time to check running process
import subprocess       # For executing in the shell
import argparse         # For the sys process arguements

parser = argparse.ArgumentParser()
fi="""This is the absolute name of the file.
If the file cannot be found, the program will exit"""
fo="""This is the name of the file to write to.  Ensure that you
have access to the file location and rights to write"""
t="""Switch to 1 to record time it took to operate the XOR"""
sw=""" Switch to 1 to record to standard output the result"""
i=""" MANDATORY:
Explict input type of file or msg.
(bin, str, hex) are your choices"""
o="""MANDATORY:
The type of output. Choices are hex, str, or bin."""
m="""Message to operate on straight from the command line"""
xor="""Single or repeating XOR used.  It is converted to bytes"""
coding="utf-8"          # encoding used bytearray

# -fi FILEIN  -fo FILEOUT -t TIME
parser.add_argument("-x", "--xor", help=xor)
parser.add_argument("-m", "--message", help=m)
parser.add_argument('-i', "--input", help=i)
parser.add_argument("-o", "--output", help=o)
parser.add_argument("-fi", "--filein", help=fi)
parser.add_argument("-fo", "--fileout", help=fo)
parser.add_argument("-t", "--time", help=t)
parser.add_argument("-sw", "--showwork", help=sw)



subprocess.call("clear")
args = parser.parse_args()
# Checking argparse
# print(args.filein, args.fileout, args.time, args.showwork, args.output)

# To clear help variables definitions
del fi,fo,t,sw,o,m,xor,i

# Check to see if the file exists
if args.filein != None:
    if convert.check_for_file(args.filein) != True:
        print("Cannot find file.  Is it a directory?")
        quit()

# Check to ensure user has not set both messag and filein
if args.filein and args.message != None:
    print("Can't have both msg and file in")
    quit()

msg = ''
if args.message != None:
    msg = bytearray(args.message, "utf-8")
if args.filein != None and args.input != None:
    if args.input.lower() == 'bin':
        file=open(args.filein,mode='r+b')
    if args.input.lower() == 'str' or args.input.lower() == 'hex':
        file=open(args.filein,mode='r+t')
    msg = file.read()

    file.close()
    if args.input.lower() == 'hex':
        msg = convert.msg_to_raw(msg, override='hex')
    else:
        msg = convert.msg_to_raw(msg)
X = bytearray(b'ICE')
if args.xor != None:
    X = bytearray(args.xor, "utf-8")

tim = 0

# print(str(msg.decode()) + "\n\n")
### Actual program ###
tim = time.time()
result, xor = defs.xor(msg,X)
tim = time.time() - tim
### End of work ###
try:
    if args.output.lower() == 'hex':
        result = convert.raw_to_hexstr(result)
    if args.output.lower() == 'str':
        result = result.decode()
    if args.output.lower() == 'bin':
        file = open(args.fileout, mode='w+b')
        file.write(result)
        file.close()
    else:
        file = open(args.fileout, mode='wt')
        file.write(result)
        file.close()
except:
    print('Both -i and -o are required')
    exit()
if args.fileout == None:
    print(result)
if args.time == '1':
    print(tim)
# print('\n\n')

if args.showwork == '1':
    if args.output.lower() == 'hex':
        print("Result in hex: " + str(result[2:]))
    if args.output.lower() == 'bin':
        print("Result in bytes:" + str(result))
    if type(result) == type(' '):
        print("Result in str: " + result)
    print("XOR used: " + str(xor))


