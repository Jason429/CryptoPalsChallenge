#! /usr/bin/python3.2mu

### This is XOR of Set 1 ###

# Variables are the following

orig = r'1c0111001f010100061a024b53535009181c'
xchange = r'686974207468652062756c6c277320657965'
result = r'746865206b696420646f6e277420706c6179'

###
### Basically start with orig and apply XOR of xchange
### to get the result of result

### only integers in Python can XOR
### orig when converted to bytes screws up and is useless!!!
#####
### xchange however is fine

a = int(orig,16)
b = int(xchange,16)
c = a ^ b
print (result)
print (hex(c)[2:])  # Slice is to remove 0x fm string
print ("\n\n")

if hex(c)[2:] == result:
    print ("The two are a match")

    
#### The better option ####
#### Keep in bytes !!! ####

d = bytes.fromhex(orig)
e = bytes.fromhex(xchange)
if len(d) == len(e):
    f = bytearray(len(d)) # If you want to set asside mem,
    #                       else use append in function
    for i in range(len(d)):
        f[i] = d[i] ^ e[i]

    print("Here is the string msg\n")
    print(f.decode())
    print("\n")
    print("Here is the hex value\n")
    msg = ''
    for i in range(len(f)):
        msg = msg + hex(f[i])[2:]

    print(msg)
    if msg == result:
        print("\nThis is also a match")
else:
    print("Original hex and XOR factor are not the same size")


        
