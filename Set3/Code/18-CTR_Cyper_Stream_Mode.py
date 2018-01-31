#! /usr/bin/python3

# Global imports

import struct
from base64 import b64decode, b64encode


# Package imports

from msg.CTR import ctr_crypt

string = b"L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu" + \
         b"/6/kXX0KSvoOLSFQ=="
d_string = b64decode(string)

print(ctr_crypt(d_string, b"YELLOW SUBMARINE"))
