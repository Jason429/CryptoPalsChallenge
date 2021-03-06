#! /usr/bin/python3.4m
import msg.convert as convert

class DCRYPT:
    """To Test class creation for iteration"""
    def __init__(self):
        self.MSG_TYPE = "" #To hold the type of crypto msg (eg. hex, base64 etc.)
        self.WORK_MSG = "" #To hold msg worked on
        self.WORK_XOR = "" #To hold iter being currently used
        self.LINE_NO = 0 # Sequence number to record line number or operation count
        self.BEST = {0 : (hex(0),0,b'No msg','')}
                        # Dict to hold best results
                        # Will be held in form { seq_numb: xor, score, result,
                        #                         original hex}
        self.ANSWER = {}  # Best answer for end
        self.SOLVE_BLOCKS = {}
        
    def next_iter(self):
        """Next iteration of work"""
        self.LINE_NO += 1
        print(".",end="")

    def convert(self,msg,override='hex'):
        """Convert msg result into hex and place into self.WORK_MSG
    It is assumed that hex is the override of the msg"""
        if override == 'hex':
            self.WORK_MSG = convert.msg_to_raw(msg,override)
    def standard_xor(self):
        """To set standard xor 0 - 255"""
        self.WORK_XOR = xor_iter()
    def run_single_xor(self,msg,i):
        return xor(msg,i)

def single(msg,xorIter,char_weight=1,eng_weight=1):
    """This uses old single bit XOR code to check for the best qualtity XOR.\n
This is to produce best block
msg = type(bytearray)
xorIter = Iter of Single byte Xors to use"""

    best = {xorIter[0]:(0,b'No msg')}   # This places something in for rank
    # Set x number to hold in best
    x = 1
    for i in xorIter:
    # Apply XOR and get result
        result, xor_answer = xor(msg,i)
        # Score printable characters
        total = character_check(result,char_weight)

        # Test and score against englishtest
        total = total + englishtest(result,eng_weight)

        rank = []
        for i in best.keys():
            rank.append(best[i][0])
        rank.sort()
        # Check if holding too much
        if len(best) < x:      
            best.update({xor_answer:(total,result)})
        elif total > rank[0]:
            pop = []
            for i in best.keys():
                if best[i][0] == rank[0]:
                    pop.append(i)
            best.pop(pop[0])
            best.update({xor_answer:(total,result)})
    # Return best score(s)

    return best
#############################################################    
def file():
    """Produces the file name"""
    return "/home/jason/Projects/Crypto/Set1/detectSingleXOR.txt"

def cleanmsg(msg, hexs=0, strip=0):
    """This is to ensure that msg is in bytes format.
--> Option to format from hex string and remove newline"""
    if type(msg) == type(bytes(b't')):
        return msg
    if type(msg) == type(' '):
        
        if hexs == 1:
            msg = msg.strip('\n')
            msg = bytes.fromhex(msg)
            return msg
        if strip == 1:
            msg = msg.strip('\n')
        if type(msg) != type(bytes(b't')):
            msg = msg.encode()
        return msg

def xor(msg,xor):
    """Msg need to be bytes and xor a list of ints or a byte/bytearray

This will run an XOR against a msg.
If the lengths don't match, the XOR pattern will look to the beginning of the XOR pattern"""

    result = bytearray(len(msg))
    for i in range(len(msg)):
        if type(xor) == type(1):        # Used for single XOR of int
            result[i] = msg[i] ^ xor
        else:                           # Used for multiple XOR (iter of ints)
            if i < len(xor):
                result[i] = msg[i] ^ xor[i]
            else:
                result[i] = msg[i] ^ xor[i%len(xor)]
    result = bytes(result)
    if type(xor) == type(1):
        return result , xor.to_bytes(1,"big")
    else:
        return result, xor

def xor_iter():
    """Returns bytes from 0 - 255 to test"""
    a = []
    for i in range(0,256,1):
        a.append(i)
    a = bytes(a)
    return a

def deviation(single,length,standard):
    """To see how close this is to english frequency.  Bigger numbers are better"""
    # Initialize var
    devi,percentfrom,percenttotal,work = 0,0,0,0
    # devi = percentage of character in string
    devi = single/length
    # work = difference between standard freq and current freq
    work = standard - devi
    # calculates percentage from standard using 0 as a base
    # negative numbers means extreme out of range
    percentfrom = standard - abs(work)
    # if statement to look for negative or division by zero
    if percentfrom < 0 or standard == 0:
        percenttotal = 0
    else:    # else to give a percentage
        percenttotal = percentfrom / standard
    return 100 * percenttotal # score is out of 100
    

def character_check(result,weight=1):
    """To score on printable characters"""

    total = 0
    a = len(result)
    for i in result:
        if i >= 48 and i <= 57:  # To check for number
            total += 1
        if i >= 65 and i <= 90:  # To check for Capital Letters
            total += 1
        if i >= 97 and i <= 122: # To check for lowercase letters
            total +=1
        if i == 32:              # To check for spaces
            total +=1
        if i == 39:             # To check for apostrophe
            total +=1            
    total = total / a
    # print(str(total) + ' ' + str(a))
    # print('Character check: ' + str(total * 100))
    return total * 10000 * weight

def dictionary(dictionary):
    """Returns dictionary in format key(int):(str(character),freq)"""
    if dictionary == 'english_utf8':
        a = {
            32:(b' ',0.19),
            39:(b"'",0.00),
            48:(b'0',0.00),
            49:(b'1',0.00),
            50:(b'2',0.00),
            51:(b'3',0.00),
            52:(b'4',0.00),
            53:(b'5',0.00),
            54:(b'6',0.00),
            55:(b'7',0.00),
            56:(b'8',0.00),
            57:(b'9',0.00),
            65:(b'A',0.0812),
            66:(b'B',0.0149),
            67:(b'C',0.0271),
            68:(b'D',0.0432),
            69:(b'E',0.1202),
            70:(b'F',0.0230),
            71:(b'G',0.0203),
            72:(b'H',0.0592),
            73:(b'I',0.0731),
            74:(b'J',0.0010),
            75:(b'K',0.0069),
            76:(b'L',0.0398),
            77:(b'M',0.0261),
            78:(b'N',0.0695),
            79:(b'O',0.0768),
            80:(b'P',0.0182),
            81:(b'Q',0.0011),
            82:(b'R',0.0602),
            83:(b'S',0.0628),
            84:(b'T',0.0910),
            85:(b'U',0.0288),
            86:(b'V',0.0111),
            87:(b'W',0.0209),
            88:(b'X',0.0017),
            89:(b'Y',0.0211),
            90:(b'Z',0.0007),
            97:(b'a',0.0812),
            98:(b'b',0.0149),
            99:(b'c',0.0271),
            100:(b'd',0.0432),
            101:(b'e',0.1202),
            102:(b'f',0.0230),
            103:(b'g',0.0203),
            104:(b'h',0.0592),
            105:(b'i',0.0731),
            106:(b'j',0.0010),
            107:(b'k',0.0069),
            108:(b'l',0.0398),
            109:(b'm',0.0261),
            110:(b'n',0.0695),
            111:(b'o',0.0768),
            112:(b'p',0.0182),
            113:(b'q',0.0011),
            114:(b'r',0.0602),
            115:(b's',0.0628),
            116:(b't',0.0910),
            117:(b'u',0.0288),
            118:(b'v',0.0111),
            119:(b'w',0.0209),
            120:(b'x',0.0017),
            121:(b'y',0.0211),
            122:(b'z',0.0007),
            }
        return a
    
def englishtest(result, eng_weight=1, dic='english_utf8'):
    """ This should return a list of possible english text
        result = msg from decrypt to test
        etaoin_shrdlu = averages used for character test"""

    # To set variables
    a = len(result)
    diction=dictionary(dic)
    # Make sure it matches the length of dictionary
    total = 0
    count = 0  # Used to place in single
    for i in diction.keys():
        # First do a count to figure out percentage
        count = result.count(i)
        total = total + deviation(count,a,diction[i][1])
    # print ('English test: ' + str(total))
    return total * eng_weight
    

def xormsg(msg,xor,hexs=0,strip=0):

    a = hexs
    b = strip
    # Below is to clean the msg to bytes format
    msg = cleanmsg(msg,hexs=a,strip=b)
    return msg, hexs, strip

def quality(answer):
    """This checks the quality of the answer.  Answer is in the form of
(XOR'd msg, XOR bits)"""
    qtotal = float(0)
    record = 1
    for i in range(len(answer[0])):
        if answer[0][i] >= 32 and answer[0][i] <=126:
            qtotal = qtotal + 1
    if qtotal / len(answer[0]) > 0.97:
        record = 1
    else:
        record = 0

    return record

def run(msg):
    """Run the xor program"""
    linecounter = 0
    it = xoriter() # This is added in to make it all work
    msg = cleanmsg(msg, hexs=1,strip=1)
    linecounter = linecounter + 1
    xmsg = [] # holds list of total (for englishtest), xor used, xmsg result
    for byte in range(len(it)):
         answer = ''
         record = 0
         english = ''
         answer = xor(msg,it[byte])
         record = quality(answer)
         if record != 0:
             english = englishtest(answer[0])
             xmsg.append([english[0],answer[1],answer[0]])
    return xmsg

def hamming_distance(msg1,msg2):
    """Send in strings of 0 and 1.  Result will count the
bits that are different"""
    if len(msg1) != len(msg2):
        return "Sorry. I need same lengths strings for this to work."
    count = 0
    for i in range(len(msg1)):
        if msg1[i] != msg2[i]: count += 1
    return count

def hamming_distance_test(msg,maxkeysize,maxbyte_iter):
    """To run over a message to generate a normalized result.
Returns dictionary and sorted lowest value results.\n
Lower result is normally the key\n
(msg,maxkeysize,maxbyte_iter)\n
msg - message to be checked as string of 0 and 1\n
maxkeysize - max keysize to check\n
maxbyte_iter - does this happen over most of the message
Requires hamming_distance(msg1,msg2) from same module"""
    a = {} # list of results
    b = []
    for i in range((2 * 8) ,((maxkeysize * 8) + 1), 8):
        j = maxbyte_iter
        lresult = []
        while j > 0:
            lresult.append((hamming_distance(msg[0:i],
                                            msg[i*j:i*(j+1)]
                                            )/i)
                           )
            ## [0:2], [(2*4):(2*5)]
            j -= 1
        a[i]=(sum(lresult))/maxbyte_iter
    b = list(a.values())
    b.sort()
    return a, b
    
            
def skip_gen(msg,skip,offset):
    """Creates new msg only using bytes fm skipped distance\n
Note that offset cannot be greater than skip\n
Msg needs to be in bytes or bytearray"""
    result = []
    count = 0
    while True:
        try:
            result.append(msg[(skip*count)+offset])
            count += 1
        except:
            break
    return bytearray(result)

def insert_gen(tomsg,fmmsg,skip,offset):
    """Insert one msg overtop of another in skipped distance\n
tomsg and fmmsg need to be bytearrays\n
skip and offset are ints.  offset needs to be less than skip\n"""
    count = 0
    while True:
        try:
            tomsg[(skip*count)+offset] = fmmsg[(skip*count)+offset]
        except:
            break
    return tomsg


    
    
        
    
        
