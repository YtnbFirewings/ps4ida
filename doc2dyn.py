# doc2dyn
# SocraticBliss (R)

import json
import os
import sys

def main():
    with open('dynlib.xml', 'w') as xml:
        # Create the XML Header
        xml.write('<?xml version="1.0"?>\n')
        xml.write('<DynlibDatabase>\n')

        nids = []
        # Walk the directories searching for json files
        for root, dirs, files in os.walk('.'):
            for file in [f for f in files if f.endswith('.json')]:
                with open(os.path.join(root, file), 'r') as file:
                    data = json.load(file)

                    # Iterate through all the libraries in the module
                    for libraries in data['modules']:
                        library = libraries['libraries'][0]['name']

                        # Iterate through all the symbols in the library 
                        for symbols in libraries['libraries'][0]['symbols']:
                            obfuscated = symbols['encoded_id']
                            symbol = symbols['name']
                            
                            # Save the Populated Unique Entries
                            if obfuscated not in nids and symbol is not None:
                                xml.write('    <Entry obf=\"%s\" lib=\"%s\" sym=\"%s\"/>\n' % (obfuscated, library, symbol))
                                nids.append(obfuscated)

        # Close the XML Header
        xml.write('</DynlibDatabase>')

if __name__=='__main__':
    sys.exit(main())