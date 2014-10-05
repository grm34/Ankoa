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
import optparse
import subprocess
from user.settings import option
from app.system import ANKOA_SYSTEM
from app.skin.style import (banner, next)
from app.main.events import (ankoa_help, global_error, ankoa_success,
                             muxing_process, muxing_success, ffmpeg_success)
from app.main.inputs import (ask_next_encode, ask_print_ffmpeg, check_cmds,
                             ask_print_mkvmerge, ask_print_tools)
from app.modules.ffmpeg import *
from app.main.main import MKVMERGE
from make import ankoa_tools

(folder, thumb, tag, team, announce, tmdb_api_key, tag_thumb) = option()


def CHECK_COMMANDS_LINES(cmd, mkvmerge, tools):
    ask_cmds = check_cmds()
    if (ask_cmds == "y"):
        print_ffmpeg = ask_print_ffmpeg()
        if (print_ffmpeg == "y"):
            print cmd
        if (mkvmerge):
            print_mkvmerge = ask_print_mkvmerge()
            if (print_mkvmerge == "y"):
                print mkvmerge
        print_tools = ask_print_tools()
        if (print_tools == "y"):
            print tools


def main():

    # HELP
    usage = ankoa_help()
    parser = optparse.OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    if (len(args) != 0):
        parser.print_help()
        parser.exit(1)

    # ANKOA SYSTEM
    banner()
    (
        source, title, year, stag, string, codec, encode_type, crf,
        bit, level, idvideo, fps, interlace, interlace2, audiolang,
        audio_config, sub_config, reso, param, pass1, mark, nfoimdb,
        nfosource, titlesub, subforced, prezquality, name, subtype,
        audiotype, extend, sync, titlesub, charset, idsub, forced,
        sync2, titlesub2, charset2, idsub2, subsource
    ) = ANKOA_SYSTEM()

    # FFMPEG CRF
    if (encode_type == "3"):
        cmd = ffmpeg_crf(thumb, source, title, year, team, idvideo,
                         interlace, fps, string, reso, codec, crf,
                         level, param, audio_config, sub_config, stag, mark)
    # FFMPEG 2PASS
    else:
        cmd = ffmpeg_2pass(thumb, source, idvideo, interlace2, fps, string,
                           reso, codec, bit, level, pass1, title, year, stag,
                           mark, team, interlace, param, audio_config,
                           sub_config)
    # MKVMERGE
    mkvmerge = MKVMERGE(subtype, audiotype, thumb, title, year, stag, mark,
                        extend, sync, titlesub, charset, idsub, forced,
                        sync2, titlesub2, charset2, idsub2, subsource)

    # ANKOA TOOLS
    tools = ankoa_tools(thumb, title, year, stag, mark, audiolang, prezquality,
                        titlesub, subforced, nfosource, nfoimdb, name)

    # ANKOA QUEUE
    run_ffmpeg = [cmd, "", "", "", "", "", "", "", "", "", "", "", "",
                  "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    if (mkvmerge):
        run_mkvmerge = [mkvmerge, "", "", "", "", "", "", "", "", "",
                        "", "", "", "", "", "", "", "", "", "", "",
                        "", "", "", "", "", ""]
    run_ankoa_tools = [tools, "", "", "", "", "", "", "", "", "", "", "", "",
                       "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    n = 1

    CHECK_COMMANDS_LINES(cmd, mkvmerge, tools)

    # ANKOA PROCESS
    again = ask_next_encode()
    while (again == "y"):
        next()
        (
            source, title, year, stag, string, codec, encode_type, crf,
            bit, level, idvideo, fps, interlace, interlace2, audiolang,
            audio_config, sub_config, reso, param, pass1, mark, nfoimdb,
            nfosource, titlesub, subforced, prezquality, name, subtype,
            audiotype, extend, sync, titlesub, charset, idsub, forced,
            sync2, titlesub2, charset2, idsub2, subsource
        ) = ANKOA_SYSTEM()

        run_ffmpeg[n] = cmd
        if (mkvmerge):
            run_mkvmerge[n] = mkvmerge
        run_ankoa_tools[n] = tools
        n += 1

        CHECK_COMMANDS_LINES(cmd, mkvmerge, tools)

        if (n != 27):
            again = ask_next_encode()
        else:
            break

    # EXECUTE ANKOA
    for i in range(n):
        try:
            subprocess.check_output(run_ffmpeg[i], shell=True)
            ffmpeg_success()
            if (mkvmerge):
                muxing_process()
                os.system(run_mkvmerge[i])
                muxing_success()
            os.system(run_ankoa_tools[i])
            i += 1
            ankoa_success()

        # ANKOA ERROR
        except OSError as e:
            global_error(e)
            sys.exit()
        except subprocess.CalledProcessError as e:
            global_error(e)
            sys.exit()

    sys.exit()

if (__name__ == "__main__"):
    main()
