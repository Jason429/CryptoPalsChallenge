#! /usr/bin/python3

from msg.padding import pkcs7 as add_pad

msg = input("Enter the msg to pad : ")
length = input("Enter the length of a block in bytes : ")

# Convert to bytearray and int

try:
    msg = msg.encode()
    length = int(length)
except:
    print("Msg needs to be a string.")
    print("Length needs to be able to converted to an integer")
    print("Float, hex (0xff) and octal (0o74) are acceptable.")
    print("Must quit.  ............... Try again")
    exit()

print("Original msg is ", msg.decode())
ret = add_pad(msg,length)
print("Returned msg is ", ret)
print("When decoded - ", ret.decode())
