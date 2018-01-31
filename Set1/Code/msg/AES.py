#! /usr/bin/python3

########################
# This module is my attempt at encrypting/ decrypting AES
######################

from . import padding

def blockp(block):
    for i in range(4):
        for j in block[i]:
            print(hex(j))
        print('\n')

def _initarray128():
    array = []
    for i in range(4):
        array.append(bytearray())
    return array

def _sizetest(msg,size, padding=1):
    """This tests the size of padding to n bytes.  If not a factor of n,
raises an exception.  Size must be int.  Msg must be bytes or bytearray.
Padding = 0 is to test for exception.
Padding = 1 is to add padding to msg."""
    if type(size) != type(1):
        print("Requires an integer for size")
        raise
    if len(msg) % size !=0:
        if padding == 1:
            # Padding =1 for PCKS7 padding
            # Requires import from padding.py
            toadd = size - (len(msg) % size)
            msg = PADDING.pkcs7(msg, toadd)
            return msg
        else:
            # Padding error raised
            print('This is not a perfect group of {0}'.format(size))
            print('Padding is required but was not selected')
            print('Quiting ....')
            raise
    return

def make128block(msg):
    """Returns a list in 4 x 4 block.
Msg must be a bytearray and 16 bytes long"""
    if type(msg) == type(bytes([1,2])):
        msg = bytearray(msg)
    if type(msg) != type(bytearray([1,2])):
        print('AES.make128block - ERROR - Msg not bytes or bytearray')
        return
    if len(msg) != 16:
        print('AES.make128block - ERROR - Msg is not 16 bytes long')
        return
    # initialize array
    array = _initarray128()
    for i in range(4):
        for j in range(4):
            array[j].append(msg[(i * 4) + j])
    ######
    # Fills columns then rows
    # Reads by rows
    ######

    return array

def deBlock(block):
    """Takes an array and returns back to a single byte array"""
    array = bytearray()
    for col in range(len(block)):
        for row in range(len(block[col])):
            array.append(block[row][col])
    return array
            

def xorBlock(msg,key, makeblock = 128):
    """This is to xor block and return an array.  If makeblock = 128, block
will be 4 x 4."""
    if makeblock == 128:
        array = _initarray128()
        for col in range(4):
            for row in range(4):
                array[row].append((msg[row][col]) ^ (key[row][col]))
        return array

_s_box = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
         0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 
         0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 
         0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 
         0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 
         0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 
         0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, 
         0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 
         0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, 
         0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 
         0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 
         0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, 
         0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 
         0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 
         0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 
         0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]

_rcon = [0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
        0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 
        0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 
        0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 
        0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 
        0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 
        0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 
        0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 
        0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 
        0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 
        0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 
        0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 
        0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 
        0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 
        0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 
        0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d]



def _send_Rcon():
    """Returns Rijndael RCON"""
    return rcon

### Tested - Works
def subBytes(msg,makeblock=128, encrypt=1):
    """Conducts byte substitution using Rijndael S-Box
Input needs to be from AES.make<number>block function.
Makeblock=128 returns a 4x4 block array"""
    if makeblock == 128:
        array = _initarray128()
        if encrypt == 1:
            for col in range(4):
                for row in range(4):
                    array[row].append(_s_box[msg[row][col]])
        if encrypt == 0:
            for col in range(4):
                for row in range(4):
                    array[row].append(_s_box.index(msg[row][col]))
    return array

def shiftRows(msg, makeblock = 128, encrypt=1):
    """Shifts the rows. Encrypt goes one way. Decrypt opposite
First row = No shift
Second row = push left 1
Third row = push left 2
Fourth row = push left 3
Ensure correct makeblock
Returns block array."""
    if makeblock == 128 and encrypt == 1:
        array = _initarray128()
        # First row
        array[0] = msg[0]
        # Second row
        array[1] = msg[1][1:4] + msg[1][0:1]
        # Third row
        array[2] = msg[2][2:4] + msg[2][0:2]
        # Fourth row
        array[3] = msg[3][3:4] + msg[3][0:3]
        return array
    if makeblock == 128 and encrypt == 0:
        array = _initarray128()
        # First row
        array[0] = msg[0]
        # Second row
        array[1] = msg[1][3:4] + msg[1][0:3]
        # Third row
        array[2] = msg[2][2:4] + msg[2][0:2]
        # Fourth row
        array[3] = msg[3][1:4] + msg[3][0:1]
        return array

################
#  mult = for computing in field for mixColumns
################
def mult(a,b):
    """This is the math required to multiply/compute the field.  Multiplies
polynomials.  Followed a C example on wikipedia.  Works well!!"""
    p = 0
    for i in range(8):
        if b % 2 == 1:
            p = p ^ a
        a = a << 1
        if a > 255 and a < 2 * 256:
            a = a ^ 0x11b
        b = b >> 1
    return p


testarray = [bytearray([0x32,0x88,0x31,0xe0]),bytearray([0x43,0x5a,0x31,0x37]),
             bytearray([0xf6,0x30,0x98,0x07]),bytearray([0xa8,0x8d,0xa2,0x34])]
testkey = [bytearray([0x2b,0x28,0xab,0x09]),bytearray([0x7e,0xae,0xf7,0xcf]),
             bytearray([0x15,0xd2,0x15,0x4f]),bytearray([0x16,0xa6,0x88,0x3c])]
testcipher = [bytearray([0x39,0x02,0xdc,0x19]),bytearray([0x25,0xdc,0x11,0x6a]),
             bytearray([0x84,0x09,0x85,0x0b]),bytearray([0x1d,0xfb,0x97,0x32])]
def mixColumns(msg, makeblock = 128, encrypt=1):
    """Runs Rijndael mixColumn.  Msg is 4 x 4 block bytearray if makeblock=128"""
    if makeblock == 128:
        array = _initarray128()
        if encrypt == 1:
            matrix = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
        if encrypt == 0:
            matrix = [[14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14]]
        for col in range(4):
            for row in range(4):
                array[row].append((mult(msg[0][col],matrix[row][0]) ^
                                       (mult(msg[1][col],matrix[row][1])) ^
                                       (mult(msg[2][col],matrix[row][2])) ^
                                       (mult(msg[3][col],matrix[row][3]))
                                   )
                                  )
        return array


def genKeySchedule(key, makeblock = 128):
    """ Generates the key schedule.  Returns the full array.
Key must be 4 x 4 bytearray.
If makeblock is 128, returns an array 44 x 4 length block (to chop up)"""
    if makeblock == 128:
        array = _initarray128()
        for col in range(len(key)):
            for row in range(len(key[col])):
                array[row].append(key[row][col])
        for i in range(20):
            if (len(array[0]) % 4) == 0:
                # Rotate
                array[0].append(array[1][-1])
                array[1].append(array[2][-1])
                array[2].append(array[3][-1])
                array[3].append(array[0][-2]) # Because -1 is now filled
                # Subtitute
                array[0][-1] = _s_box[array[0][-1]]
                array[1][-1] = _s_box[array[1][-1]]
                array[2][-1] = _s_box[array[2][-1]]
                array[3][-1] = _s_box[array[3][-1]]
                # XOR rot
                len_array4 = len(array[0])/4
                rcon_debug = _rcon[int(len(array[0])/4)]
                array[0][-1] = (array[0][-1]) ^ (_rcon[int(len(array[0])/4)])
                # XOR
                array[0][-1] = array[0][-5] ^ array[0][-1]
                array[1][-1] = array[1][-5] ^ array[1][-1]
                array[2][-1] = array[2][-5] ^ array[2][-1]
                array[3][-1] = array[3][-5] ^ array[3][-1]
            else:
                for j in range(3):
                    array[0].append(array[0][-1] ^ array[0][-4])
                    array[1].append(array[1][-1] ^ array[1][-4])
                    array[2].append(array[2][-1] ^ array[2][-4])
                    array[3].append(array[3][-1] ^ array[3][-4])
        return array
                                            
    
    
def encryptAES(msg, key, makeblock = 128):
    """Takes block128 = 4 x 4 msg an key.  Returns an encrypted 4 x 4 array."""
    if makeblock == 128:
        key = genKeySchedule(key)

        # xor original plain text with genkey round1
        array = xorBlock(msg,key)
        # Subbyte, shift Row, mix Columns Xor next Round Key
        # do this 9 times
        for count in range(1,10):
            array = subBytes(array, makeblock=128, encrypt=1)
            array = shiftRows(array, makeblock=128, encrypt=1)
            array = mixColumns(array, makeblock=128, encrypt=1)
            for col in range(4):
                for row in range(4):
                    array[row][col] = array[row][col] ^ key[row][col + (count * 4)]
        
        # Subbyte, shift Row, last round key
        array = subBytes(array, makeblock=128)
        array = shiftRows(array, makeblock=128, encrypt=1)
        for col in range(4):
            for row in range(4):
                array[row][col] = array[row][col] ^ key[row][col + 40]
        
        # return ciphertext
        return array

def encryptMsg(msg, key, makeblock = 128):
    """This function is to simply allow bytes or bytearray msg and key and encrypts.
Returns message as bytearray."""
    encrypt_msg = bytearray()
    if makeblock == 128:
        if len(msg) % 16 != 0:
            msg = _sizetest(msg,16,padding=1)
        _sizetest(key,16,padding = 0)

        for start_of_next_block in range(0,len(msg),16):
            # Break original msg into 16 byte block
            workingmsg = make128block(msg[start_of_next_block:(start_of_next_block + 16)])
            keyblock = make128block(key)

            # Send to be encrypted
            result = encryptAES(workingmsg, keyblock, makeblock=128)
            result = deBlock(result)
            encrypt_msg.extend(result)
        return encrypt_msg

def encryptMsgCBC(msg, key, iv, makeblock = 128):
    """Uses CBC mode for encrypting msgs.  Returns msg bytearray, same as encryptMsg"""
    encrypt_msg = bytearray()
    if makeblock == 128:
        if len(msg) % 16 != 0:
            msg = _sizetest(msg,16,padding=1)
        _sizetest(key,16, padding=0)
        _sizetest(iv,16, padding=0)
        iv = make128block(iv)

        for start_of_next_block in range(0,len(msg),16):
            workingmsg = make128block(msg[start_of_next_block:(start_of_next_block + 16)])
            keyblock = make128block(key)
            # xor against iv (or result of cipher)
            workingmsg = xorBlock(workingmsg, iv, makeblock=128)
            result = encryptAES(workingmsg, keyblock, makeblock=128)
            # copy result to iv for next iteration
            iv = result
            result = deBlock(result)
            encrypt_msg.extend(result)
        return encrypt_msg
        
    
    
def decryptAES(msg, key, makeblock = 128):
    """ Takes block128 = 4 x 4 msg as encrypted key.  Returns plain text 4 x 4 array."""
    if makeblock == 128:
        key = genKeySchedule(key)
        keyblock = _initarray128()
        
        # Xor Round key (11), shift Row reverse, find subbyte and pull position
        #### Make key block
        for i in range(4):
            keyblock[i] = key[i][40:44]
        # XOR round key
        array = xorBlock(msg, keyblock, makeblock=128)
        # shiftRows reverse
        array = shiftRows(array, makeblock=128, encrypt=0)
        # replace subbyte
        array = subBytes(array, makeblock=128, encrypt=0)
        
        # Xor Round key, Mix Column (with inverse), shift Row reverse, find subbyte and pull position
        # do this 9 times
        for rcount in range(9,0,-1):
            for i in range(4):
                keyblock[i] = key[i][(rcount * 4):((rcount + 1) * 4)]
            array = xorBlock(array, keyblock, makeblock=128)
            array = mixColumns(array, makeblock=128, encrypt=0)
            array = shiftRows(array, makeblock=128, encrypt=0)
            array = subBytes(array, makeblock=128, encrypt=0)
        # Xor Final Round key
        for i in range(4):
            keyblock[i] = key[i][0:4]
        array = xorBlock(array, keyblock, makeblock=128)
        # Return plain text
        return array

def decryptMsg(msg, key, makeblock = 128):
    """This function is to simply allow bytes or bytearray msg and key and decrypts.
Returns message as bytearray."""
    decrypt_msg = bytearray()
    if makeblock == 128:
        _sizetest(msg,16,padding=0)
        _sizetest(key,16,padding=0)
        
        for start_of_next_block in range(0,len(msg),16):
            # print(start_of_next_block)
            # Break original msg into 16 byte block
            workingmsg = make128block(msg[start_of_next_block:(start_of_next_block + 16)])
            keyblock = make128block(key)
                               
            # Create block for key

            # Send to be decrypted
            result = decryptAES(workingmsg,keyblock,makeblock=128)
            result = deBlock(result)
            decrypt_msg.extend(result)
        return decrypt_msg

def decryptMsgCBC(msg,key,iv, makeblock=128):
    """Uses CBC mode for decrypting msgs.  Returns msg bytearray, same as decryptMsg"""
    decrypt_msg = bytearray()
    if makeblock == 128:
        _sizetest(msg,16,padding=0)
        _sizetest(key,16,padding=0)
        _sizetest(iv,16,padding=0)
        iv = make128block(iv)
        
        for start_of_next_block in range(0,len(msg),16):
            workingmsg = make128block(msg[start_of_next_block:(start_of_next_block + 16)])
            keyblock = make128block(key)
            # grab cipher text for next iv
            next_iv = workingmsg
            result = decryptAES(workingmsg,keyblock,makeblock=128)
            # XOR to IV or next_iv
            result = xorBlock(result,iv,makeblock=128)
            result = deBlock(result)
            decrypt_msg.extend(result)
            # make iv = next_iv for next iteration
            iv = next_iv
        return decrypt_msg




