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

import os
import sys
import subprocess
sys.path.append("app/")
from system import ANKOA_SYSTEM
from style import (banner, next, color)

(BLUE, RED, YELLOW, GREEN, END) = color()


def main():

    # RUN ANKOA
    banner()
    (
        source, thumb, team, announce, title, year, stag, string, codec,
        encode_type, crf, bit, level, idvideo, fps, interlace, interlace2,
        audiolang, audio_config, sub_config, sub_remux, reso, param, pass1,
        mark, nfoimdb, nfosource, titlesub, subforced, prezquality,
        name, pprint
    ) = ANKOA_SYSTEM()

    # FFMPEG CLI
    def ffmpeg():
        if (encode_type == "2"):    # CRF
            return (
                "cd {0} && ffmpeg -i {1} -metadata title='{2}.{3}' -metadata "
                "proudly.presented.by='{4}' -map 0:{5}{6}{7} -metadata:s:v:0 "
                "title= -metadata:s:v:0 language= -f {8}{9} -c:v:0 {10} -crf "
                "{11} -level {12}{13}{14}{15} -passlogfile {2}.{3}.log "
                "{2}.{3}{16}{17}{18}"
                .format(thumb, source, title, year, team, idvideo, interlace,
                        fps, string, reso, codec, crf, level, param,
                        audio_config, sub_config, stag, mark, sub_remux))

        else:                       # 2PASS
            return (
                "cd {0} && ffmpeg -i {1} -pass 1 -map 0:{2}{3}{4} -f {5}{6} -"
                "c:v:0 {7} -b:v:0 {8}k -level {9}{10} -an -sn -passlogfile "
                "{11}.log {11}.{12}{13}{14} && ffmpeg -y -i {1} -pass 2 -meta"
                "data title='{11}.{12}' -metadata proudly.presented.by='{15}'"
                " -map 0:{2}{16}{4} -metadata:s:v:0 title= -metadata:s:v:0 la"
                "nguage= -f {5}{6} -c:v:0 {7} -b:v:0 {8}k -level {9}{17}{18}"
                "{19} -passlogfile {11}.{12}.log {11}.{12}{13}{14}{20}"
                .format(thumb, source, idvideo, interlace2, fps, string, reso,
                        codec, bit, level, pass1, title, year, stag, mark,
                        team, interlace, param, audio_config, sub_config,
                        sub_remux))

    # ANKOA TOOLS
    def ankoa_tools():
        return (
            "./make.py {0}{1}.{2}{3}{4} {1} {2} {5} {6} {7} {8} {9} {10} {11}"
            .format(thumb, title, year, stag, mark, audiolang, prezquality,
                    titlesub, subforced, nfosource, nfoimdb, name))

    print ankoa_tools()

    # ANKOA QUEUE
    run_ffmpeg = [ffmpeg(), "", "", "", "", "", "", "", "",
                  "", "", "", "", "", "", "", "", "", "", ""]

    run_ankoa_tools = [ankoa_tools(), "", "", "", "", "", "", "", "",
                       "", "", "", "", "", "", "", "", "", "", ""]

    n = 1
    if (pprint == "y"):
        print ffmpeg()

    again = raw_input("{0}NEXT ENCODE {1}(y/n){0} : {2}"
                      .format(GREEN, YELLOW, END))

    # QUEUE PROCESS
    while (again == "y"):
        next()
        (
            source, thumb, team, announce, title, year, stag, string, codec,
            encode_type, crf, bit, level, idvideo, fps, interlace, interlace2,
            audiolang, audio_config, sub_config, sub_remux, reso, param, pass1,
            mark, nfoimdb, nfosource, titlesub, subforced, prezquality,
            name, pprint
        ) = ANKOA_SYSTEM()

        run_ffmpeg[n] = ffmpeg()
        run_ankoa_tools[n] = ankoa_tools()

        n = n + 1
        if (n != 20):
            again = raw_input("{0}NEXT ENCODE {1}(y/n){0} : {2}"
                              .format(GREEN, YELLOW, END))
        else:
            break

    # RUN ANKOA PROCESS
    for i in range(n):
        try:
            os.system(run_ffmpeg[i])
            os.system(run_ankoa_tools[i])
            i = i + 1
        except OSError as e:
            print ("{0} -> {1}ERROR : {2}{4}{3}"
                   .format(GREEN, BLUE, RED, END, str(e)))
            sys.exit()

    print ("{0} ->{1} ENCODE(s) DONE, CONGRATULATIONS !\n{0} ->{1} NFO, THU"
           "MBNAILS, (PREZ) & TORRENT CREATED !{2}".format(RED, GREEN, END))

    sys.exit()

if (__name__ == "__main__"):
    main()
