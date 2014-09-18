#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#-------------------- [ AnKoA ] -------------------#
#     Made with love by grm34 (FRIPOUILLEJACK)     #
#--------------------------------------------------#
"""
    Copyright PARDO Jérémy (Sept 2014)
    Contact: jerem.pardo@gmail.com

    This software is a computer program whose purpose is to help command
    line encoders. Intuitive command line interface with many tools:

    * FFMPEG easy encoding
    * Thumbnails Generator
    * NFO Generator
    * Genprez Upload
    * Auto make .torrent

    This software is governed by the CeCILL-C license under French law and
    abiding by the rules of distribution of free software.  You can  use,
    modify and/ or redistribute the software under the terms of the CeCILL-C
    license as circulated by CEA, CNRS and INRIA at the following URL
    "http://www.cecill.info".

    As a counterpart to the access to the source code and  rights to copy,
    modify and redistribute granted by the license, users are provided only
    with a limited warranty  and the software's author,  the holder of the
    economic rights,  and the successive licensors  have only  limited
    liability.

    In this respect, the user's attention is drawn to the risks associated
    with loading,  using,  modifying and/or developing or reproducing the
    software by the user in light of its specific status of free software,
    that may mean  that it is complicated to manipulate,  and  that  also
    therefore means  that it is reserved for developers  and  experienced
    professionals having in-depth computer knowledge. Users are therefore
    encouraged to load and test the software's suitability as regards their
    requirements in conditions enabling the security of their systems and/or
    data to be ensured and,  more generally, to use and operate it in the
    same conditions as regards security.

    The fact that you are presently reading this means that you have had
    knowledge of the CeCILL-C license and that you accept its terms.
"""

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