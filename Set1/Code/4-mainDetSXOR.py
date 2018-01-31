#!/usr/bin/python3

from msg import defs
from msg import convert
import time
import subprocess
t1 = time.time()

file = "/home/jason/Projects/Crypto/Set1/detectSingleXOR.txt"


class DCRYPT:
    """To Test class creation for iteration"""

    def __init__(self):
        # To hold the type of crypto msg (eg. hex, base64 etc.)
        self.MSG_TYPE = ""
        self.WORK_MSG = ""  # To hold msg worked on
        self.WORK_XOR = ""  # To hold iter being currently used
        self.LINE_NO = 0  # Sequence number to record line number
        self.BEST = {0: (hex(0), 0, b'No msg', '')}
        # Dict to hold best results
        # Will be held in form { seq_numb: xor, score, result,
        #                         original hex}
        self.ANSWER = {}  # Best answer for end

    def next_iter(self):
        """Next iteration of work"""
        self.LINE_NO += 1
        print(".", end="")

    def convert(self, msg, override='hex'):
        """Convert msg result into hex and place into self.WORK_MSG
    It is assumed that hex is the override of the msg"""
        if override == 'hex':
            self.WORK_MSG = convert.msg_to_raw(msg, override)

    def standard_xor(self):
        """To set standard xor 0 - 255"""
        self.WORK_XOR = defs.xor_iter()

    def run_single_xor(self, msg, i):
        return defs.xor(msg, i)

# Start of main

a = DCRYPT()
a.standard_xor()
counter = 0  # Initialize counter
num = 10  # Number of best to check
f = open(file)

# To test each line for secret msg

for line in f:
    a.convert(line)
    a.LINE_NO += 1
    for i in a.WORK_XOR:
        counter += 1
        result, xor = defs.xor(a.WORK_MSG, i)
        total = defs.character_check(result) + defs.englishtest(result)

        # Set rank list
        rank = []
        for j in a.BEST.keys():
            rank.append(a.BEST[j][1])
        rank.sort()

        # Check if holding too much
        if len(a.BEST) < num:
            a.BEST.update({counter: (i, total, result, line, a.LINE_NO)})
        elif total > rank[0]:
            pop = []
            for k in a.BEST.keys():
                if a.BEST[k][1] == rank[0]:
                    pop.append(k)
            if len(pop) != 0:
                a.BEST.pop(pop[0])
            a.BEST.update({counter: (i, total, result, line, a.LINE_NO)})

    if a.LINE_NO % 20 == 0:
        print('.', end='', flush=True)
#    os.system("echo -n .")
    # if a.LINE_NO % 20 == 0:
    #     subprocess.call(["echo", "-n", "."])
f.close()
t2 = time.time()

# Display best score(s)
# print(a.BEST, end='\n\n\n')  # To check dictionary left

rank = []
for i in a.BEST.keys():
    rank.append(a.BEST[i][1])
rank.sort()

# Number of sorted displayed
x = 3
print("\n\n")
for j in range(1, x + 1):
    for i in a.BEST.keys():
        if a.BEST[i][1] == rank[len(rank) - j]:
            if j == 1:
                a.ANSWER = (i, a.BEST[i][0], a.BEST[i][1],
                            a.BEST[i][2], a.BEST[i][3],
                            a.BEST[i][4]
                            )

            print("***********************************" +
                  "************************************")
            print("Result: " + str(a.BEST[i][2]) + "\n")
            print("Score: " + str(a.BEST[i][1]))
            print("Line: " + str(a.BEST[i][3]) +
                  "Line Number: " + str(a.BEST[i][4]) +
                  " XOR Used: " + str(bytes([a.BEST[i][0]])) +
                  " XOR Int is: " + str(a.BEST[i][0]))
            print("***********************************" +
                  "************************************")


print("Time to go through XOR = " + str(t2 - t1))
print("Through " + str(a.LINE_NO) + " msg(s)!!!")
print("Best answer is: " + str(a.ANSWER[3]))
