#! /usr/bin/python3

from msg.padding import padtest as pt 

msg = eval(input("Enter string with padding (eg \\x02\\x02)\n" + \
            "To send bytes objects, start with b' and end with '\n" + \
            "\\x01 is the format for padding.\n"))
block_size = input("Enter block size in bytes\n")

try:
    block_size = int(block_size)
except:
    print("Block size must be able to be an int")
    exit()
    
b_msg = msg
print("Verifying...")
print("{}".format(b_msg))
print("Block size is {}".format(block_size))

print(pt(b_msg, block_size))

