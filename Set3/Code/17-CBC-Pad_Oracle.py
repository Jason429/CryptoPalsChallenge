#! /usr/bin/python3

from msg.CBC_Pad_Oracle import Oracle_Server as Server


print("""\nThis function is not perfect.  On rare occasion blocks will get dropped due to
multiple possibilities.  Current rates are 0.5% dropped packet rates.  This is acceptable
but perfect decryption is prefered.""")
print("""\nOutput in results will show how many calls to the server are made over the course
of the decryption.  To minimize this, make changes to CBC_Pad_Oracle.work (in package) to
not test all 256 bit choices and instead return on first valid.  This will of course increase
the error/decrypt failure rate.  This is done by inserting break upon a valid hit.  
(Brings approx 12000 calls down to 4000!)

(Error rate on first valid is approx 1.8% (on 1700 trials)

Trading sneakiness for errors.\n""")
blocksize = 16
server = Server(blocksize)
e = server.encrypted

print("Encrypted msg:\n\n",e, "\n")



blocks = []
blocks.append(server.iv)       # You would not normally be able to get this.
                               # Hope for plain text knowledge of first block.
                               
for i in range(len(e) // blocksize):
    blocks.append(e[i * blocksize: i * blocksize + blocksize])

# Set working registers

# test = bytearray(blocksize)
test = bytearray(blocksize)
working_on = []
completed = [False for i in range(blocksize)]
known = [[0 for x in range(blocksize)]]
plaintext = []
final_working_on = 0
image = ["|","\\","-",'/']
num= 0
server_calls = 0

for msg in range(len(blocks) -1, 0, -1):
    for i in range (-1, (blocksize * -1) - 1 , -1):
        working_on.append(i)
        num_to_pop = len(known)
        for known_no in range(len(known)):
        
            for j in working_on:
                if completed[j] == True:
                    try:
                        test[j] = blocks[msg-1][j] ^ known[known_no][j] ^ (i * -1)
                    except:
                        print("known shrinking")
                else:
                    final_working_on = j
                    result, calls = server.work(test, blocks, i, j, msg)
                    server_calls += calls
                    if result == None:
                        print("\r",end='',flush=True)
                        print(image[num % 4],end='',flush=True)
                        num += 1
                        break

                    if len(result) == 1:
                        known[known_no][j] = result[0]
                        known.append(known[known_no])
                        print("\r", " " * 80, end = '', flush=True)
                        print("\r", str(bytearray(known[known_no])),end = '', flush=True)
                        break
                    if len(result) > 1:
                        for k in result:
                            hold = list(known[known_no])
                            hold[j] = k
                            known.append(hold)
                        break
        completed[final_working_on] = 1
        for k in range(num_to_pop):
            known.pop(0)

    # Reset registers
    print("\n")
    try:
        print("\r","Solved block: ", str(bytearray(known[0])),end='\n',flush=True)    # rm known_no
    except:
        error_file = open('/home/jason/Projects/Crypto/Set3/errors(short).txt', \
                          'a')
        error_file.write('Msg ' + str(server.string) + "\n")
        error_file.write('IV  ' + str(server.iv) + "\n")
        error_file.write('Key ' + str(server.key) + "\n")
        error_file.close()
    working_on = []
    completed = [False for i in range(blocksize)]
    # print(msg)
    plaintext = known + plaintext
    known = [[0 for x in range(blocksize)]]
    test = bytearray(blocksize)
    print("\n", flush=True)

print("\n")
end_print = []
for i in plaintext:
    end_print.extend(i)
print(bytearray(end_print))
print("Server Calls : ", server_calls)
print("\n")




# Turn on assert below to stop script.
# Leave off to have errors.txt generate over time.
#assert bytearray(end_print) == bytearray(server.string)    
f = open('/home/jason/Projects/Crypto/Set3/results(short).txt','a')
f.write('Server calls ' + str(server_calls) + "\n")
f.close()

