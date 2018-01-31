#!/usr/bin/python3.4m


from msg import convert      # grab convert to ensure byte level
# from msg import englishtest  # grab englishtest to test msg
from msg import defs

# Get encoding string
# HARDCODE
origmsg='0x1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
# Because msg is hex, should be taken apart number by number and put back together
#  -- OR --
# msg.bytes.fromhex(msg) **-- This one works and is less work --**
# convert takes care of this
# Feed to convert to ensure it's bytes
msg = convert.msg_to_raw(origmsg,override='hex')
# Test type to ensure it's bytes
if type(msg) != bytes:
    print('This should fail because msg was not converted properly.\n',
          'Msg was type ', type(msg))
# Generate single XOR list to test
xorIter = defs.xor_iter()
best = {xorIter[0]:(0,b'No msg')}   # This places something in for rank
# Set x number to hold in best
x = 3
for i in xorIter:
# Apply XOR and get result
    result, xor = defs.xor(msg,i)
    # Score printable characters
    total = defs.character_check(result)
    
    # Test and score against englishtest
    total = total + defs.englishtest(result)
    print('Total score: ' + str(total))
    print(str(total) + ' ' + str(xor))
    # Store dictionary of best score to XOR

    # Set rank list
    rank = []
    for i in best.keys():
        rank.append(best[i][0])
    rank.sort()
    # Check if holding too much
    if len(best) < x:      
        best.update({xor:(total,result)})
    elif total > rank[0]:
        pop = []
        for i in best.keys():
            if best[i][0] == rank[0]:
                pop.append(i)
        best.pop(pop[0])
        best.update({xor:(total,result)})
    
# Display best score(s)
print(best, end='\n\n\n')
rank = []
for i in best.values():
    rank.append(i[0])
rank.sort()
for i in best.keys():
    if best[i][0] == rank[len(rank) - 1]:
        print(i, best[i][1], best[i][0])
        

