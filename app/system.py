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
import json
import socket
import urllib2
import readline
import optparse
import commands
from json import loads
from urllib2 import (Request, urlopen, URLError, HTTPError, unquote)
from django.utils.encoding import (smart_str, smart_unicode)
from style import color
from settings import option
from bitrate import (calcul, calc)

(folder, thumb, tag, team, announce, tmdb_api_key, tag_thumb) = option()
(BLUE, RED, YELLOW, GREEN, END) = color()


def ANKOA_SYSTEM():

    # AUTO COMPLETE
    def completer(text, state):
        return (
            [entry.replace(' ', '\ ') for entry in os.listdir(
                folder + os.path.dirname(
                    readline.get_line_buffer())
                ) if entry.startswith(text)][state])

    # Select Source
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)
    prefix = raw_input("{0}RELEASE SOURCE > \n{1}".format(GREEN, END))
    while not prefix or os.path.isfile(folder+prefix) is False:
        print ("{0} -> {1}ERROR : {2}Bad source selection, please try"
               " again !{3}\n".format(GREEN, BLUE, RED, END))
        prefix = raw_input("{0}RELEASE SOURCE > \n{1}".format(GREEN, END))
    readline.parse_and_bind("tab: ")
    source = "{0}{1}".format(folder, prefix)

    # Release Title
    title = raw_input("{0}RELEASE TITLE {1}(ex: Hudson.Hawk){0} : {2}"
                      .format(GREEN, YELLOW, END))
    while not title:
        print ("\n{0} -> {1}ERROR : {2}Please, specify release title !{3}\n"
               .format(GREEN, BLUE, RED, END))
        title = raw_input("{0}RELEASE TITLE {1}(ex: Hudson.Hawk){0} : {2}"
                          .format(GREEN, YELLOW, END))

    # Release Year
    year = raw_input("{0}RELEASE PRODUCTION YEAR : {1}".format(GREEN, END))
    while not year or len(year) != 4 or year.isdigit() is False:
        print ("\n{0} -> {1}ERROR : {2}Please, specify valid release year !"
               "{3}\n".format(GREEN, BLUE, RED, END))
        year = raw_input("{0}RELEASE PRODUCTION YEAR : {1}"
                         .format(GREEN, END))

    # Special Tag
    special = raw_input("{0}SPECIAL TAG {1}(ex: EXTENDED.CUT){0} : {2}"
                        .format(GREEN, YELLOW, END))
    if (special == ""):
        stag = ""
    else:
        stag = ".{0}".format(special)

    # Scan Source
    type = raw_input("{0}SCAN INFOS SOURCE > \n{1}HANDBRAKE {0}[1]{1} - MEDIA"
                     "INFO {0}[2] : {2}".format(GREEN, YELLOW, END))
    scan = [
        "ffmpeg -i " + source,
        "HandBrakeCLI -t 0 --scan -i " + source,
        "mediainfo -f --Inform='General;%Duration/String3%' " + source,
        "mediainfo -f --Inform='General;%FileSize/String4%' " + source,
        "mediainfo -f --Inform='Video;%BitRate/String%' " + source,
        "mediainfo -f --Inform='Video;%FrameRate/String%' " + source,
        "mediainfo -f --Inform='Video;%Width/String%' " + source,
        "mediainfo -f --Inform='Video;%Height/String%' " + source,
        "mediainfo -f --Inform='Video;%DisplayAspectRatio/String%' " + source,
        "mediainfo -f --Inform='Audio;%CodecID% - ' " + source,
        "mediainfo -f --Inform='Audio;%Language/String% - ' " + source,
        "mediainfo -f --Inform='Audio;%BitRate/String% - ' " + source,
        "mediainfo -f --Inform='Audio;%SamplingRate/String% - ' " + source,
        "mediainfo -f --Inform='Audio;%Channel(s)/String% - ' " + source,
        "mediainfo -f --Inform='Text;%CodecID% - ' " + source,
        "mediainfo -f --Inform='Text;%Language/String% - ' " + source]

    try:

        # Handbrake Scan
        if (type == "1"):
            hb = smart_str(commands.getoutput("{0}".format(scan[1])))
            hb_out = file("{0}{1}.{2}_scan.txt"
                          .format(thumb, title, year), "w").write(hb)
            hb_data = file("{0}{1}.{2}_scan.txt"
                           .format(thumb, title, year), "r").readlines()
            for lines in hb_data:
                if ("Duration:" in lines or "Stream #" in lines):
                    print lines.replace('\n', '')
            os.system("rm -f {0}{1}.{2}_scan.txt".format(thumb, title, year))

        # MediaInfo Scan
        else:
            for x in range(2, 16):
                os.system(scan[x])
                x = x + 1

    except (OSError) as e:
        print ("\n{0} -> {1}ERROR : {2}{4}{3}\n"
               .format(GREEN, BLUE, RED, END, str(e)))
        sys.exit()

    # Video Codec
    codec_type = raw_input("{0}VIDEO CODEC > \n{1}x264 {0}[1]{1} - x265 {0}"
                           "[2] : {2}".format(GREEN, YELLOW, END))
    if (codec_type == "2"):
        codec = "libx265"
        x = "x265"
    else:
        codec = "libx264"
        x = "x264"

    # Encode Type
    encode_type = raw_input("{0}ENCODING MODE > \n{1}DUALPASS {0}[1]{1} - CRF"
                            " {0}[2] : {2}".format(GREEN, YELLOW, END))
    if (encode_type == "2"):
        bit = ""
        crf = raw_input("{0}CRF LEVEL {1}(ex: 19){0} : {2}"
                        .format(GREEN, YELLOW, END))
    else:
        crf = ""
        calculator = raw_input("{0}BITRATE CALCULATOR {1}(y/n){0} : {2}"
                               .format(GREEN, YELLOW, END))

        # Birate Calculator
        if (calculator == "y"):
            next = "y"
            while (next != "n"):
                HH, MM, SS, audiobit, rls_size, calsize = calcul()
                run_calc = calc(HH, MM, SS, audiobit, rls_size, calsize)
                try:
                    os.system(run_calc)
                except OSError as e:
                    print ("{0} -> {1}ERROR : {2}{4}{3}\n"
                           .format(GREEN, BLUE, RED, END, str(e)))
                    sys.exit()
                next = raw_input("{0}TRY AGAIN {1}(y/n){0} : {2}"
                                 .format(GREEN, YELLOW, END))
            bit = raw_input("{0}VIDEO BITRATE Kbps : {1}".format(GREEN, END))
            while not bit or len(bit) < 3 or bit.isdigit() is False:
                print ("\n{0} -> {1}ERROR : {2}Please, specify valid video "
                       "bitrate !{3}\n".format(GREEN, BLUE, RED, END))
                bit = raw_input("{0}VIDEO BITRATE Kbps : {1}"
                                .format(GREEN, END))
        else:
            bit = raw_input("{0}VIDEO BITRATE Kbps : {1}".format(GREEN, END))
            while not bit or len(bit) < 3 or bit.isdigit() is False:
                print ("\n{0} -> {1}ERROR : {2}Please, specify valid video "
                       "bitrate !{3}\n".format(GREEN, BLUE, RED, END))
                bit = raw_input("{0}VIDEO BITRATE Kbps : {1}"
                                .format(GREEN, END))

    # Video Format
    format = raw_input("{0}RELEASE FORMAT > \n{1}HDTV {0}[1]{1} - PDTV {0}[2]"
                       "{1} - BDRip {0}[3]\n{1}DVDRip {0}[4]{1} - BRRip {0}[5"
                       "]{1} - 720p {0}[6] : {2}".format(GREEN, YELLOW, END))
    form_resp = ["1", "2", "3", "4", "5", "6", "7"]
    form_values = ["", "HDTV", "PDTV", "BDRip", "DVDRip",
                   "BRRip", "720p.BluRay", "HR.PDTV"]
    if (format in form_resp):
        form = form_values[int(format)]
    else:
        form = form_values[5]

    # If PDTV
    if (format == "2"):
        hr = raw_input("{0}PDTV HIGH RESOLUTION {1}(y/n){0} : {2}"
                       .format(GREEN, YELLOW, END))
        if (hr == "y"):
            format = "7"

    # Video Container
    rlstype = raw_input("{0}RELEASE CONTAINER > \n{1}MPEG4 {0}[1]{1} - "
                        "MATROSKA {0}[2] : {2}".format(GREEN, YELLOW, END))
    if (rlstype == "1"):
        string = "mp4"
        extend = ".mp4"
    else:
        string = "matroska"
        extend = ".mkv"

    # Scan Source Tracks
    scan2 = raw_input("{0}FFMPEG SCAN TRACKS {1}(y/n){0} : {2}"
                      .format(GREEN, YELLOW, END))
    if (scan2 == "y"):
        try:
            hb = smart_str(commands.getoutput("{0}".format(scan[0])))
            hb_out = file("{0}{1}.{2}_scan.txt"
                          .format(thumb, title, year), "w").write(hb)
            hb_data = file("{0}{1}.{2}_scan.txt"
                           .format(thumb, title, year), "r").readlines()
            for lines in hb_data:
                if ("Stream #" in lines):
                    print lines.replace('\n', '')
            os.system("rm -f {0}{1}.{2}_scan.txt".format(thumb, title, year))
        except OSError as e:
            print ("{0} -> {1}ERROR : {2}{4}{3}\n"
                   .format(GREEN, BLUE, RED, END, str(e)))
            sys.exit()

    # Select Video Track
    idvideo = raw_input("{0}VIDEO TRACK FFMPEG ID {1}(ex: 0){0} : {2}"
                        .format(GREEN, YELLOW, END))
    while not idvideo or len(idvideo) > 2 or idvideo.isdigit() is False:
        print ("\n{0} -> {1}ERROR : {2}Please, specify valid video ID !{3}\n"
               .format(GREEN, BLUE, RED, END))
        idvideo = raw_input("{0}VIDEO TRACK FFMPEG ID {1}(ex: 0){0} : {2}"
                            .format(GREEN, YELLOW, END))

    # Change Video FPS
    modif_fps = raw_input("{0}CHANGE VIDEO FRAMERATE {1}(y/n){0} : {2}"
                          .format(GREEN, YELLOW, END))
    if (modif_fps == "y"):
        set_fps = raw_input("{0}VIDEO FRAMERATE {1}(ex: 23.98){0} : {2}"
                            .format(GREEN, YELLOW, END))
        while not (set_fps):
            print ("\n{0} -> {1}ERROR : {2}Please, specify video FPS !{3}\n"
                   .format(GREEN, BLUE, RED, END))
            set_fps = raw_input("{0}VIDEO FRAMERATE {1}(ex: 23.98){0} : {2}"
                                .format(GREEN, YELLOW, END))
        fps = " -r {0}".format(set_fps)
    else:
        fps = ""

    # Deinterlace Video
    deinterlace = raw_input("{0}DEINTERLACE VIDEO {1}(y/n){0} : {2}"
                            .format(GREEN, YELLOW, END))
    if (deinterlace == "y"):
        interlace = " -filter:v yadif=deint=0 "
        if (encode_type == "2"):
            interlace2 = ""
        else:
            interlace2 = " -filter:v yadif=deint=1 "
    else:
        interlace = ""
        interlace2 = ""

    # Audio Type
    codec_resp = ["1", "2", "3"]
    audiotype = raw_input("{0}RELEASE AUDIO TYPE > \n{1}FRENCH {0}[1]{1} - EN"
                          "GLiSH {0}[2]\n{1}OTHER {0}[3]{1} - MULTi {0}[4]"
                          "{1} - NONE {0}[5] : {2}"
                          .format(GREEN, YELLOW, END))

    # Single Audio Track
    if (audiotype == "1" or audiotype == "2" or audiotype == "3"):

        # Select Audio Track
        audionum = raw_input("{0}AUDIO TRACK FFMPEG ID {1}(ex: 1){0} : {2}"
                             .format(GREEN, YELLOW, END))
        while not audionum or len(audionum) > 2\
                or audionum.isdigit() is False:
            print ("\n{0} -> {1}ERROR : {2}Please, specify valid audio ID !"
                   "{3}\n".format(GREEN, BLUE, RED, END))
            audionum = raw_input("{0}AUDIO TRACK FFMPEG ID {1}(ex: 1){0} :"
                                 " {2}".format(GREEN, YELLOW, END))

        # Audio Track Title
        if (audiotype == "3"):
            audiolang = raw_input("{0}AUDIO TRACK TITLE {1}(ex: Espagnol){0} "
                                  ": {2}".format(GREEN, YELLOW, END))
            while not audiolang:
                print ("\n{0} -> {1}ERROR : {2}Please, specify audio title !"
                       "{3}\n".format(GREEN, BLUE, RED, END))
                audiolang = raw_input("{0}AUDIO TRACK TITLE {1}(ex: Espagnol)"
                                      "{0} : {2}".format(GREEN, YELLOW, END))

        # Audio Track Codec
        audiocodec = raw_input("{0}AUDIO TRACK CODEC > \n{1}MP3 {0}[1]{1} - A"
                               "C3 {0}[2]{1} - DTS/COPY {0}[3] : {2}"
                               .format(GREEN, YELLOW, END))
        while audiocodec not in codec_resp:
            print ("\n{0} -> {1}ERROR : {2}Please, specify valid codec !"
                   "{3}\n".format(GREEN, BLUE, RED, END))
            audiocodec = raw_input("{0}AUDIO TRACK CODEC > \n{1}MP3 {0}[1]{1}"
                                   " - AC3 {0}[2]{1} - DTS/COPY {0}[3] : {2}"
                                   .format(GREEN, YELLOW, END))

        # If Audio Codec AC3
        if (audiocodec == "2"):

            # Audio Track bitrate
            abitrate = raw_input("{0}AUDIO TRACK BITRATE Kbps {1}(ex: 448){0}"
                                 " : {2}".format(GREEN, YELLOW, END))
            while not abitrate or len(abitrate) < 1\
                    or abitrate.isdigit() is False:
                print ("\n{0} -> {1}ERROR : {2}Please, specify valid audio bi"
                       "trate !{3}\n".format(GREEN, BLUE, RED, END))
                abitrate = raw_input("{0}AUDIO TRACK BITRATE Kbps {1}(ex: 448"
                                     "){0} : {2}".format(GREEN, YELLOW, END))

            # Audio Track Channels
            surround = raw_input("{0}AUDIO TRACK CHANNELS {1}(ex: 2){0} : {2}"
                                 .format(GREEN, YELLOW, END))
            while not surround or len(surround) != 1\
                    or surround.isdigit() is False:
                print ("\n{0} -> {1}ERROR : {2}Please, specify valid audio su"
                       "rround !{3}\n".format(GREEN, BLUE, RED, END))
                surround = raw_input("{0}AUDIO TRACK CHANNELS {1}(ex: 2){0} :"
                                     " {2}".format(GREEN, YELLOW, END))

    # Multi Audio Tracks
    elif (audiotype == "4"):

        # Select Audio Track 01
        audionum = raw_input("{0}AUDIO TRACK 01 FFMPEG ID {1}(ex: 1){0} :"
                             " {2}".format(GREEN, YELLOW, END))
        while not audionum or len(audionum) > 2\
                or audionum.isdigit() is False:
            print ("\n{0} -> {1}ERROR : {2}Please, specify valid audio ID !"
                   "{3}\n".format(GREEN, BLUE, RED, END))
            audionum = raw_input("{0}AUDIO TRACK 01 FFMPEG ID {1}(ex: 1){0} :"
                                 " {2}".format(GREEN, YELLOW, END))

        # Audio Track 01 Title
        audiolang = raw_input("{0}AUDIO TRACK 01 TITLE {1}(ex: English){0} :"
                              " {2}".format(GREEN, YELLOW, END))
        while not audiolang:
            print ("\n{0} -> {1}ERROR : {2}Please, specify audio title !"
                   "{3}\n".format(GREEN, BLUE, RED, END))
            audiolang = raw_input("{0}AUDIO TRACK TITLE 01 {1}(ex: Espagnol)"
                                  "{0} : {2}".format(GREEN, YELLOW, END))

        # Audio Track 01 Codec
        audiocodec = raw_input("{0}AUDIO TRACK 01 CODEC > \n{1}MP3 {0}[1]{1}"
                               " - AC3 {0}[2]{1} - DTS/COPY {0}[3] : {2}"
                               .format(GREEN, YELLOW, END))
        while audiocodec not in codec_resp:
            print ("\n{0} -> {1}ERROR : {2}Please, specify valid codec !"
                   "{3}\n".format(GREEN, BLUE, RED, END))
            audiocodec = raw_input("{0}AUDIO TRACK 01 CODEC > \n{1}MP3 {0}[1]"
                                   "{1} - AC3 {0}[2]{1} - DTS/COPY {0}[3] : "
                                   "{2}".format(GREEN, YELLOW, END))

        # If Track 01 Codec AC3
        if (audiocodec == "2"):

            # Audio Track 01 bitrate
            abitrate = raw_input("{0}AUDIO TRACK 01 BITRATE Kbps {1}(ex: 448)"
                                 "{0} : {2}".format(GREEN, YELLOW, END))
            while not abitrate or len(abitrate) < 1\
                    or abitrate.isdigit() is False:
                print ("\n{0} -> {1}ERROR : {2}Please, specify valid audio bi"
                       "trate !{3}\n".format(GREEN, BLUE, RED, END))
                abitrate = raw_input("{0}AUDIO TRACK 01 BITRATE Kbps {1}(ex: "
                                     "448){0} : {2}"
                                     .format(GREEN, YELLOW, END))

            # Audio Track 01 channels
            surround = raw_input("{0}AUDIO TRACK 01 CHANNELS {1}(ex: 2){0} :"
                                 " {2}".format(GREEN, YELLOW, END))
            while not surround or len(surround) != 1\
                    or surround.isdigit() is False:
                print ("\n{0} -> {1}ERROR : {2}Please, specify valid audio su"
                       "rround !{3}\n".format(GREEN, BLUE, RED, END))
                surround = raw_input("{0}AUDIO TRACK 01 CHANNELS {1}(ex: 2)"
                                     "{0} : {2}".format(GREEN, YELLOW, END))

        # Select Audio Track 02
        audionum2 = raw_input("{0}AUDIO TRACK 02 FFMPEG ID {1}(ex: 0){0} :"
                              " {2}".format(GREEN, YELLOW, END))
        while not audionum2 or len(audionum2) > 2\
                or audionum2.isdigit() is False:
            print ("\n{0} -> {1}ERROR : {2}Please, specify valid audio ID !"
                   "{3}\n".format(GREEN, BLUE, RED, END))
            audionum2 = raw_input("{0}AUDIO TRACK 02 FFMPEG ID {1}(ex: 1){0} "
                                  ": {2}".format(GREEN, YELLOW, END))

        # Audio Track 02 Title
        audiolang2 = raw_input("{0}AUDIO TRACK 02 TITLE {1}(ex: English){0} :"
                               " {2}".format(GREEN, YELLOW, END))
        while not audiolang2:
            print ("\n{0} -> {1}ERROR : {2}Please, specify audio title !"
                   "{3}\n".format(GREEN, BLUE, RED, END))
            audiolang2 = raw_input("{0}AUDIO TRACK TITLE 02 {1}(ex: English)"
                                   "{0} : {2}".format(GREEN, YELLOW, END))

        # Audio Track 02 Codec
        audiocodec2 = raw_input("{0}AUDIO TRACK 02 CODEC > \n{1}MP3 {0}[1]{1}"
                                " - AC3 {0}[2]{1} - DTS/COPY {0}[3] : {2}"
                                .format(GREEN, YELLOW, END))
        while audiocodec2 not in codec_resp:
            print ("\n{0} -> {1}ERROR : {2}Please, specify valid codec !"
                   "{3}\n".format(GREEN, BLUE, RED, END))
            audiocodec2 = raw_input("{0}AUDIO TRACK 02 CODEC > \n{1}MP3 {0}[1"
                                    "]{1} - AC3 {0}[2]{1} - DTS/COPY {0}[3] :"
                                    " {2}".format(GREEN, YELLOW, END))

        # If Track 02 Codec AC3
        if (audiocodec2 == "2"):

            # Audio Track 02 bitrate
            abitrate2 = raw_input("{0}AUDIO TRACK 02 BITRATE Kbps {1}(ex: 448"
                                  "){0} : {2}".format(GREEN, YELLOW, END))
            while not abitrate2 or len(abitrate2) < 1\
                    or abitrate2.isdigit() is False:
                print ("\n{0} -> {1}ERROR : {2}Please, specify valid audio bi"
                       "trate !{3}\n".format(GREEN, BLUE, RED, END))
                abitrate2 = raw_input("{0}AUDIO TRACK 02 BITRATE Kbps {1}(ex:"
                                      " 448){0} : {2}"
                                      .format(GREEN, YELLOW, END))

            # Audio Track 02 channels
            surround2 = raw_input("{0}AUDIO TRACK 02 CHANNELS {1}(ex: 2){0} :"
                                  " {2}".format(GREEN, YELLOW, END))
            while not surround2 or len(surround2) != 1\
                    or surround2.isdigit() is False:
                print ("\n{0} -> {1}ERROR : {2}Please, specify valid audio su"
                       "rround !{3}\n".format(GREEN, BLUE, RED, END))
                surround2 = raw_input("{0}AUDIO TRACK 02 CHANNELS {1}(ex: 2)"
                                      "{0} : {2}".format(GREEN, YELLOW, END))
    # No Audio
    else:
        audiocodec = ""

    # Change Audio Sampling Rate
    if (audiotype == "1" or audiotype == "2"
            or audiotype == "3" or audiotype == "4"):
        audiox_ = raw_input("{0}CHANGE SAMPLING RATE {1}(y/n){0} : {2}"
                            .format(GREEN, YELLOW, END))
        if (audiox_ == "y"):

            # If Multi Audio Tracks
            if (audiotype == "4"):

                # Audio Track 01 Sampling Rate
                ar1 = raw_input("{0}AUDIO TRACK 01 SAMPLING RATE {1}(ex: 48)"
                                "{0} : {2}".format(GREEN, YELLOW, END))
                if not ar1 or ar1.isdigit() is False:
                    audiox = " -ar:a:0 48k"
                else:
                    audiox = " -ar:a:0 {0}k".format(ar1)

                # Audio Track 02 Sampling Rate
                ar2 = raw_input("{0}AUDIO TRACK 02 SAMPLING RATE {1}(ex: 48)"
                                "{0} : {2}".format(GREEN, YELLOW, END))
                if not ar2 or ar2.isdigit() is False:
                    audiox2 = " -ar:a:1 48k"
                else:
                    audiox2 = " -ar:a:1 {0}k".format(ar2)

            # If Single Audio Track
            else:

                # Audio Track Sampling Rate
                ar = raw_input("{0}AUDIO TRACK SAMPLING RATE {1}(ex: 48){0} :"
                               " {2}".format(GREEN, YELLOW, END))
                if not ar or ar.isdigit() is False:
                    audiox = " -ar:a:0 48k"
                else:
                    audiox = " -ar:a:0 {0}k".format(ar)
                    audiox2 = ""

        # Default Sampling Rate
        else:
            audiox = " -ar:a:0 48k"
            audiox2 = " -ar:a:1 48k"

    # Audio Track 01 Codec Config
    if (audiocodec == "1"):                 # MP3
        config = "-c:a:0 mp3 -b:a:0 128k -ac:a:0 2 {0}".format(audiox)
    elif (audiocodec == "2"):               # AC3
        config = "-c:a:0 ac3 -b:a:0 {0}k -ac:a:0 {1}{2}"\
                 .format(abitrate, surround, audiox)
    else:                                   # DTS
        config = "-c:a:0 copy"

    # Audio Track 02 Codec Config
    if (audiotype == "4"):
        if (audiocodec2 == "1"):            # MP3
            config2 = "-c:a:1 mp3 -b:a:1 128k -ac:a:1 2 {0}".format(audiox2)
        elif (audiocodec2 == "2"):          # AC3
            config2 = "-c:a:1 ac3 -b:a:1 {0}k -ac:a:1 {1}{2}"\
                      .format(abitrate2, surround2, audiox2)
        else:                               # DTS
            config2 = "-c:a:1 copy"

    # Audio Languages
    atype_resp = ["1", "2", "3", "4"]
    lang_values = ["", "FRENCH", "VOSTFR", "VOSTFR", "MULTi"]
    if (audiotype in atype_resp):
        lang = lang_values[int(audiotype)]
        if (audiotype == "1"):
            audiolang = lang
        elif (audiotype == "2"):
            audiolang = "ENGLiSH"
    else:
        lang = "NOAUDIO"
        audiolang = "NOAUDIO"

    # Multi Audio Tracks FFMPEG Config
    if (audiotype == "4"):
        audio_config = " -map 0:{0} -metadata:s:a:0 title='{1}' -metadata:s:"\
                       "a:0 language= {2} -map 0:{3} -metadata:s:a:1 title='"\
                       "{4}' -metadata:s:a:1 language= {5}"\
                       .format(audionum, audiolang, config,
                               audionum2, audiolang2, config2)

    # Single Audio Track FFPMEG Config
    elif (audiotype == "1" or audiotype == "2" or audiotype == "3"):
        audio_config = " -map 0:{0} -metadata:s:a:0 title='{1}' -metadata:s:"\
                       "a:0 language= {2}".format(audionum, audiolang, config)

    # No Audio FFMPEG Config
    else:
        audio_config = ""

    # Release Complete Title
    if (audiocodec == "1"):                 # MP3
        mark = ".{0}.{1}.{2}-{3}{4}".format(lang, form, x, tag, extend)
        prezquality = "{0} {1}".format(form, x)
    elif (audiocodec == "3"):               # DTS
        mark = ".{0}..DTS.{1}-{2}{3}".format(lang, form, x, tag, extend)
        prezquality = "{0} DTS.{1}".format(form, x)
    else:                                   # AC3
        mark = ".{0}.{1}.AC3.{2}-{3}{4}".format(lang, form, x, tag, extend)
        prezquality = "{0} AC3.{1}".format(form, x)

    # Mkvmerge with External Subtitles
    def remux_ext():
        if (subtype == "3"):
            if (audiotype == "4"):  # MULTi Audio / MULTi SUBS
                return (
                    " && mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}."
                    "{2}{3}{4} --compression -1:none --default-track 0:yes --"
                    "forced-track 0:no --default-track 1:yes --forced-track 1"
                    ":no --default-track 2:no --forced-track 2:no {0}{1}{5} -"
                    "-default-track '0:yes' --forced-track '0:no' --language "
                    "'0:und' {6}--track-name '0:{7}'{8} {9} --default-track '"
                    "0:no' {10}--language '0:und' {11}--track-name '0:{12}'"
                    "{13} {14} && rm -f {0}{1}{5}"
                    .format(thumb, title, year, stag, mark, extend, sync,
                            titlesub, charset, idsub, forced, sync2,
                            titlesub2, charset2, idsub2))

            else:                   # Single Audio / MULTi SUBS
                return (
                    " && mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}."
                    "{2}{3}{4} --compression -1:none --default-track 0:yes --"
                    "forced-track 0:no --default-track 1:yes --forced-track 1"
                    ":no {0}{1}{5} --default-track '0:yes' --forced-track '0:"
                    "no' --language '0:und' {6}--track-name '0:{7}'{8} {9} --"
                    "default-track '0:no' {10}--language '0:und' {11}--track-"
                    "name '0:{12}'{13} {14} && rm -f {0}{1}{5}"
                    .format(thumb, title, year, stag, mark, extend, sync,
                            titlesub, charset, idsub, forced, sync2,
                            titlesub2, charset2, idsub2))

        else:
            if (audiotype == "4"):  # MULTi Audio / Single SUBS
                return (
                    " && mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}."
                    "{2}{3}{4} --compression -1:none --default-track 0:yes --"
                    "forced-track 0:no --default-track 1:yes --forced-track 1"
                    ":no --default-track 2:no --forced-track 2:no {0}{1}{5} -"
                    "-default-track '0:yes' {6}--language '0:und' {7}--track-"
                    "name '0:{8}'{9} {10} && rm -f {0}{1}{5}"
                    .format(thumb, title, year, stag, mark, extend, forced,
                            sync, titlesub, charset, idsub))

            else:                   # Single Audio / Single SUBS
                return (
                    " && mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}."
                    "{2}{3}{4} --compression -1:none --default-track 0:yes --"
                    "forced-track 0:no --default-track 1:yes --forced-track 1"
                    ":no {0}{1}{5} --default-track '0:yes' {6}--language '0:u"
                    "nd' {7}--track-name '0:{8}'{9} {10} && rm -f {0}{1}{5}"
                    .format(thumb, title, year, stag, mark, extend, forced,
                            sync, titlesub, charset, idsub))

    # Mkvmerge with Internal Subtitles
    def remux_int():
        if (subtype == "3"):
            if (audiotype == "4"):  # MULTi Audio / MULTi SUBS
                return (
                    " && mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}."
                    "{2}{3}{4} --compression -1:none --default-track 0:yes --"
                    "forced-track 0:no --default-track 1:yes --forced-track 1"
                    ":no --default-track 2:no --forced-track 2:no --default-t"
                    "rack 3:yes --forced-track 3:no --default-track 4:no {6}"
                    "{0}{1}{5} && rm -f {0}{1}{5}"
                    .format(thumb, title, year, stag, mark, extend, forced))

            else:                    # Single Audio / MULTi SUBS
                return (
                    " && mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}."
                    "{2}{3}{4} --compression -1:none --default-track 0:yes --"
                    "forced-track 0:no --default-track 1:yes --forced-track 1"
                    ":no --default-track 2:yes --forced-track 2:no --default-"
                    "track 3:no {6}{0}{1}{5} && rm -f {0}{1}{5}"
                    .format(thumb, title, year, stag, mark, extend, forced))

        else:
            if (audiotype == "4"):  # MULTi Audio / Single SUBS
                return (
                    " && mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}."
                    "{2}{3}{4} --compression -1:none --default-track 0:yes --"
                    "forced-track 0:no --default-track 1:yes --forced-track 1"
                    ":no --default-track 2:no --forced-track 2:no --default-t"
                    "rack 3:yes {6}{0}{1}{5} && rm -f {0}{1}{5}"
                    .format(thumb, title, year, stag, mark, extend, forced))

            else:                   # Single Audio / Single SUBS
                return (
                    " && mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}."
                    "{2}{3}{4} --compression -1:none --default-track 0:yes --"
                    "forced-track 0:no --default-track 1:yes --forced-track 1"
                    ":no --default-track 2:yes {6}{0}{1}{5} && rm -f {0}{1}"
                    "{5}".format(thumb, title, year, stag,
                                 mark, extend, forced))

    # Subtitles Infos From Source
    def infos_subs_in():

        # MULTi SUBS
        if (subtype == "3"):

            # From ISO/IMG
            if (subsource == "4"):

                # Subtitles Track 01 ISO ID
                idsub = raw_input("{0}SUBTITLES TRACK 01 ISO ID {1}(ex: 1){0}"
                                  " : {2}".format(GREEN, YELLOW, END))
                while not idsub or len(idsub) > 2 or idsub.isdigit() is False:
                    print ("\n{0} -> {1}ERROR : {2}Please, specify valid subt"
                           "itles track !{3}\n".format(GREEN, BLUE, RED, END))
                    idsub = raw_input("{0}SUBTITLES TRACK 01 ISO ID {1}(ex: 1"
                                      "){0} : {2}".format(GREEN, YELLOW, END))

                # Subtitles Tracks 02 ISO ID
                idsub2 = raw_input("{0}SUBTITLES TRACK 02 ISO ID {1}(ex: 2)"
                                   "{0} : {2}".format(GREEN, YELLOW, END))
                while not idsub2 or len(idsub2) > 2\
                        or idsub2.isdigit() is False:
                    print ("\n{0} -> {1}ERROR : {2}Please, specify valid subt"
                           "itles track !{3}\n".format(GREEN, BLUE, RED, END))
                    idsub2 = raw_input("{0}SUBTITLES TRACK 01 ISO ID {1}(ex: "
                                       "1){0} : {2}"
                                       .format(GREEN, YELLOW, END))

            # From MKV or M2TS
            else:

                # Subtitles Track 01 FFMPEG ID
                idsub = raw_input("{0}SUBTITLES TRACK 01 FFMPEG ID {1}(ex: 1)"
                                  "{0} : {2}".format(GREEN, YELLOW, END))
                while not idsub or len(idsub) > 2 or idsub.isdigit() is False:
                    print ("\n{0} -> {1}ERROR : {2}Please, specify valid subt"
                           "itles track !{3}\n".format(GREEN, BLUE, RED, END))
                    idsub = raw_input("{0}SUBTITLES TRACK 01 FFMPEG ID {1}(ex"
                                      ": 1){0} : {2}"
                                      .format(GREEN, YELLOW, END))

                # Subtitles Track 02 FFMPEG ID
                idsub2 = raw_input("{0}SUBTITLES TRACK 02 FFMPEG ID {1}(ex: 2"
                                   "){0} : {2}".format(GREEN, YELLOW, END))
                while not idsub2 or len(idsub2) > 2\
                        or idsub2.isdigit() is False:
                    print ("\n{0} -> {1}ERROR : {2}Please, specify valid subt"
                           "itles track !{3}\n".format(GREEN, BLUE, RED, END))
                    idsub2 = raw_input("{0}SUBTITLES TRACK 02 FFMPEG ID {1}(e"
                                       "x: 2){0} : {2}"
                                       .format(GREEN, YELLOW, END))

            # Subtitles Track 01 Title
            titlesub = raw_input("{0}SUBTITLES TRACK 01 TITLE {1}(ex: Full.Fr"
                                 "ench){0} : {2}".format(GREEN, YELLOW, END))
            while not titlesub:
                print ("\n{0} -> {1}ERROR : {2}Please, specify subtitles "
                       "track title !{3}\n".format(GREEN, BLUE, RED, END))
                titlesub = raw_input("{0}SUBTITLES TRACK 01 TITLE {1}(ex: Ful"
                                     "l.French){0} : {2}"
                                     .format(GREEN, YELLOW, END))

            # Subtitles Track 02 Title
            titlesub2 = raw_input("{0}SUBTITLES TRACK 02 TITLE {1}(ex: French"
                                  ".Forced){0} : {2}"
                                  .format(GREEN, YELLOW, END))
            while not titlesub2:
                print ("\n{0} -> {1}ERROR : {2}Please, specify subtitles "
                       "track title !{3}\n".format(GREEN, BLUE, RED, END))
                titlesub2 = raw_input("{0}SUBTITLES TRACK 02 TITLE {1}(ex"
                                      ": French.Forced){0} : {2}"
                                      .format(GREEN, YELLOW, END))

        # Single SUBS
        else:

            # From ISO/IMG
            if (subsource == "4"):

                # Subtitles Track ISO ID
                idsub = raw_input("{0}SUBTITLES TRACK ISO ID {1}(ex: 1){0} : "
                                  "{2}".format(GREEN, YELLOW, END))
                while not idsub or len(idsub) > 2 or idsub.isdigit() is False:
                    print ("\n{0} -> {1}ERROR : {2}Please, specify valid subt"
                           "itles track !{3}\n".format(GREEN, BLUE, RED, END))
                    idsub = raw_input("{0}SUBTITLES TRACK ISO ID {1}(ex: 1"
                                      "){0} : {2}".format(GREEN, YELLOW, END))

            # From MKV or M2TS
            else:

                # Subtitles Track FFMPEG ID
                idsub = raw_input("{0}SUBTITLES TRACK FFMPEG ID {1}(ex: 1){0}"
                                  " : {2}".format(GREEN, YELLOW, END))
                while not idsub or len(idsub) > 2 or idsub.isdigit() is False:
                    print ("\n{0} -> {1}ERROR : {2}Please, specify valid subt"
                           "itles track !{3}\n".format(GREEN, BLUE, RED, END))
                    idsub = raw_input("{0}SUBTITLES TRACK FFMPEG ID {1}(ex: 1"
                                      "){0} : {2}".format(GREEN, YELLOW, END))

            # Subtitles Track Title
            if (subtype == "1"):
                titlesub = "FULL.FRENCH"
            elif (subtype == "2"):
                titlesub = "FRENCH.FORCED"
            idsub2 = ""
            titlesub2 = ""

        infos_subs_in = (idsub, titlesub, idsub2, titlesub2)
        return (infos_subs_in)

    # Subtitles Infos From Location
    def infos_subs_out():
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)

        # MULTi SUBS
        if (subtype == "3"):

            # Subtitles Track 01 Location
            ub = raw_input("{0}SUBTITLES TRACK 01 SOURCE > \n{1}"
                           .format(GREEN, END))
            while not ub or os.path.isfile(folder+ub) is False:
                print ("{0} -> {1}ERROR : {2}Bad subtitles source, please try"
                       " again !{3}\n".format(GREEN, BLUE, RED, END))
                ub = raw_input("{0}SUBTITLES TRACK 01 SOURCE > \n{1}"
                               .format(GREEN, END))

            # Subtitles Track 02 Location
            ub2 = raw_input("{0}SUBTITLES TRACK 02 SOURCE > \n{1}"
                            .format(GREEN, END))
            while not ub2 or os.path.isfile(folder+ub2) is False:
                print ("{0} -> {1}ERROR : {2}Bad subtitles source, please try"
                       " again !{3}\n".format(GREEN, BLUE, RED, END))
                ub2 = raw_input("{0}SUBTITLES TRACK 02 SOURCE > \n{1}"
                                .format(GREEN, END))

            readline.parse_and_bind("tab: ")
            idsub = "{0}{1}".format(folder, ub)
            idsub2 = "{0}{1}".format(folder, ub2)

            # Subtitles From File
            if (subsource == "3"):

                # Subtitles Track 01 Title
                titlesub = raw_input("{0}SUBTITLES TRACK 01 TITLE {1}"
                                     "(ex: Full.French){0} : {2}"
                                     .format(GREEN, YELLOW, END))
                while not titlesub:
                    print ("\n{0} -> {1}ERROR : {2}Please, specify subtitles "
                           "track title !{3}\n".format(GREEN, BLUE, RED, END))
                    titlesub = raw_input("{0}SUBTITLES TRACK 01 TITLE {1}(ex:"
                                         " Full.French){0} : {2}"
                                         .format(GREEN, YELLOW, END))

                # Subtitles Track 02 Title
                titlesub2 = raw_input("{0}SUBTITLES TRACK 02 TITLE {1}"
                                      "(ex: French.Forced){0} : {2}"
                                      .format(GREEN, YELLOW, END))
                while not titlesub2:
                    print ("\n{0} -> {1}ERROR : {2}Please, specify subtitles "
                           "track title !{3}\n".format(GREEN, BLUE, RED, END))
                    titlesub2 = raw_input("{0}SUBTITLES TRACK 02 TITLE {1}(ex"
                                          ": French.Forced){0} : {2}"
                                          .format(GREEN, YELLOW, END))

        # Single SUBS
        else:

            # Subtitles Track Location
            ub = raw_input("{0}SUBTITLES TRACK SOURCE > \n{1}"
                           .format(GREEN, END))
            while not ub or os.path.isfile(folder+ub) is False:
                print ("{0} -> {1}ERROR : {2}Bad subtitles source, please try"
                       " again !{3}\n".format(GREEN, BLUE, RED, END))
                ub = raw_input("{0}SUBTITLES TRACK SOURCE > \n{1}"
                               .format(GREEN, END))

            readline.parse_and_bind("tab: ")
            idsub = "{0}{1}".format(folder, ub)

            # Subtitles Track Title
            if (subtype == "1"):
                titlesub = "FULL.FRENCH"
            elif (subtype == "2"):
                titlesub = "FRENCH.FORCED"
            idsub2 = ""
            titlesub2 = ""

        # Subtitles Charset - MULTI SUBS
        if (subtype == "3"):
            idcharset = raw_input("{0}SUBTITLES 01 CHARSET ANSI {1}(y/n){0} :"
                                  " {2}".format(GREEN, YELLOW, END))
            idcharset2 = raw_input("{0}SUBTITLES 02 CHARSET ANSI {1}(y/n){0} "
                                   ": {2}".format(GREEN, YELLOW, END))

        # Subtitles Charset - Single SUBS
        else:
            idcharset = raw_input("{0}SUBTITLES CHARSET ANSI {1}(y/n){0} : "
                                  "{2}".format(GREEN, YELLOW, END))

        # Subtitles Charset Config
        if (idcharset == "y"):              # Track 01
            charset = " --sub-charset '0:cp1252'"
        else:
            charset = ""
        if (subtype == "3"):                # Track 02
            if idcharset2 == "y":
                charset2 = " --sub-charset '0:cp1252'"
        else:
            charset2 = ""

        # Subtitles Delay
        subsync = raw_input("{0}SUBTITLES DELAY {1}(y/n){0} : {2}"
                            .format(GREEN, YELLOW, END))
        if (subsync == "y"):

            # Delay MULTi SUBS
            if (subtype == "3"):
                subdelay1 = raw_input("{0}SUBTITLES 01 DELAY {1}(ex: -200){0}"
                                      " : {2}".format(GREEN, YELLOW, END))
                subdelay2 = raw_input("{1}SUBTITLES 02 DELAY {1}(ex: -200){1}"
                                      " : {1}".format(GREEN, YELLOW, END))
                if not subdelay1:
                    sync = ""
                else:
                    sync = "--sync 0:{0}".format(subdelay1)
                if not subdelay2:
                    sync = ""
                else:
                    sync2 = "--sync 0:{0} ".format(subdelay2)

            # Delay Single SUBS
            else:
                subdelay = raw_input("{0}SUBTITLES DELAY {1}(ex: -200){0} : "
                                     "{2}".format(GREEN, YELLOW, END))
                if not subdelay:
                    sync = ""
                    sync2 = ""
                else:
                    sync = "--sync 0:{0} ".format(subdelay)
                    sync2 = ""
        else:
            sync = ""
            sync2 = ""

        infos_subs_out = (idsub, titlesub, idsub2, titlesub2,
                          charset, charset2, sync, sync2)
        return (infos_subs_out)

    # Subtitles Extract from ISO/IMG
    def iso_extract():
        if (subtype == "3"):    # EXTRACT ISO MULTi Subs
            return (
                "sudo mount -o loop -t iso9660 {0} /media/ && cd {1} && menco"
                "der -dvd-device /media/ dvd://1 -vobsubout {2}1 -vobsuboutin"
                "dex 0 -sid {3} -o /dev/null -nosound -ovc frameno && mencode"
                "r -dvd-device /media/ dvd://1 -vobsubout {2}2 -vobsuboutinde"
                "x 0 -sid {4} -o /dev/null -nosound -ovc frameno && sudo umou"
                "nt -f /media*".format(source, thumb, title, idsub, idsub2))

        else:                   # EXTRACT ISO Single Subs
            return (
                "sudo mount -o loop -t iso9660 {0} /media/ && cd {1} && menco"
                "der -dvd-device /media/ dvd://1 -vobsubout {2} -vobsuboutind"
                "ex 0 -sid {3} -o /dev/null -nosound -ovc frameno && sudo umo"
                "unt -f /media*".format(source, thumb, title, idsub))

    # Subtitles Extract from M2TS
    def m2ts_extract():
        if (subtype == "3"):    # EXTRACT M2TS MULTi Subs
            return (
                "cd {0} && ffmpeg -i {1} -vn -an -map 0:{2} -scodec copy {3}1"
                ".mkv && ffmpeg -i {1} -vn -an -map 0:{4} -scodec copy {3}2.m"
                "kv && mkvextract tracks {3}1.mkv 0:{3}1.pgs && mkvextract tr"
                "acks {3}2.mkv 0:{3}2.pgs && mv {3}1.pgs {3}1.sup && mv {3}2."
                "pgs {3}2.sup && rm -f {3}1.mkv && rm -f {3}2.mkv"
                .format(thumb, source, idsub, title, idsub2))

        else:                   # EXTRACT M2TS Single Subs
            return (
                "cd {0} && ffmpeg -i {1} -vn -an -map 0:{2} -scodec copy {3}."
                "mkv && mkvextract tracks {3}.mkv 0:{3}.pgs && mv {3}.pgs {3}"
                ".sup && rm -f {3}.mkv".format(thumb, source, idsub, title))

    # Subtitles Format - Extract from MKV
    def mkv_format():

        # MULTi SUBS
        if (subtype == "3"):
            ext = raw_input("{0}SUBTITLES 01 FORMAT > \n{1}PGS {0}[1]{1} - "
                            "VOBSUB {0}[2]{1} - ASS {0}[3]{1} - SRT {0}[4] "
                            ": {2}".format(GREEN, YELLOW, END))
            ext2 = raw_input("{0}SUBTITLES 02 FORMAT > \n{1}PGS {0}[1]{1} -"
                             " VOBSUB {0}[2]{1} - ASS {0}[3]{1} - SRT {0}[4]"
                             " : {2}".format(GREEN, YELLOW, END))

        # Single SUBS
        else:
            ext = raw_input("{0}SUBTITLES FORMAT > \n{1}PGS {0}[1]{1} - VOBS"
                            "UB {0}[2]{1} - ASS {0}[3]{1} - SRT {0}[4] : {2}"
                            .format(GREEN, YELLOW, END))
            ext2 = ""

        # Subtitles Format Values
        ext_resp = ["1", "2", "3", "4"]
        ext_values = ["", ".pgs", ".vobsub", ".ass", ".srt"]
        if (ext in ext_resp):
            ext = ext_values[int(ext)]
        else:
            ext = ext_values[4]
        if (int(ext2) in ext_resp):
            ext2 = ext_values[int(ext2)]
        else:
            ext2 = ""

        subext = (ext, ext2)
        return (subext)

    # Subtitles Extract from MKV
    def mkv_extract():
        if (subtype == "3"):
            if (ext == "1"):
                if (ext2 == "1"):   # EXTRACT MULTi PGS
                    return (
                        "cd {0} && mkvextract tracks {1} {2}:{3}1{4} && mkvex"
                        "tract tracks {1} {5}:{3}2{6} && mv {3}1{4} {3}1.sup "
                        "&& mv {3}2{6} {3}2.sup"
                        .format(thumb, source, idsub,
                                title, ext, idsub2, ext2))

            else:                   # EXTRACT MULTi SRT/ASS/VOBSUB
                return (
                    "cd {0} && mkvextract tracks {1} {2}:{3}1{4} && mkvextrac"
                    "t tracks {1} {5}:{3}2{6}"
                    .format(thumb, source, idsub,
                            title, ext, idsub2, ext2))
        else:
            if (ext == "1"):        # EXTRACT SINGLE PGS
                return (
                    "cd {0} && mkvextract tracks {1} {2}:{3}{4} && mv {3}1{4}"
                    " {3}1.sup".format(thumb, source, idsub, title, ext))

            else:                   # EXTRACT SINGLE SRT/ASS/VOBSUB
                return (
                    "cd {0} && mkvextract tracks {1} {2}:{3}{4}"
                    .format(thumb, source, idsub, title, ext))

    # Subtitles FFMPEG Config
    def internal_subs():
        if (subtype == "3"):        # CONFIG MULTI Subs
            sub_config = " -map 0:{0} -metadata:s:s:0 title='{1}' -metadata:"\
                         "s:s:0 language= -c:s:0 srt -map 0:{2} -metadata:s:"\
                         "s:1 title='{3}' -metadata:s:s:1 language= -c:s:1 s"\
                         "rt".format(idsub, titlesub, idsub2, titlesub2)

        else:                       # CONFIG SINGLE Subs
            sub_config = " -map 0:{0} -metadata:s:s:0 title='{1}' -metadata:"\
                         "s:s:0 language= -c:s:0 srt".format(idsub, titlesub)

        return (sub_config)

    # Subtitles FROM
    subsource = raw_input("{0}SUBTITLES FROM > \n{1}SOURCE {0}[1]{1} - NONE "
                          "{0}[2]{1} - FILE {0}[3]\n{1}ISO/IMG {0}[4]{1} - M"
                          "KV {0}[5]{1} - M2TS {0}[6] : {2}"
                          .format(GREEN, YELLOW, END))

    if (subsource == "1" or subsource == "3" or subsource == "4"
            or subsource == "5" or subsource == "6"):

        # Subtitles Type
        subtype = raw_input("{0}SUBTITLES TYPE > \n{1}FR {0}[1]{1} - FORCED "
                            "{0}[2]{1} - MULTi {0}[3] : {2}"
                            .format(GREEN, YELLOW, END))

        # If from SOURCE
        if (subsource == "1"):

            # If MULTi AUDIO
            if (audiotype == "4"):
                if (subtype == "1"):        # FRENCH
                    forced = "--forced-track 3:no "
                elif (subtype == "2"):      # FORCED
                    forced = "--forced-track 3:yes "
                else:                       # MULTi
                    stforced = raw_input("{0}USE FORCED TRACK {1}(y/n){0} : "
                                         "{2}".format(GREEN, YELLOW, END))
                    if (stforced == "y"):
                        forced = "--forced-track 4:yes "
                    else:
                        forced = "--forced-track 4:no "

            # If SINGLE AUDIO
            else:
                if (subtype == "1"):        # FRENCH
                    forced = "--forced-track 2:no "
                elif (subtype == "2"):      # FORCED
                    forced = "--forced-track 2:yes "
                else:                       # MULTi
                    stforced = raw_input("{0}USE FORCED TRACK {1}(y/n){0} : "
                                         "{2}".format(GREEN, YELLOW, END))
                    if (stforced == "y"):
                        forced = "--forced-track 3:yes "
                    else:
                        forced = "--forced-track 3:no "

        # If from FILE or ISO/IMG or M2TS or MKV
        elif (subsource == "3" or subsource == "4"
                or subsource == "5" or subsource == "6"):

            if (subtype == "1"):            # FRENCH
                forced = "--forced-track '0:no' "
            elif (subtype == "2"):          # FORCED
                forced = "--forced-track '0:yes' "
            else:                           # MULTi
                stforced = raw_input("{0}USE FORCED TRACK {1}(y/n){0} : "
                                     "{2}".format(GREEN, YELLOW, END))
                if (stforced == "y"):
                    forced = "--forced-track '0:yes' "
                else:
                    forced = "--forced-track '0:no' "

        # SUBS Forced Values
        if (subtype == "3"):        # MULTi
            if (stforced == "y"):
                subforced = "YES"
            else:
                subforced = "N/A"
        elif (subtype == "2"):      # FORCED
            subforced = "YES"
        else:
            subforced = "N/A"       # FRENCH

        # Subtitles Extract Message
        def subextract_message():
            print (
                "{0}\n ->{1} EXTRACTION DONE, CHECK RESULT FOLDER & RUN OCR I"
                "F NEEDED !{0}\n ->{1} WARNING > PUT FINAL SRT IN SOURCE FOLD"
                "ER FOR NEXT STEP !{2}\n".format(RED, GREEN, END))

        # PROCESS Subtitles from SOURCE
        if (subsource == "1"):
            (idsub, titlesub, idsub2, titlesub2) = infos_subs_in()
            sub_config = internal_subs()
            sub_remux = remux_int()

        # PROCESS Subtitles ISO/IMG
        elif (subsource == "4"):
            (idsub, titlesub, idsub2, titlesub2) = infos_subs_in()
            extract_iso = iso_extract()
            try:
                os.system(extract_iso)
            except OSError as e:
                print ("{0} -> {1}ERROR : {2}{4}{3}\n"
                       .format(GREEN, BLUE, RED, END, str(e)))
                sys.exit()
            subextract_message()

            (
                idsub, titlesub, idsub2, titlesub2,
                charset, charset2, sync, sync2
            ) = infos_subs_out()

            sub_config = ""
            sub_remux = remux_ext()

        # PROCESS Subtitles from MKV
        elif (subsource == "5"):
            (idsub, titlesub, idsub2, titlesub2) = infos_subs_in()
            (ext, ext2) = mkv_format()
            extract_mkv = mkv_extract()
            try:
                os.system(extract_mkv)
            except OSError as e:
                print ("{0} -> {1}ERROR : {2}{4}{3}\n"
                       .format(GREEN, BLUE, RED, END, str(e)))
                sys.exit()
            subextract_message()

            (
                idsub, titlesub, idsub2, titlesub2,
                charset, charset2, sync, sync2
            ) = infos_subs_out()

            sub_config = ""
            sub_remux = remux_ext()

        # PROCESS Subtitles from M2TS
        elif (subsource == "6"):
            (idsub, titlesub, idsub2, titlesub2) = infos_subs_in()
            extract_m2ts = m2ts_extract()
            try:
                os.system(extract_m2ts)
            except OSError as e:
                print ("{0} -> {1}ERROR : {2}{4}{3}\n"
                       .format(GREEN, BLUE, RED, END, str(e)))
                sys.exit()
            subextract_message()

            (
                idsub, titlesub, idsub2, titlesub2,
                charset, charset2, sync, sync2
            ) = infos_subs_out()

            sub_config = ""
            sub_remux = remux_ext()

        # PROCESS Subtitles from FILE
        else:
            (
                idsub, titlesub, idsub2, titlesub2,
                charset, charset2, sync, sync2
            ) = infos_subs_out()

            sub_config = ""
            sub_remux = remux_ext()

    # NO SUBTITLES
    else:
        sub_config = ""
        sub_remux = ""
        titlesub = "N/A"
        subforced = "N/A"

    # Custom Aspect Ratio
    def custom():

        # Resolution WIDTH
        W = raw_input("{0}RESOLUTION WIDTH : {1}".format(GREEN, END))
        while not W or len(W) > 5 or W.isdigit is False:
            print ("\n{0} -> {1}ERROR : {2}Bad WIDTH entry, please try"
                   " again !{3}\n".format(GREEN, BLUE, RED, END))
            W = raw_input("{0}RESOLUTION WIDTH : {1}".format(GREEN, END))

        # Resolution HEIGHT
        H = raw_input("{0}RESOLUTION HEIGHT : {1}".format(GREEN, END))
        while not H or len(H) > 5 or H.isdigit is False:
            print ("\n{0} -> {1}ERROR : {2}Bad HEIGHT entry, please try"
                   " again !{3}\n".format(GREEN, BLUE, RED, END))
            H = raw_input("{0}RESOLUTION HEIGHT : {1}".format(GREEN, END))
        reso = " -s {0}x{1}{2}".format(W, H, crop)
        return (reso)

    # DVD Aspect Ratio
    def DVD():

        # Sample Aspect Ratio
        ask_sar = raw_input("{0}USE SAMPLE ASPECT RATIO {1}(y/n){0} : {2}"
                            .format(GREEN, YELLOW, END))
        if (ask_sar == "y"):
            sar = raw_input("{0}SOURCE ASPECT RATIO > \n{1}PAL 16:9 {0}[1]{1}"
                            " - PAL 4:3 {0}[2]\n{1}NTSC 16:9 {0}[3]{1} - NTSC"
                            " 4:3 {0}[4] : {2}".format(GREEN, YELLOW, END))
            if (sar == "1"):
                reso = " -sar 64:45{0}".format(crop)
            elif (sar == "2"):
                reso = " -sar 16:15{0}".format(crop)
            elif (sar == "3"):
                reso = " -sar 32:27{0}".format(crop)
            elif (sar == "4"):
                reso = " -sar 8:9{0}".format(crop)
            else:
                reso = custom()

        # Custom Resolution
        else:
            reso = custom()
        return (reso)

    # BluRay Aspect Ratio
    def BLURAY():

        # Custom Resolution
        perso = raw_input("{0}CUSTOM RESOLUTION {1}(y/n){0} : {2}"
                          .format(GREEN, YELLOW, END))
        if (perso == "y"):
            reso = custom()

        # Standard Resolution
        else:
            ratio = raw_input("{0}RELEASE ASPECT RATIO > \n{1}1.33 - 1.66"
                              " - 1.78 - 1.85 - 2.35 - 2.40{0} : {2}"
                              .format(GREEN, YELLOW, END))

            if (ratio == "2.40"):
                reso = " -s 720x300{0}".format(crop)
            elif (ratio == "2.35"):
                reso = " -s 720x306{0}".format(crop)
            elif (ratio == "1.85"):
                reso = " -s 720x390{0}".format(crop)
            elif (ratio == "1.78"):
                reso = " -s 720x404{0}".format(crop)
            elif (ratio == "1.66"):
                reso = " -s 720x432{0}".format(crop)
            elif (ratio == "1.33"):
                reso = " -s 720x540{0}".format(crop)
            else:
                reso = custom()
        return (reso)

    # Scan Autocrop
    scan_crop = raw_input("{0}SCAN AUTOCROP SOURCE {1}(y/n){0} : {2}"
                          .format(GREEN, YELLOW, END))
    if (scan_crop == "y"):
        try:
            hb = smart_str(commands.getoutput("{0}".format(scan[1])))
            hb_out = file("{0}{1}.{2}_scan.txt"
                          .format(thumb, title, year), "w").write(hb)
            hb_data = file("{0}{1}.{2}_scan.txt"
                           .format(thumb, title, year), "r").readlines()
            for lines in hb_data:
                if ("size:" in lines or "autocrop" in lines):
                    print lines.replace('\n', '')
            os.system("rm -f {0}{1}.{2}_scan.txt".format(thumb, title, year))
        except OSError as e:
            print ("{0} -> {1}ERROR : {2}{4}{3}\n"
                   .format(GREEN, BLUE, RED, END, str(e)))
            sys.exit()

    # Screenshots Verification
    ask_screen = raw_input("{0}SCREENSHOT VERIFICATION {1}(y/n){0} : {2}"
                           .format(GREEN, YELLOW, END))
    if (ask_screen == "y"):
        try:
            os.system("./thumbnails.py {0} 5 2".format(source))
        except OSError as e:
            print ("{0} -> {1}ERROR : {2}{4}{3}\n"
                   .format(GREEN, BLUE, RED, END, str(e)))
            sys.exit()

    # Manual CROP
    man_crop = raw_input("{0}MANUAL SOURCE CROP {1}(y/n){0} : {2}"
                         .format(GREEN, YELLOW, END))
    if (man_crop == "y"):

        # CROP Width
        w_crop = raw_input("{0}SOURCE CROP WIDTH {1}(ex: 1920){0} : {2}"
                           .format(GREEN, YELLOW, END))
        while not w_crop or len(w_crop) > 5 or w_crop.isdigit is False:
            print ("\n{0} -> {1}ERROR : {2}Bad CROP WIDTH entry, please try"
                   " again !{3}\n".format(GREEN, BLUE, RED, END))
            w_crop = raw_input("{0}SOURCE CROP WIDTH {1}(ex: 1920){0} : {2}"
                               .format(GREEN, YELLOW, END))

        # CROP Height
        h_crop = raw_input("{0}SOURCE CROP HEIGHT {1}(ex: 800){0} : {2}"
                           .format(GREEN, YELLOW, END))
        while not h_crop or len(h_crop) > 5 or h_crop.isdigit is False:
            print ("\n{0} -> {1}ERROR : {2}Bad CROP HEIGHT entry, please try"
                   " again !{3}\n".format(GREEN, BLUE, RED, END))
            h_crop = raw_input("{0}SOURCE CROP HEIGHT {1}(ex: 800){0} : {2}"
                               .format(GREEN, YELLOW, END))

        # CROP Pixels LEFT/RIGHT
        x_crop = raw_input("{0}PIXELS CROP LEFT/RIGHT {1}(ex: 0){0} : {2}"
                           .format(GREEN, YELLOW, END))
        while not x_crop or len(x_crop) > 4 or x_crop.isdigit is False:
            print ("\n{0} -> {1}ERROR : {2}Bad CROP LEFT/RIGHT entry, please "
                   "try again !{3}\n".format(GREEN, BLUE, RED, END))
            x_crop = raw_input("{0}PIXELS CROP LEFT/RIGHT {1}(ex: 0){0} : "
                               "{2}".format(GREEN, YELLOW, END))

        # CROP Pixels TOP/BOTTOM
        y_crop = raw_input("{0}PIXELS CROP TOP/BOTTOM {1}(ex: 140){0} : {2}"
                           .format(GREEN, YELLOW, END))
        while not y_crop or len(y_crop) > 4 or y_crop.isdigit is False:
            print ("\n{0} -> {1}ERROR : {2}Bad CROP TOP/BOTTOM entry, please "
                   "try again !{3}\n".format(GREEN, BLUE, RED, END))
            y_crop = raw_input("{0}PIXELS CROP TOP/BOTTOM {1}(ex: 140){0} : "
                               "{2}".format(GREEN, YELLOW, END))

        # CROP Values
        crop = " -filter:v crop={0}:{1}:{2}:{3}"\
               .format(w_crop, h_crop, x_crop, y_crop)
    else:
        crop = ""

    # Resolution PROCESS
    if (format == "4"):
        reso = DVD()
    elif (format == "6"):
        reso = custom()
    else:
        reso = BLURAY()

    # Video Format Profile
    level = raw_input("{0}VIDEO FORMAT PROFILE {1}(ex: 3.1){0} : {2}"
                      .format(GREEN, YELLOW, END))
    while not level or len(level) > 3:
        print ("\n{0} -> {1}ERROR : {2}Bad FORMAT PROFILE entry, please "
               "try again !{3}\n".format(GREEN, BLUE, RED, END))
        level = raw_input("{0}VIDEO FORMAT PROFILE {1}(ex: 3.1){0} : {2}"
                          .format(GREEN, YELLOW, END))

    # Preset x264/x265
    preset = raw_input("{0}CUSTOM PRESET X264/X265 > \n{1}FAST {0}[1]{1} - SL"
                       "OW {0}[2]{1} - SLOWER {0}[3]\n{1}VERYSLOW {0}[4]{1} -"
                       " PLACEBO {0}[5]{1} - NONE {0}[6] : {2}"
                       .format(GREEN, YELLOW, END))
    preset_resp = ["1", "2", "3", "4", "5"]
    preset_values = ["", "fast", "slow", "slower", "veryslow", "placebo"]
    if (preset in preset_resp):
        preset = " -preset {0}".format(preset_values[int(preset)])
    else:
        preset = ""

    # Tune x264/x265
    tuned = raw_input("{0}X264/X265 TUNE > \n{1}FILM {0}[1]{1} - ANIMATION "
                      "{0}[2]{1} - GRAIN {0}[3]\n{1}STILLIMAGE {0}[4]{1} - "
                      "PSNR {0}[5]{1} - SSIM {0}[6]\n{1}FASTDECODE {0}[7]{1}"
                      " - {0}[8]{1} - NONE {0}[9] : {2}"
                      .format(GREEN, YELLOW, END))
    tuned_resp = ["1", "2", "3", "4", "5", "6", "7", "8"]
    tuned_values = ["", "film", "animation", "grain", "stillimage", "psnr",
                    "ssim", "fastdecode", "zerolatency"]
    if (tuned in tuned_resp):
        tune = " -tune {0}".format(tuned_values[int(tuned)])
    else:
        tune = ""

    # Expert Mode
    x264 = raw_input("{0}X264/X265 EXPERT MODE {1}(y/n){0} : {2}"
                     .format(GREEN, YELLOW, END))
    if (x264 == "y"):

        # Threads
        threads_ = raw_input("{0}PROCESSOR THREADS {1}(ex: 8){0} : {2}"
                             .format(GREEN, YELLOW, END))
        if not (threads_):
            threads = " -threads 0"
        else:
            threads = " -threads {0}".format(threads_)

        thread_type_ = raw_input("{0}THREAD TYPE > \n{1}SLICE {0}[1]{1} - FRA"
                                 "ME {0}[2] : {2}".format(GREEN, YELLOW, END))
        if (thread_type_ == "1"):
            thread_type = " -thread_type slice"
        elif (thread_type_ == "2"):
            thread_type = " -thread_type frame"
        else:
            thread_type = ""

        # First PASS
        if (encode_type == "2"):
            fastfirstpass = ""
        else:
            fastfirstpass_ = raw_input("{0}FAST FIRST PASS {1}(y/n){0} : {2}"
                                       .format(GREEN, YELLOW, END))
            if (fastfirstpass_ == "y"):
                fastfirstpass = " -fastfirstpass 1"
            elif (fastfirstpass_ == "n"):
                fastfirstpass = " -fastfirstpass 0"
            else:
                fastfirstpass = ""

        # Refs Frames
        refs_ = raw_input("{0}REFERENCE FRAMES {1}(ex: 8){0} : {2}"
                          .format(GREEN, YELLOW, END))
        if not (refs_):
            refs = ""
        else:
            refs = " -refs {0}".format(refs_)

        # Mixed Refs
        mixed_ = raw_input("{0}MIXED REFERENCES {1}(y/n){0} : {2}"
                           .format(GREEN, YELLOW, END))
        if (mixed_ == "n"):
            mixed = " -mixed-refs 0"
        elif (mixed_ == "y"):
            mixed = " -mixed-refs 1"
        else:
            mixed = ""

        # MAX B-Frames
        bf_ = raw_input("{0}MAXIMUM B-FRAMES {1}(ex: 16){0} : {2}"
                        .format(GREEN, YELLOW, END))
        if not (bf_):
            bf = ""
        else:
            bf = " -bf {0}".format(bf_)

        # Pyramidal
        pyramid_ = raw_input("{0}PYRAMIDAL METHOD > \n{1}NONE {0}[1]{1} - NOR"
                             "MAL {0}[2]{1} - STRICT {0}[3] : {2}"
                             .format(GREEN, YELLOW, END))

        pyramid_resp = ["1", "2", "3"]
        pyramid_values = ["", "none", "normal", "strict"]
        if (pyramid_ in pyramid_resp):
            pyramid = " -b-pyramid {0}".format(pyramid_values[int(pyramid_)])
        else:
            pyramid = ""

        # Weight B-Frames
        weightb_ = raw_input("{0}WEIGHTED B-FRAMES {1}(y/n){0} : {2}"
                             .format(GREEN, YELLOW, END))
        if (weightb_ == "n"):
            weightb = " -weightb 0"
        elif (weightb_ == "y"):
            weightb = " -weightb 1"
        else:
            weightb = ""

        # Weight P-Frames
        weightp_ = raw_input("{0}WEIGHTED P-FRAMES > \n{1}NONE {0}[1]{1} - SI"
                             "MPLE {0}[2]{1} - SMART {0}[3] : {2}"
                             .format(GREEN, YELLOW, END))

        weightp_resp = ["1", "2", "3"]
        weightp_values = ["", "none", "simple", "smart"]
        if (weightp_ in weightp_resp):
            weightp = " -weightp {0}".format(weightp_values[int(weightp_)])
        else:
            weightp = ""

        # 8x8 Transform
        dct_ = raw_input("{0}ENABLE 8x8 TRANSFORM {1}(y/n){0} : {2}"
                         .format(GREEN, YELLOW, END))
        if (dct_ == "n"):
            dct = " -8x8dct 0"
        elif (dct_ == "y"):
            dct = " -8x8dct 1"
        else:
            dct = ""

        # Cabac
        cabac_ = raw_input("{0}ENABLE CABAC {1}(y/n){0} : {2}"
                           .format(GREEN, YELLOW, END))
        if (cabac_ == "n"):
            cabac = " -coder vlc"
        elif (cabac_ == "y"):
            cabac = " -coder ac"
        else:
            cabac = ""

        # Adaptive B-Frames
        b_strat = raw_input("{0}ADAPTIVE B-FRAMES > \n{1}VERYFAST {0}[1]"
                            "{1} - FAST {0}[2]{1} - SLOWER {0}[3] : {2}"
                            .format(GREEN, YELLOW, END))

        b_strategy_resp = ["1", "2", "3"]
        b_strategy_values = ["", "0", "1", "2"]
        if (b_strat in b_strategy_resp):
            b_strategy = " -b_strategy {0}"\
                         .format(b_strategy_values[int(b_strat)])
        else:
            b_strategy = ""

        # Direct Mode
        direct_ = raw_input("{0}ADAPTIVE DIRECT MODE > \n{1}NONE {0}[1]{1} - "
                            "SPATIAL {0}[2]\n{1}TEMPORAL {0}[3]{1} - AUTO {0}"
                            "[4] : {2}".format(GREEN, YELLOW, END))

        direct_resp = ["1", "2", "3", "4"]
        direct_values = ["", "none", "spatial", "temporal", "auto"]
        if (direct_ in direct_resp):
            direct = " -direct-pred {0}".format(direct_values[int(direct_)])
        else:
            direct = ""

        # Motion Estimation
        me_method_ = raw_input("{0}MOTION ESTIMATION METHOD > \n{1}DIA {0}[1]"
                               "{1} - HEX {0}[2]\n{1}UMH {0}[3]{1} - ESA {0}["
                               "4]{1} - TESA {0}[5] : {2}"
                               .format(GREEN, YELLOW, END))

        me_resp = ["1", "2", "3", "4", "5"]
        me_values = ["", "dia", "hex", "umh", "esa", "tesa"]
        if (me_method_ in me_resp):
            me_method = " -me_method {0}".format(me_values[int(me_method_)])
        else:
            me_method = ""

        # Subpixel
        subq_ = raw_input("{0}SUBPIXEL MOTION ESTIMATION {1}(ex: 11){0} : {2}"
                          .format(GREEN, YELLOW, END))
        if not (subq_):
            subq = ""
        else:
            subq = " -subq {0}".format(subq_)

        # Estimation Range
        me_range_ = raw_input("{0}MOTION ESTIMATION RANGE {1}(ex: 16){0} : "
                              "{2}".format(GREEN, YELLOW, END))
        if not (me_range_):
            me_range = ""
        else:
            me_range = " -me_range {0}".format(me_range_)

        # Partitions
        parts_ = raw_input("{0}PARTITIONS TYPE > \n{1}ALL {0}[1]{1} - p8x8 "
                           "{0}[2]{1} - p4x4 {0}[3]\n{1}NONE {0}[4]{1} - b8x8"
                           "{0}[5]{1} - i8x8 {0}[6]{1} - i4x4 {0}[7] : {2}"
                           .format(GREEN, YELLOW, END))

        parts_resp = ["1", "2", "3", "4", "5", "6", "7"]
        p_values = ["", "all", "p8x8", "p4x4", "none", "b8x8", "i8x8", "i4x4"]
        if (parts_ in parts_resp):
            partitions = " -partitions {0}".format(p_values[int(parts_)])
        else:
            partitions = ""

        # Trellis Mode
        trellis_ = raw_input("{0}TRELLIS MODE > \n{1}OFF {0}[1]{1} - DEFAULT "
                             "{0}[2]{1} - ALL {0}[3] : {2}"
                             .format(GREEN, YELLOW, END))

        trellis_resp = ["1", "2", "3"]
        trellis_values = ["", "0", "1", "2"]
        if (trellis_ in trellis_resp):
            trellis = " -trellis {0}".format(trellis_values[int(trellis_)])
        else:
            trellis = ""

        # Quantization
        aq_ = raw_input("{0}ADAPTIVE QUANTIZATION {1}(ex: 1.5){0} : {2}"
                        .format(GREEN, YELLOW, END))
        if not (aq_):
            aq = ""
        else:
            aq = " -aq-strength {0}".format(aq_)

        # Psychovisual
        psy_ = raw_input("{0}PSYCHOVISUAL OPTIMIZATION {1}(y/n){0} : {2}"
                         .format(GREEN, YELLOW, END))
        if (psy_) == "n":
            psy = " -psy 0"
        elif (psy_) == "y":
            psy = " -psy 1"
        else:
            psy = ""

        # Rate Distortion
        psy1 = raw_input("{0}RATE DISTORTION [psy-rd] {1}(ex: 1.00){0} : {2}"
                         .format(GREEN, YELLOW, END))
        if not (psy1):
            psyrd = ""
        else:

            # Psy RD
            psy2 = raw_input("{0}PSYCHOVISUAL TRELLIS [psy-rd] {1}(ex: 0.15)"
                             "{0} : {2}".format(GREEN, YELLOW, END))
            if not (psy2):
                psyrd = ""
            else:
                psyrd = " -psy-rd {0}:{1}".format(psy1, psy2)

        # Deblock
        deblock_ = raw_input("{0}DEBLOCKING {1}(ex: -1:-1){0} : {2}"
                             .format(GREEN, YELLOW, END))
        if not (deblock_):
            deblock = ""
        else:
            deblock = " -deblock {0}".format(deblock_)

        # Frames Lookahead
        lookahead_ = raw_input("{0}FRAMES LOOKAHEAD {1}(ex: 60){0} : {2}"
                               .format(GREEN, YELLOW, END))
        if not (lookahead_):
            lookahead = ""
        else:
            lookahead = " -rc-lookahead {0}".format(lookahead_)

        # BluRay Compatibility
        bluray_ = raw_input("{0}BLURAY COMPATIBILITY {1}(y/n){0} : {2}"
                            .format(GREEN, YELLOW, END))
        if (bluray_ == "y"):
            bluray = " -bluray-compat 1"
        elif (bluray_ == "n"):
            bluray = " -bluray-compat 0"
        else:
            bluray = ""

        # Fast Skip
        fastpskip_ = raw_input("{0}FAST SKIP on P-FRAMES {1}(y/n){0} : {2}"
                               .format(GREEN, YELLOW, END))
        if (fastpskip_ == "y"):
            fastpskip = " -fast-pskip 1"
        elif (fastpskip_ == "n"):
            fastpskip = " -fast-pskip 0"
        else:
            fastpskip = ""

        # Keyframe Interval
        g_ = raw_input("{0}KEYFRAME INTERVAL {1}(ex: 250){0} : {2}"
                       .format(GREEN, YELLOW, END))
        if not (g_):
            g = ""
        else:
            g = " -g {0}".format(g_)

        # Minimal Key Interval
        keyint_min_ = raw_input("{0}MINIMAL KEY INTERVAL {1}(ex: 25){0} : {2}"
                                .format(GREEN, YELLOW, END))
        if not (keyint_min_):
            keyint_min = ""
        else:
            keyint_min = " -keyint_min {0}".format(keyint_min_)

        # Scene Cut
        scenecut_ = raw_input("{0}SCENECUT DETECTION {1}(ex: 40){0} : {2}"
                              .format(GREEN, YELLOW, END))
        if not (scenecut_):
            scenecut = ""
        else:
            scenecut = " -sc_threshold {0}".format(scenecut_)

        # Chroma Motion
        cmp_ = raw_input("{0}CHROMA MOTION ESTIMATION {1}(y/n){0} : {2}"
                         .format(GREEN, YELLOW, END))
        if (cmp_ == "n"):
            cmp = " -cmp sad"
        elif (cmp_ == "y"):
            cmp = " -cmp chroma"
        else:
            cmp = ""

        # Expert Mode Values
        param = "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}"\
                "{16}{17}{18}{19}{20}{21}{22}{23}{24}{25}{26}{27}{28}{29}"\
                .format(preset, tune, threads, thread_type, fastfirstpass,
                        refs, mixed, bf, pyramid, weightb, weightp, dct,
                        cabac, b_strategy, direct, me_method, subq, me_range,
                        partitions, trellis, aq, psy, psyrd, deblock,
                        lookahead, bluray, fastpskip, g, keyint_min,
                        scenecut, cmp)

        # First Pass Values
        pass1 = "{0}{1}{2}{3}{4}".format(preset, tune, threads,
                                         thread_type, fastfirstpass)

    # Default Threads Values
    else:
        param = "{0}{1} -threads 0".format(preset, tune)
        pass1 = "{0}{1} -threads 0".format(preset, tune)

    # Release SOURCE
    nfosource = raw_input("{0}RELEASE SOURCE {1}(ex: 1080p.HDZ){0} : {2}"
                          .format(GREEN, YELLOW, END))
    while not nfosource:
        print ("\n{0} -> {1}ERROR : {2}Please, specify RELEASE SOURCE !{3}\n"
               .format(GREEN, BLUE, RED, END))
        nfosource = raw_input("{0}RELEASE SOURCE {1}(ex: 1080p.HDZ){0} : {2}"
                              .format(GREEN, YELLOW, END))

    # Release IMDB ID
    nfoimdb = raw_input("{0}RELEASE IMDB ID {1}(ex: 6686697){0} : {2}"
                        .format(GREEN, YELLOW, END))

    # Find Release Title
    if (len(nfoimdb) == 7 and nfoimdb.isdigit()):
        print ("{0} -> {1}Scanning API Databases...{2}".format(RED, BLUE, END))

        # Search IMDB
        searchIMDB = "http://deanclatworthy.com/imdb/?id=tt{0}"\
                     .format(nfoimdb)
        try:
            data1 = loads(urlopen(searchIMDB, None, 5.0).read())
        except (HTTPError, ValueError, URLError):
            data1 = ""
            pass
        except socket.timeout:
            data1 = ""
            pass

        # Search TMDB
        searchTMDB = "http://api.themoviedb.org/3/movie/tt{0}?api_key={1}&"\
                     "language=fr".format(nfoimdb, tmdb_api_key)
        dataTMDB = urllib2.Request(searchTMDB,
                                   headers={"Accept": "application/json"})
        try:
            data2 = loads(urllib2.urlopen(dataTMDB, None, 5.0).read())
        except (HTTPError, ValueError, URLError):
            data2 = ""
            pass
        except socket.timeout:
            data2 = ""
            pass

        # Search OMDB
        searchOMDB = "http://www.omdbapi.com/?i=tt{0}".format(nfoimdb)
        try:
            data3 = loads(urlopen(searchOMDB, None, 5.0).read())
        except (HTTPError, ValueError, URLError):
            data3 = ""
            pass
        except socket.timeout:
            data3 = ""
            pass

        # Search MyAPI
        searchAPI = "http://www.myapifilms.com/imdb?idIMDB=tt{0}&format=JSON"\
                    "&aka=0&business=0&seasons=0&seasonYear=0&technical=0&la"\
                    "ng=en-us&actors=N&biography=0&trailer=0&uniqueName=0&fi"\
                    "lmography=0&bornDied=0&starSign=0&actorActress=0&actorT"\
                    "rivia=0&movieTrivia=0".format(nfoimdb)
        try:
            data4 = loads(urlopen(searchAPI, None, 5.0).read())
        except(HTTPError, ValueError, URLError):
            data4 = ""
            pass
        except socket.timeout:
            data4 = ""
            pass

        # Parse Title
        tit = ["title", "original_title", "Title", "title"]

        if (tit[0] in data1):
            dir = "{0}".format(smart_str(data1['title']))
        elif (tit[1] in data2):
            dir = "{0}".format(smart_str(data2['original_title']))
        elif (tit[2] in data3):
            dir = "{0}".format(smart_str(data3['Title']))
        elif (tit[3] in data4):
            dir = "{0}".format(smart_str(data4['title']))
        else:
            nfoimdb = ""

        # Replace Title Bad chars
        if (tit[0] in data1 or tit[1] in data2
                or tit[2] in data3 or tit[3] in data4):
            name = dir.replace(' ', '.').replace('/', '').replace('(', '')\
                      .replace(')', '').replace('"', '').replace(':', '')\
                      .replace("'", "").replace("[", "").replace("]", "")\
                      .replace(";", "").replace(",", "")
        else:
            name = ""
    else:
        name = ""

    # Release Desired Size
    tsize = raw_input("{0}RELEASE SIZE > \n{1}SD - 350 - 550 - 700 - 1.37"
                      " - 2.05 - 2.74 - 4.37 - 6.56 - HD{0} : {2}"
                      .format(GREEN, YELLOW, END))

    tsize = tsize.lower()
    tsize_resp = ["350", "550", "700", "1.37", "2.05",
                  "2.74", "4.37", "6.56", "sd", "hd"]
    pieces_val = ["18", "18", "19", "20", "20", "21", "22", "22", "19", "22"]
    prezsize_val = ["350Mo", "550Mo", "700Mo", "1.37Go", "2.05Go",
                    "2.74Go", "4.37Go", "6.56Go", "..Mo", "..Go"]

    if (tsize in tsize_resp):
        pieces = pieces_val[tsize_resp.index(tsize)]
        prezsize = prezsize_val[tsize_resp.index(tsize)]
    else:
        pieces = "20"
        prezsize = "..Mo"

    # Print FFMPEG Command
    pprint = raw_input("{0}PRINT FFMPEG FINAL COMMAND {1}(y/n){0} : {2}"
                       .format(GREEN, YELLOW, END))

    # Return Global Values
    info_main = (
        source, thumb, team, announce, title, year, stag, string, codec,
        encode_type, crf, bit, level, idvideo, fps, interlace, interlace2,
        audiolang, audio_config, sub_config, sub_remux, reso, param, pass1,
        mark, nfoimdb, nfosource, titlesub, subforced, prezquality,
        prezsize, pieces, name, pprint
    )

    return (info_main)
