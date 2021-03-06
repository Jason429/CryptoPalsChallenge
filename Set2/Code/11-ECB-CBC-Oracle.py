#! /usr/bin/python3

# Need to test encryption and decryption of AES - CBC and EBC modes
#  first before we run the encryptor (just to verify)
from msg import AES
from random import randint


class Encryption_Oracle:
    """This is a object that generates a random msg encrypted under AES 128
eBC or CBC. (Do I want to leave this as an object?  Or just as a large funciton.)

In msg (in bytes/bytearray) Out prepended and random.  Where is the key and iv
it used?  In order to check, need that info (for debug).
That's why I will use an object with a function.  Once completed, they I
can look at exporting only the desired function.
It has the following exposed functions and attributes.

! .key = key used to encrypt AES
! .iv = iv used for CBC mode. (still created if in EBC)
! .org_msg = msg that was inserted
! .msg = msg that was encrypted with prepend and append of random 5-10 bytes
! .mode = The resulting mode used for encrypting (EBC or CBC)
! .result = encrypted result of action
"""

    def __init__(self, msg, makeblock=128):
        """Takes msg in bytes or bytearray to create randomly encrypted msg
with a prepend of 5-10 bytes and a append of 5-10 bytes (both random).
Standard is size 128."""
        self.key = self._randomKeyOrIV()
        self.iv = self._randomKeyOrIV()
        self.org_msg = msg
        self.mode = self._randomMode()

        # Created for prepending and appending msg
        prependmsg = bytearray()
        appendmsg = bytearray()
        for i in range(randint(5, 10)):
            prependmsg.append(randint(0, 255))
        for i in range(randint(5, 10)):
            appendmsg.append(randint(0, 255))

        self.msg = prependmsg + self.org_msg + appendmsg
        del prependmsg, appendmsg
        # Run the encryption and get result
        if self.mode == 'EBC':
            self.result = AES.encryptMsg(self.msg, self.key)
        if self.mode == 'CBC':
            self.result = AES.encryptMsgCBC(self.msg, self.key, self.iv)

        # .result is returned

    def _randomMode(self):
        """Picks a random number for which mode to encrypt with.
0 = EBC
1 = CBC
"""
        mode = randint(0, 1)
        if mode == 0:
            return 'EBC'
        if mode == 1:
            return 'CBC'

    def _randomKeyOrIV(self, makeblock=128):
        """Creates a random key or IV block.  Default is set to 128"""
        k = bytearray()
        for i in range(16):
            k.append(randint(0, 255))
        return k


def testForEBC(result, makeblock=128):
    """Take result and test to see if EBC mode is on.
If not, assume that it's CBC.
Return string of mode suspected"""
    result_list = []
    if makeblock == 128:
        for i in range(0, len(result), 16):
            result_list.append(result[i:i + 16])
    for i in range(len(result_list) - 1):
        if result_list[i] == result_list[i + 1]:
            return 'EBC'
        # Optimize by not going through all
        # Return CBC as assumed
        if i > len(result) * .80:
            return 'CBC'
    # In case *.80 doesn't fire because length is too short
    return 'CBC'

if __name__ == '__main__':
    msg = b'Yellow Submarine'
    print("The message being used is {}".format(msg))
    a = Encryption_Oracle(msg)
    print("The mode is {}".format(a.mode))
    print("The key was {}".format(a.key))
    print("The iv was {}".format(a.iv))
    print("\nThe original msg was {}".format(a.org_msg))
    print("The result of encrypting the msg was\n{}".format(a.result))
