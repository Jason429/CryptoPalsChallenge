#! /usr/bin/python3.4m

## Single XOR 

# Generate single XOR list
xor = []
for i in range(0,256,1):
    xor.append(i.to_bytes(1,"big"))

# Below msg is from single XOR

msg = r'1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
orig = bytes.fromhex(msg)

def englishtest(result, etaoin_shrdlu=[12.02,9.1,8.12,7.68,7.31,6.95,6.28,6.02,5.92,4.32,3.98,2.88]):
    """ This should return a list of possible english text
        result = msg from decrypt to test
        etaoin_shrdlu = averages used for character test"""
    
    a = len(result)
    single = []
    for i in range(12):
        single.append(9999)
    total = 0
    single[0]= result.count(b'e') + result.count(b'E')
    single[1]= result.count(b't') + result.count(b'T')
    single[2]= result.count(b'a') + result.count(b'A')
    single[3]= result.count(b'o') + result.count(b'O')
    single[4]= result.count(b'i') + result.count(b'I')
    single[5]= result.count(b'n') + result.count(b'N')
    single[6]= result.count(b's') + result.count(b'S')
    single[7]= result.count(b'h') + result.count(b'H')
    single[8]= result.count(b'r') + result.count(b'R')
    single[9]= result.count(b'd') + result.count(b'D')
    single[10]= result.count(b'l') + result.count(b'L')
    single[11]= result.count(b'u') + result.count(b'U')

    for i in range(12):
        if single[i] == 0:
            single[i] =100
        else:
            single[i] = single[i]/a
    for i in single:
        total = total + i
   
    return total, single

    
def xorsingle(msg,xor,best=3):
    """Returns a tuple with lists enclosed.
    The lists hold first the xor byte used, the decrypt msg and the score
    Default is best 3 scores. """
    # Variables
    holdresult = {}
    rank = []
    dictreturn = {}
    # msg to bytes if not already
    if type(msg)== type(' '):
        msg = bytes.fromhex(msg)
   
    # Run Xor and produce bytearray
    for i in range(len(xor)):
        result = bytearray(len(msg))
        for j in range(len(msg)):
            result[j] = msg[j] ^ int.from_bytes(xor[i],"big")
        #convert to bytes to make immutable
        result = bytes(result)
        # Run english language test
        # Can change this in future to other languages
        total, single = englishtest(result)
        # total is the score value as a float
        # (FOR DEBUG )single is the list of numbers used to produce totat result
        # print(total)
        # creates dictionary of key value score and XOR msg list
        try:
            holdresult[total].append(xor[i])
        except:
            holdresult[total] = []
            holdresult[total].append(xor[i])
        
    # Creates rank of scores
    for i in holdresult.keys():
        rank.append(i)

    # Sorts scores
    rank.sort()

    # Takes best scores
    rank = rank[0:best]
    # Generates dictionary of best results
    for i in range(best):
        dictreturn[rank[i]] = holdresult[rank[i]]
    
    # Frees memory from holdresult (all 256 XORs)
    del holdresult
    # Creates ranked dictionary with key = score and list[byte,msg]
    resultdict = {}
    for i in rank:
        resultdict[i] = []
        for j in dictreturn[i]:
            normal = []
            normal.append(j)
            resultdict[i].append(xormsg(msg,normal))
    # Create a tuple of lists
    # List will be in order of byte, score and msg
    rank = []
    for i in resultdict.keys():
        rank.append(i)
    rank.sort()
    final = []
    for i in rank:
        for j in resultdict[i]:
            final.append([j[0],i,j[1]])
    final = tuple(final)
    print ("*",end='.')
    return final

def xormsg(msg,xor):
    """ This is to print the msg.  Xor must be part of a list"""

    bytelist = []
    if type(msg)== type(' '):
        msg = bytes.fromhex(msg)
   
    for i in range(len(xor)):
        result = bytearray(len(msg))
        for j in range(len(msg)):
            result[j] = msg[j] ^ int.from_bytes(xor[i],"big")
        result = bytes(result)
        bytelist.append(result)
        rettup = (xor[i],bytelist)
        

    return rettup
