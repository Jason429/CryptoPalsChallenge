#! /usr/bin/python3

def pkcs7(msg, len_needed):
    """(len_needed = int)This returns a bytearray with pkcs7 padding.
Msg needs to be bytearray
It places it into the msg.
It takes the the msg and add the padding required to the end."""
    # Test for int
    if type(len_needed) != type(1):
        print('From padding.py -> pkcs7')
        print('len_needed must be an integer')
        raise
    if len_needed == 0:
        print('Padding is not required')
        return msg
    if len_needed < 1 or len_needed > 255:
        print('From padding.py -> pkcs7  ')
        print('len_needed must be between 0 - 255')
        raise
    op_msg = bytearray(msg)
    needed = len_needed - (len(msg) % len_needed)
    for count in range(needed):
       op_msg.append(needed)
    return op_msg

def padtest(msg, block_size):
    """(msg = bytes/bytearray, block_size = int)
This returns whether the block_size is correct or invalid"""
    last_byte = msg[-1:]
    # Need bytearray to hold matching count and assign
    
    count = bytearray((1,))
    for i in range(-2, (-1 * len(msg)) -1, -1):
        if msg[i:i+1] == last_byte:
            count[0] += 1
            if count == last_byte:
                break
        else:
            break
    # DEBUG value and type below
    # print("Last_byte type and value: {} {}".format(type(last_byte), last_byte))
    # print("Count[0] type and value: {} {}".format(type(count[0]),  count[0]))
    if count == last_byte:
        # print("Success", last_byte, count)
        # Make function (checkfit)
        return checkfit(msg, block_size, count)
    else:
        # print(last_byte, count)
        return "INVALID"

def checkfit(msg,block_size,pad):
    """"Msg - last block (given).  Needs to be last block and in byte format!!!
block_size - int - in bytes
pad - padding to test, (must be byte type object)
"""
    total_msglen = len(msg)
    if total_msglen % block_size != 0:
        return "INVALID"
    assert len(pad) == 1
    last_block = msg[(-1 * block_size): ]

    # Have to strip off only those required
    for i in range(pad[0]):
        if last_block[-1] == pad[0]:
            last_block = last_block[0:-1]
            
    msg_len = len(last_block)
    if msg_len + pad[0] != block_size:
        print("msg",msg)
        print("msg_len with strip", msg_len)
        print("pad", pad)
        print("pad[0]", pad[0])
        print("Checkfit issue!!!!!!")
        return "INVALID"
    else:
        return "VALID"
