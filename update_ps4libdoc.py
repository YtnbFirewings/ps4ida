# A script for updating your ps4libdoc json files with additional names...
# SocraticBliss (R)
# Big thanks to zecoxao, flatz and IDC <3

from binascii import unhexlify as uhx, b2a_base64
from hashlib import sha1
import json
import os
import re
import struct
import sys

NID_SUFFIX = uhx('518D64A635DED8C1E6B039B1C3E55230')

def name_to_nid(name):
    symbol = sha1(name + NID_SUFFIX).digest()
    id = struct.unpack('<Q', symbol[:8])[0]
    encoded_id = b2a_base64(uhx('%016x' % id))[:-2]
    return encoded_id.replace('/','-')

def update_ps4libdocs():
    updates = {}
    with open('updates.txt', 'r') as dict:
         for line in dict:
             key,value = line.split(':')
             updates[key] = value.rstrip()
    
    # Walk the directories searching for ps4libdoc json files
    for root, dirs, files in os.walk('.'):
        for file in [f for f in files if f.endswith('.json')]:
            # Iterate through the input python dictionary for each ps4libdoc json file
            print('Processing %s...' % file)
            for key,value in updates.iteritems():
                with open(os.path.join(root, file), 'r+') as ps4libfile:
                    result, matches = re.subn(ur'("encoded_id": "%s",\n.*"name": )(null)' % re.escape(key),
                                              u"\\1\"%s\"" % value,
                                              ps4libfile.read(),
                                              re.M)
                    # If a match was found, update the ps4libdoc json file name (null) with the new name
                    if matches > 0:
                        print('%s was updated!' % file)
                        ps4libfile.seek(0)
                        ps4libfile.write(result)
                        ps4libfile.truncate()

# PROGRAM START
def main():
    
    # 1) Run name2nid and get a list of nid:names
    try:
        with open('names.txt', 'rb') as file:
             names = file.read().split('\n')
    except:
        raise SystemExit('\nError: unable to read input file!')
    
    with open('updates.txt', 'wb') as output:
        for name in names:
            encoded_id = name_to_nid(name)
            nidname = '%s:%s\n' % (encoded_id, name)
            output.write(nidname)
            #print(nidname)
    
    # 2) Update ps4libdocs with the newly found names
    update_ps4libdocs()
    
    # 3) ??? Profit!
    print('Done!')

if __name__=='__main__':
    sys.exit(main())