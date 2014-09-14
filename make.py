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
import subprocess
from subprocess import CalledProcessError, check_output
sys.path.append("app/")
from style import (banner, next, color)
from settings import option

(folder, thumb, tag, team, announce, tmdb_api_key, tag_thumb) = option()

(BLUE, RED, YELLOW, GREEN, END) = color()

def main():
    usage = "./make.py SOURCE.mkv SOURCE SUBS SUBFORCED URL"

    parser = optparse.OptionParser(usage = usage)
    (options, args) = parser.parse_args()
    if(len(args) != 5):
        parser.print_help()
        parser.exit(1)

    source = sys.argv[1]
    rls_source = sys.argv[2]
    sub = sys.argv[3]
    forced = sys.argv[4]
    url = sys.argv[5]

    process = "./thumbnails.py "+source+" 5 2 && ./nfogen.sh "+source+\
              " "+rls_source+" "+sub+" "+forced+" "+url+" && cd "+thumb+\
              " && mktorrent -a http://tk.gks.gs:6969/announce"\
              " -p -t 8 -l 22 "+source

    try:
        subprocess.check_output(process, shell=True)
        print (RED+"\n ->"+GREEN+" ALL JOBS DONE, CONGRATULATIONS !"+END)
        print (RED+" ->"+GREEN+" NFO, THUMBNAILS & TORRENT CREATED !\n"+END)
    except (OSError, CalledProcessError):
        print (GREEN+"\n -> "+BLUE+"ERROR : "+RED+"Bad source selection"\
               ", please try again !\n"+END)

if (__name__ == "__main__"):
    main()