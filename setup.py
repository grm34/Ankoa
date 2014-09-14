#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#------------------  AnKoA  -----------------------#
#     Made with love by grm34 (FRIPOUILLEJACK)     #
#     ........fripouillejack@gmail.com .......     #
# Greetz: thibs, Rockweb, c0da, Hydrog3n, Speedy76 #
#--------------------------------------------------#

import os
import sys
import optparse
sys.path.append("app/")
from style import color

(BLUE, RED, YELLOW, GREEN, END) = color()

def main():
    usage = "./setup.py SOURCE_PATH RESULT_PATH TEAM TK_ANNOUNCE TMDB_API_KEY"

    parser = optparse.OptionParser(usage = usage)
    (options, args) = parser.parse_args()
    if (len(args) != 5):
        parser.print_help()
        parser.exit( 1 )

    source = sys.argv[1]
    result = sys.argv[2]
    team = sys.argv[3]
    tk = sys.argv[4]
    api = sys.argv[5]

    #---> AUTHORIZE & CLEAN <---#
    chmod = ("chmod +x * && cd app/ && chmod +x * && cd ..")
    rm = ("rm setup.py")
    os.system(chmod)

    #---> WRITE settings <---#
    f = file('app/settings.py', 'r')
    chaine = f.read()
    f.close()
    data = chaine.replace("XXX001", source).replace("XXX002", result)\
                 .replace("XXX003", team).replace("XXX004", tk)\
                 .replace("XXX005", api)
    f = file('app/settings.py', 'w')
    f.write(data)
    f.close

    #---> WRITE nfogen <---#
    ff = file('nfogen.sh', 'r')
    chaine = ff.read()
    ff.close()
    data = chaine.replace("XXX002", result)
    ff = file('nfogen.sh', 'w')
    ff.write(data)
    ff.close

    os.system(rm)

    print (BLUE+"AnkoA "+RED+"=> "+GREEN+"Installation successful !"+END)

if (__name__ == "__main__"):
    main()