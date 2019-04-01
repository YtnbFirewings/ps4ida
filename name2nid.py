# name2nid
# SocraticBliss (R)
# Big thanks to zecoxao, flatz and IDC <3

from binascii import unhexlify as uhx, b2a_base64
from hashlib import sha1
import struct
import sys

NID_SUFFIX = uhx('518D64A635DED8C1E6B039B1C3E55230')

def name_to_nid(name):
    symbol = sha1(name + NID_SUFFIX).digest()
    id = struct.unpack('<Q', symbol[:8])[0]
    encoded_id = b2a_base64(uhx('%016x' % id))[:-2]
    return encoded_id.replace('/','-')

def main(argc, argv):
     if argc != 2:
        raise SystemExit('\nUsage : python name2nid.py <names file>')
     
     try:
         with open(argv[1]) as file:
             names = file.read().split('\n')
     except:
        raise SystemExit('\nError: unable to read input file!')
     
     for name in names:      
        encoded_id = name_to_nid(name)
        print('name: %s\nNID: %s' % (name, encoded_id))

if __name__=='__main__':
    main(len(sys.argv), sys.argv)