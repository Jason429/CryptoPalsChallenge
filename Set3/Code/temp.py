#! /usr/bin/python3

from msg.CBC_Pad_Oracle import Oracle_Server as Server

blocksize = 16
server = Server(blocksize)
e = server.encrypted



blocks = []
blocks.append(server.iv)       # You would not normally be able to get this.
                               # Hope for plain text knowledge of first block.
                               
for i in range(len(e) // blocksize):
    blocks.append(e[i * blocksize: i * blocksize + blocksize])

# Set working registers

test = bytearray(blocksize)

working_on = []
completed = [False for i in range(blocksize)]
known = bytearray(blocksize)
plaintext = bytearray()

for msg in range(len(blocks) -1, 0, -1):
    for i in range (-1, (blocksize * -1) - 1 , -1):
        working_on.append(i)

        for j in working_on:
            if completed[j] == True:
                test[j] = blocks[msg-1][j] ^ known[j] ^ (i * -1)
            else:
                # Getting a weird error intermittently
                # Sometimes it doesn't find a valid answer
                # Take below and make it a function.
                # Attempt three times then quit.
                
                for bit_test in range(0,256):
                    #print(bit_test)
                    test[j] = blocks[msg-1][j] ^ (i * -1) ^ bit_test
                    result = server.test_padding(blocks[msg], test)
                    if result == "VALID":
                        known[j] = bit_test
                        completed[j] = True
                        print(known)
                        break
            
            if completed[j] != True:
                print("Something failed")
                print("working_on", working_on)
                print("completed", completed)
                print("test", test)
                print("result", result)

    working_on = []
    completed = [False for i in range(blocksize)]
    print(msg)
    plaintext = known + plaintext
    known = bytearray(blocksize)


print(plaintext)
print("\n")

    
               

