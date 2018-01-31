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
    msg = bytearray(msg)
    for count in range(len_needed):
        msg.append(len_needed)
    return msg
        
    
    
