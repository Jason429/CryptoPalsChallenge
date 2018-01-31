#! /usr/local/bin/python3

import string
from base64 import b64decode
from random import randint

from itertools import zip_longest, product

from msg.defs import array_quality, xor, xor_iter
from msg.CTR import ctr_crypt

STRING_QUALITY = 0.95  # Percentage of printable in xor test
STRING_TEST = None     # Set if you want custom string to test in msg
#                        Must be in bytes or bytearray
TOP_ANS = 3            # Top num answers from xor
WORDS = []             # List of words to look for
WORD_FILE = "./msg/top_1000_words.txt"

with open(WORD_FILE, 'r') as f:
    WORDS = tuple([bytes(x.rstrip('\n').lower(), encoding='utf8')
                   for x in f.readlines()])

strings = []
with open('20_input_file.txt', 'r') as f:
    for line in f.readlines():
        j = line.rstrip('\n')
        strings.append(j)

b_strings = [b64decode(x) for x in strings]
cipher_key = bytes()
# b_strings is not encrypted!!!  Encrypt with random

for i in range(16):
    cipher_key += bytes([randint(0, 255), ])

result = [ctr_crypt(x, cipher_key) for x in b_strings]
max_len_result = max(map(len, result))
test_list = []

# To hold final lines.  Key = line
final_answer = {}
for i in range(len(result)):
    final_answer[i] = bytes()

# ########## Area for chunks ##########
for chunk in range(0, max_len_result, 16):

    # First take first 16 of everything in result
    # TODO: Ability to change size of block required for other encryption
    first = [x[chunk:chunk + 16] for x in result]

    print("[+] Starting itertools and getting top answers")
    combos = []
    MODIFIER = 0
    while len(combos) == 0:
        # Look at using itertools.zip_longest for different sized messages
        # IT DIED IN HERE!!!!!
        it_long = zip_longest(*first)
        to_test = []
        for i in it_long:
            top_ans = {}

            # This is any char that are part of that length
            cleaned = tuple(x for x in i if x is not None)  # one tuple of zip
            for j in xor_iter():
                ans, num = xor(cleaned, j)
                aq = array_quality(ans, STRING_TEST)
                if aq > (STRING_QUALITY - MODIFIER):
                    top_ans[num] = aq
                    top = sorted(top_ans.values(), reverse=True)[0:TOP_ANS]
            to_test.append([k for k, v in top_ans.items() if v in top])

        total = sum([len(i) for i in to_test])
        print(f"Sum of possible variables {total}")
        if total > 200:
            print("There are over 200 possible variables.\n" +
                  "This WILL take a while.\n" +
                  "(Consider tweeking array_quality func to be more" +
                  "specific on good chars)\n" +
                  "CONTINUE? (y for yes")
            ans = input()
            if ans[0].lower() != 'y':
                print('Exiting.\nHere are the results')
                for i in sorted(final_answer.keys()):
                    print(final_answer[i])

        combos = [b''.join(x) for x in product(*to_test)]
        if len(combos) == 0:
            MODIFIER += 0.001
            print(f"Dropping STRING_QUALITY to {STRING_QUALITY - MODIFIER}.")

    finals = []
    print(f"[+] Done getting top answers.  Total {len(combos)} combinations.")

    print("[+] Starting checking printability")
    printable = bytes(string.printable, encoding='utf8')
    for i in combos:
        final = True
        for line in first:
            ans, test = xor(line, i)
            for j in range(len(ans)):
                if ans[j] not in printable:
                    final = False
                    break
                if j != (len(ans) - 1) and ans[j] == b'\r' and \
                        ans[j:j + 1] != b'\r\n':
                    final = False
                    break
            if not final:
                break

        if final:
            finals.append(i)

    # finals hold all that will be within the word check.

    print(f"[+] Total of {len(finals)} to run through words")
    # ########################################
    # To check against word list
    # ########################################
    best = []
    for i in finals:
        total = 0
        for line in first:
            ans, test = xor(line, i)
            ans = [x.lower() for x in ans.split(b' ')]
            for j in ans:
                if j in WORDS:
                    total += 1
        best.append((total, test))
        # Check best length and get rid of numbers too low.
        if len(best) > 10:
            best = sorted(best, reverse=True)
            best.pop()
    best = sorted(best, reverse=True)

    for i in range(len(first)):
        ans, _ = xor(first[i], best[0][1])
        final_answer[i] = final_answer[i] + ans
        # print(ans)
    for i in sorted(final_answer.keys()):
        print(final_answer[i])

# Produce the best 5? printable characters for each 16 positions
#  Must be 90% Printable or more (a list of lists, each pos per byte pos)

# Generate combinations for each line and test against
#      english freq and printability of all lines

# Print the top three results (using input)

#
