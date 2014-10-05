#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    [AnKoA] Made with love by grm34 (FRIPOUILLEJACK)

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
    modify and/or redistribute the software under the terms of the CeCILL-C
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

import re
import os
import sys
import commands
import optparse
from django.utils.encoding import (smart_str, smart_unicode)
from app.main.events import (make_help, global_error, bad_source)
from user.settings import option

(folder, thumb, tag, team, announce, tmdb_api_key, tag_thumb) = option()


# ANKOA TOOLS
def ankoa_tools(thumb, title, year, stag, mark, audiolang, prezquality,
                titlesub, subforced, nfosource, nfoimdb, name):
    return (
        "./make.py {0}{1}.{2}{3}{4} {1} {2} {5} {6} {7} {8} {9} {10} {11}"
        .format(thumb, title, year, stag, mark, audiolang, prezquality,
                titlesub, subforced, nfosource, nfoimdb, name))


# MANUAL TOOLS
def main():

    # HELP
    usage = make_help()
    parser = optparse.OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    if (len(args) != 5 and len(args) != 11):
        parser.print_help()
        parser.exit(1)

    source = sys.argv[1]

    # MANUAL TOOLS VALUES
    if (len(args) == 5):
        rls_source = sys.argv[2]
        sub = sys.argv[3]
        forced = sys.argv[4]
        url = sys.argv[5]

    # AUTO TOOLS VALUES
    else:
        title = sys.argv[2]
        year = sys.argv[3]
        audiolang = sys.argv[4]
        prezquality = "{0} {1}".format(sys.argv[5], sys.argv[6])
        titlesub = sys.argv[7]
        subforced = sys.argv[8]
        nfosource = sys.argv[9]
        nfoimdb = sys.argv[10]
        name = sys.argv[11]

    # Release Size & torrent pieces
    def check_size():
        try:
            scan_s = "mediainfo -f --Inform='General;%FileSize/String4%'"\
                     " {0}".format(source)
            rls_size = smart_str(commands.getoutput("{0}".format(scan_s)))
            prezsize = rls_size.strip().replace(' ', '')
            regex = re.sub("\\D", '.', prezsize).split('.')[0]
            if ("gib" in prezsize.lower()):
                if (int(regex) < 2.5):
                    pieces = "20"
                elif (int(regex) > 2.5 and int(regex) < 3.5):
                    pieces = "21"
                else:
                    pieces = "22"
            elif ("mib" in prezsize.lower()):
                if (int(regex) < 400):
                    pieces = "18"
                elif (int(regex) > 400 and int(regex) < 650):
                    pieces = "19"
                else:
                    pieces = "20"
            else:
                pieces = "20"

        except OSError:
            prezsize = "Mo"
            pieces = "20"

        return (prezsize, pieces)

    # AUTO TOOLS PROCESS
    def auto_tools():
        (prezsize, pieces) = check_size()

        # Tools whith prez
        if (len(nfoimdb) == 7 and nfoimdb.isdigit()):
            prezz = "&& ./genprez.py {0} {1} {2} {3} {4} && mv {5}{6}"\
                    "*.txt {7}.txt && ./imgur.py {7}.png add "\
                    .format(audiolang, prezquality, titlesub, prezsize,
                            nfoimdb, thumb, name, source[:-4])

            zipp = "cd {0} && zip -r {3}.zip -m {3}*.torrent "\
                   "{3}.nfo {3}.txt {1}.{2}*.log {3}.png"\
                   .format(thumb, title, year, source.split('/')[-1][:-4])

        # Tools without prez
        else:
            prezz = "&& ./imgur.py {0}.png ".format(source[:-4])

            zipp = "cd {0} && zip -r {3}.zip -m {3}*.torrent "\
                   "{3}.nfo {1}.{2}*.log {3}.png"\
                   .format(thumb, title, year, source.split('/')[-1][:-4])

        # Return Tools
        return (
            "./thumbnails.py {3} 5 2 {4}&& ./nfogen.sh {3} {5} {6} {7} http:"
            "//www.imdb.com/title/tt{8} && rm -f {0}{1}.{2}*.mbtree && cd {0}"
            " && mktorrent -a {9} -p -t 8 -l {10} {3} && {11}"
            .format(thumb, title, year, source, prezz, nfosource,
                    titlesub, subforced, nfoimdb, announce, pieces, zipp))

    # MANUAL TOOLS PROCESS
    def manual_tools():
        return(
            "./thumbnails.py {0} 5 2 && ./nfogen.sh {0} {1} {2} {3}"
            " {4} && cd {5} && mktorrent -a {6} -p -t 8 -l 22 {0}"
            .format(source, rls_source, sub, forced, url, thumb, announce))

    # FINALLY
    try:
        # Run manual tools
        if (os.path.isfile(sys.argv[1]) is True and len(args) == 5):
                os.system(manual_tools())

        # Run auto tools
        elif (os.path.isfile(sys.argv[1]) is True and len(args) == 11):
            os.system(auto_tools())

        # Source not found
        else:
            bad_source()

    # make Error
    except OSError as e:
        global_error(e)
        sys.exit()

if (__name__ == "__main__"):
    main()
