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
import readline
import optparse
import json
import urllib2
import subprocess
from json import loads
from urllib2 import (Request, urlopen, URLError, HTTPError, unquote)
from subprocess import (CalledProcessError, check_output)
from pprint import pprint
sys.path.append("app/")
from style import (banner, next, color)
from bitrate import (calcul, calc)
from settings import option

(folder, thumb, tag, team, announce, tmdb_api_key, tag_thumb) = option()
(BLUE, RED, YELLOW, GREEN, END) = color()


def ffmpeg():
    if (encode_type == "2"):    # CRF
        return (
            "cd {0} && ffmpeg -i {1} -metadata title='{2}.{3}' -metadata prou"
            "dly.presented.by='{4}' -map 0:{5}{6}{7} -metadata:s:v:0 title= -"
            "metadata:s:v:0 language= -f {8}{9} -c:v:0 {10} -crf {11} -level "
            "{12}{13}{14}{15} -passlogfile {2}.log {2}.{3}{16}{17}{18}"
            .format(thumb, source, title, year, team, idvideo, interlace, fps,
                    string, reso, codec, crf, level, param, audio_config,
                    sub_config, stag, mark, sub_remux))

    else:                       # 2PASS
        return (
            "cd {0} && ffmpeg -i {1} -pass 1 -map 0:{2}{3}{4} -f {5}{6} -c:v:"
            "0 {7} -b:v:0 {8}k -level {9}{10} -an -sn -passlogfile {11}.log "
            "{11}.{12}{13}{14} && ffmpeg -y -i {1} -pass 2 -metadata title='"
            "{11}.{12}' -metadata proudly.presented.by='{15}' -map 0:{2}{16}"
            "{4} -metadata:s:v:0 title= -metadata:s:v:0 language= -f {5}{6}"
            " -c:v:0 {7} -b:v:0 {8}k -level {9}{17}{18}{19} -passlogfile "
            "{11}.log {11}.{12}{13}{14}{20}"
            .format(thumb, source, idvideo, interlace2, fps, string, reso,
                    codec, bit, level, pass1, title, year, stag, mark, team,
                    interlace, param, audio_config, sub_config, sub_remux))


def data():
    if (len(nfoimdb) == 7 and nfoimdb.isdigit()):
        prezz = "&& ./genprez.py {0} {1} {2} {3} {4} && mv {5}{6}*.txt {5}"\
                "{7}.{8}{9}{10}txt && ./imgur.py {5}{7}.{8}*.png add "\
                .format(audiolang, prezquality, titlesub, prezsize, nfoimdb,
                        thumb, name, title, year, stag, mark[:3])

        zipp = "cd {0} && zip -r {1}.zip -m {1}.{2}{3}*.torrent {1}.{2}{3}"\
               "*.nfo {1}.{2}{3}*.txt {1}*.log {1}.{2}{3}*.png"\
               .format(thumb, title, year, stag)

    else:
        prezz = "&& ./imgur.py {0}{1}.{2}*.png ".format(thumb, title, year)

        zipp = "cd {0} && zip -r {1}.zip -m {1}.{2}{3}*.torrent {1}.{2}{3}*."\
               "nfo {1}*.log {1}.{2}{3}*.png".format(thumb, title, year, stag)

    return (
        "./thumbnails.py {0}{1}.{2}{3}{4} 5 2 {5}&& ./nfogen.sh {0}{1}.{2}{3}"
        "{4} {6} {7} {8} http://www.imdb.com/title/tt{9} && rm -f {0}{1}*.mbt"
        "ree && cd {0} && mktorrent -a {10} -p -t 8 -l {11} {1}.{2}{3}{4} "
        "{12}".format(thumb, title, year, stag, mark, prezz, nfosource,
                      titlesub, subforced, nfoimdb, announce, pieces, zipp))


def main():

    # Auto complete
    def completer(text, state):
        return (
            [entry for entry in os.listdir(
                folder + os.path.dirname(
                    readline.get_line_buffer())
                ) if entry.startswith(text)][state])

    # Source Infos
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)
    prefix = raw_input("{0}RELEASE SOURCE > \n{1}".format(GREEN, END))
    readline.parse_and_bind("tab: ")
    source = "{0}{1}".format(folder, prefix)
    title = raw_input("{0}RELEASE TITLE {1}(ex: Hudson.Hawk){0} : {2}"
                      .format(GREEN, YELLOW, END))
    year = raw_input("{0}RELEASE PRODUCTION YEAR : {1}".format(GREEN, END))
    special = raw_input("{0}SPECIAL TAG {1}(ex: EXTENDED.CUT){0} : {2}"
                        .format(GREEN, YELLOW, END))

    scan = [
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

    type = raw_input("{0}SCAN INFOS SOURCE > \n{1}HANDBRAKE {0}[1]{1} - MEDIA"
                     "INFO {0}[2] : {2}".format(GREEN, YELLOW, END))
    try:
        if (type == "1"):
            subprocess.check_output(scan[0], shell=True)
        else:
            subprocess.check_output(scan[1], shell=True)
            for x in range(1, 15):
                os.system(scan[x])
                x = x + 1

    except (OSError, CalledProcessError) as e:
        print ("{0}\n -> {1}ERROR : {2}Bad source selection, please try"
               " again !\n{3}".format(GREEN, BLUE, RED, END))
        sys.exit()

    # Video Params
    codec_type = raw_input("{0}VIDEO CODEC > \n{1}x264 {0}[1]{1} - x265 {0}"
                           "[2] : {2}".format(GREEN, YELLOW, END))
    if (codec_type == "2"):
        codec = "libx265"
    else:
        codec = "libx264"

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
        if (calculator == "y"):
            next = "y"
            while (next != "n"):
                HH, MM, SS, audiobit, rls_size, calsize = calcul()
                run_calc = calc(HH, MM, SS, audiobit, rls_size, calsize)
                os.system(run_calc)
                next = raw_input("{0}TRY AGAIN {1}(y/n){0} : {2}"
                                 .format(GREEN, YELLOW, END))
            bit = raw_input("{0}VIDEO BITRATE Kbps : {1}".format(GREEN, END))
        else:
            bit = raw_input("{0}VIDEO BITRATE Kbps : {1}".format(GREEN, END))

    format = raw_input("{0}RELEASE FORMAT > \n{1}HDTV {0}[1]{1} - PDTV {0}[2]"
                       "{1} - BDRip {0}[3]\n{1}DVDRip {0}[4]{1} - BRRip {0}[5"
                       "]{1} - 720p {0}[6] : {2}".format(GREEN, YELLOW, END))
    if (format == "2"):
        hr = raw_input("{0}PDTV HIGH RESOLUTION {1}(y/n){0} : {2}"
                       .format(GREEN, YELLOW, END))
        if (hr == "y"):
            format = "7"

    rlstype = raw_input("{0}RELEASE CONTAINER > \n{1}MPEG4 {0}[1]{1} - "
                        "MATROSKA {0}[2] : {2}".format(GREEN, YELLOW, END))
    if (rlstype == "1"):
        string = "mp4"
    else:
        string = "matroska"

    scan2 = raw_input("{0}FFMPEG SCAN TRACKS {1}(y/n){0} : {2}"
                      .format(GREEN, YELLOW, END))
    ffmpeg = "ffmpeg -i {0}".format(source)
    if (scan2 == "y"):
        os.system(ffmpeg)

    idvideo = raw_input("{0}VIDEO TRACK FFMPEG ID {1}(ex: 0){0} : {2}"
                        .format(GREEN, YELLOW, END))
    modif_fps = raw_input("{0}CHANGE VIDEO FRAMERATE {1}(y/n){0} : {2}"
                          .format(GREEN, YELLOW, END))
    if (modif_fps == "y"):
        set_fps = raw_input("{0}VIDEO FRAMERATE {1}(ex: 23.98){0} : {2}"
                            .format(GREEN, YELLOW, END))
        fps = " -r {0}".format(set_fps)
    else:
        fps = ""

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

    # Audio Infos
    audiotype = raw_input("{0}RELEASE AUDIO TYPE > \n{1}FRENCH {0}[1]{1} - EN"
                          "GLiSH {0}[2]\n{1}OTHER {0}[3]{1} - MULTi {0}[4]"
                          "{1} - NONE {0}[5] : {2}"
                          .format(GREEN, YELLOW, END))

    if (audiotype == "1" or audiotype == "2" or audiotype == "3"):
        audionum = raw_input("{0}AUDIO TRACK FFMPEG ID {1}(ex: 1){0} : {2}"
                             .format(GREEN, YELLOW, END))
        if (audiotype == "3"):
            audiolang = raw_input("{0}AUDIO TRACK TITLE {1}(ex: Espagnol){0} "
                                  ": {2}".format(GREEN, YELLOW, END))
        audiocodec = raw_input("{0}AUDIO TRACK CODEC > \n{1}MP3 {0}[1]{1} - A"
                               "C3 {0}[2]{1} - DTS/COPY {0}[3] : {2}"
                               .format(GREEN, YELLOW, END))
        if (audiocodec == "2"):
            abitrate = raw_input("{0}AUDIO TRACK BITRATE Kbps {1}(ex: 448){0}"
                                 " : {2}".format(GREEN, YELLOW, END))
            surround = raw_input("{0}AUDIO TRACK CHANNELS {1}(ex: 2){0} : {2}"
                                 .format(GREEN, YELLOW, END))
    elif (audiotype == "4"):
        audionum = raw_input("{0}AUDIO TRACK 01 FFMPEG ID {1}(ex: 1){0} :"
                             " {2}".format(GREEN, YELLOW, END))
        audiolang = raw_input("{0}AUDIO TRACK 01 TITLE {1}(ex: English){0} :"
                              " {2}".format(GREEN, YELLOW, END))
        audiocodec = raw_input("{0}AUDIO TRACK 01 CODEC > \n{1}MP3 {0}[1]{1}"
                               " - AC3 {0}[2]{1} - DTS/COPY {0}[3] : {2}"
                               .format(GREEN, YELLOW, END))
        if (audiocodec == "2"):
            abitrate = raw_input("{0}AUDIO TRACK 01 BITRATE Kbps {1}(ex: 448)"
                                 "{0} : {2}".format(GREEN, YELLOW, END))
            surround = raw_input("{0}AUDIO TRACK 01 CHANNELS {1}(ex: 2){0} :"
                                 " {2}".format(GREEN, YELLOW, END))
        audionum2 = raw_input("{0}AUDIO TRACK 02 FFMPEG ID {1}(ex: 0){0} :"
                              " {2}".format(GREEN, YELLOW, END))
        audiolang2 = raw_input("{0}AUDIO TRACK 02 TITLE {1}(ex: English){0} :"
                               " {2}".format(GREEN, YELLOW, END))
        audiocodec2 = raw_input("{0}AUDIO TRACK 02 CODEC > \n{1}MP3 {0}[1]{1}"
                                " - AC3 {0}[2]{1} - DTS/COPY {0}[3] : {2}"
                                .format(GREEN, YELLOW, END))

        if (audiocodec2 == "2"):
            abitrate2 = raw_input("{0}AUDIO TRACK 02 BITRATE Kbps {1}(ex: 448"
                                  "){0} : {2}".format(GREEN, YELLOW, END))
            surround2 = raw_input("{0}AUDIO TRACK 02 CHANNELS {1}(ex: 2){0} :"
                                  " {2}".format(GREEN, YELLOW, END))
    else:
        audiocodec = ""
    if (audiotype == "1" or audiotype == "2"
            or audiotype == "3" or audiotype == "4"):
        audiox_ = raw_input("{0}CHANGE SAMPLING RATE {1}(y/n){0} : {2}"
                            .format(GREEN, YELLOW, END))
        if (audiox_ == "y"):
            if (audiotype == "4"):
                ar1 = raw_input("{0}AUDIO TRACK 01 SAMPLING RATE {1}(ex: 48)"
                                "{0} : {2}".format(GREEN, YELLOW, END))
                if not (ar1):
                    audiox = " -ar:a:0 48k"
                else:
                    audiox = " -ar:a:0 {0}k".format(ar1)
                ar2 = raw_input("{0}AUDIO TRACK 02 SAMPLING RATE {1}(ex: 48)"
                                "{0} : {2}".format(GREEN, YELLOW, END))
                if not (ar2):
                    audiox2 = " -ar:a:1 48k"
                else:
                    audiox2 = " -ar:a:1 {0}k".format(ar2)
            else:
                ar = raw_input("{0}AUDIO TRACK SAMPLING RATE {1}(ex: 48){0} :"
                               " {2}".format(GREEN, YELLOW, END))
                if not (ar):
                    audiox = " -ar:a:0 48k"
                else:
                    audiox = " -ar:a:0 {0}k".format(ar)
                    audiox2 = ""
        else:
            audiox = " -ar:a:0 48k"
            audiox2 = " -ar:a:1 48k"

    # Audio Params
    if (audiocodec == "1"):
        config = "-c:a:0 mp3 -b:a:0 128k -ac:a:0 2 {0}".format(audiox)
    elif (audiocodec == "2"):
        config = "-c:a:0 ac3 -b:a:0 {0}k -ac:a:0 {1}{2}"\
                 .format(abitrate, surround, audiox)
    else:
        config = "-c:a:0 copy"

    if (audiotype == "4"):
        if (audiocodec2 == "1"):
            config2 = "-c:a:1 mp3 -b:a:1 128k -ac:a:1 2 {0}".format(audiox2)
        elif (audiocodec2 == "2"):
            config2 = "-c:a:1 ac3 -b:a:1 {0}k -ac:a:1 {1}{2}"\
                      .format(abitrate2, surround2, audiox2)
        else:
            config2 = "-c:a:1 copy"

    if (audiotype == "1"):
        lang = "FRENCH"
        audiolang = "FRENCH"
    elif (audiotype == "2"):
        lang = "VOSTFR"
        audiolang = "ENGLiSH"
    elif (audiotype == "3"):
        lang = "VOSTFR"
    elif (audiotype == "4"):
        lang = "MULTi"
    else:
        lang = "NOAUDIO"
        audiolang = "NOAUDIO"

    if (audiotype == "4"):
        audio_config = " -map 0:{0} -metadata:s:a:0 title='{1}' -metadata:s:"\
                       "a:0 language= {2} -map 0:{3} -metadata:s:a:1 title='"\
                       "{4}' -metadata:s:a:1 language= {5}"\
                       .format(audionum, audiolang, config,
                               audionum2, audiolang2, config2)

    elif (audiotype == "1" or audiotype == "2" or audiotype == "3"):
        audio_config = " -map 0:{0} -metadata:s:a:0 title='{1}' -metadata:s:"\
                       "a:0 language= {2}".format(audionum, audiolang, config)
    else:
        audio_config = ""

    # Release Tag
    if (special == ""):
        stag = ""
    else:
        stag = ".{0}".format(special)

    form_resp = [1, 2, 3, 4, 5, 6, 7]
    form_values = ["", "HDTV", "PDTV", "BDRip", "DVDRip",
                   "BRRip", "720p.BluRay", "HR.PDTV"]
    if (format in form_resp):
        form = form_values[format]
    else:
        form = form_values[5]
    if (rlstype == "1"):
        extend = ".mp4"
    else:
        extend = ".mkv"
    if (codec_type == "2"):
        x = "x265"
    else:
        x = "x264"

    if (audiocodec == "1"):
        mark = ".{0}.{1}.{2}-{3}{4}".format(lang, form, x, tag, extend)
        prezquality = "{0} {1}".format(form, x)
    elif (audiocodec == "3"):
        mark = ".{0}..DTS.{1}-{2}{3}".format(lang, form, x, tag, extend)
        prezquality = "{0} DTS.{1}".format(form, x)
    else:
        mark = ".{0}.{1}.AC3.{2}-{3}{4}".format(lang, form, x, tag, extend)
        prezquality = "{0} AC3.{1}".format(form, x)

    # Mkvmerge
    def remux_ext():
        if (subtype == "3"):
            if (audiotype == "4"):  # Audio MULTi / SRT MULTi
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

            else:                   # Audio FR-VO / SRT MULTi
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
            if (audiotype == "4"):  # Audio MULTi / SRT FR-VO
                return (
                    " && mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}."
                    "{2}{3}{4} --compression -1:none --default-track 0:yes --"
                    "forced-track 0:no --default-track 1:yes --forced-track 1"
                    ":no --default-track 2:no --forced-track 2:no {0}{1}{5} -"
                    "-default-track '0:yes' {6}--language '0:und' {7}--track-"
                    "name '0:{8}'{9} {10} && rm -f {0}{1}{5}"
                    .format(thumb, title, year, stag, mark, extend, forced,
                            sync, titlesub, charset, idsub))

            else:                   # Audio FR-VO / SRT FR-VO
                return (
                    " && mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}."
                    "{2}{3}{4} --compression -1:none --default-track 0:yes --"
                    "forced-track 0:no --default-track 1:yes --forced-track 1"
                    ":no {0}{1}{5} --default-track '0:yes' {6}--language '0:u"
                    "nd' {7}--track-name '0:{8}'{9} {10} && rm -f {0}{1}{5}"
                    .format(thumb, title, year, stag, mark, extend, forced,
                            sync, titlesub, charset, idsub))

    def remux_int():
        if (subtype == "3"):
            if (audiotype == "4"):  # Audio MULTi / SRT MULTi
                return (
                    " && mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}."
                    "{2}{3}{4} --compression -1:none --default-track 0:yes --"
                    "forced-track 0:no --default-track 1:yes --forced-track 1"
                    ":no --default-track 2:no --forced-track 2:no --default-t"
                    "rack 3:yes --forced-track 3:no --default-track 4:no {6}"
                    "{0}{1}{5} && rm -f {0}{1}{5}"
                    .format(thumb, title, year, stag, mark, extend, forced))

            else:                   # Audio FR/VO / SRT MULTi
                return (
                    " && mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}."
                    "{2}{3}{4} --compression -1:none --default-track 0:yes --"
                    "forced-track 0:no --default-track 1:yes --forced-track 1"
                    ":no --default-track 2:yes --forced-track 2:no --default-"
                    "track 3:no {6}{0}{1}{5} && rm -f {0}{1}{5}"
                    .format(thumb, title, year, stag, mark, extend, forced))

        else:
            if (audiotype == "4"):  # Audio MULTi / SRT FR/VO
                return (
                    " && mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}."
                    "{2}{3}{4} --compression -1:none --default-track 0:yes --"
                    "forced-track 0:no --default-track 1:yes --forced-track 1"
                    ":no --default-track 2:no --forced-track 2:no --default-t"
                    "rack 3:yes {6}{0}{1}{5} && rm -f {0}{1}{5}"
                    .format(thumb, title, year, stag, mark, extend, forced))

            else:                   # Audio FR/VO / SRT FR/VO
                return (
                    " && mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}."
                    "{2}{3}{4} --compression -1:none --default-track 0:yes --"
                    "forced-track 0:no --default-track 1:yes --forced-track 1"
                    ":no --default-track 2:yes {6}{0}{1}{5} && rm -f {0}{1}"
                    "{5}".format(thumb, title, year, stag,
                                 mark, extend, forced))

    # Subtitles Params
    def infos_subs_in():
        if (subtype == "3"):
            if (subsource == "4"):
                idsub = raw_input("{0}SUBTITLES TRACK 01 ISO ID {1}(ex: 1){0}"
                                  " : {3}".format(GREEN, YELLOW, END))
                idsub2 = raw_input("{0}SUBTITLES TRACK 02 ISO ID {1}(ex: 2)"
                                   "{0} : {2}".format(GREEN, YELLOW, END))
            else:
                idsub = raw_input("{0}SUBTITLES TRACK 01 FFMPEG ID {1}(ex: 1)"
                                  "{0} : {2}".format(GREEN, YELLOW, END))
                idsub2 = raw_input("{0}SUBTITLES TRACK 02 FFMPEG ID {1}(ex: 2"
                                   "){0} : {2}".format(GREEN, YELLOW, END))
            titlesub = raw_input("{0}SUBTITLES TRACK 01 TITLE {1}(ex: Full.Fr"
                                 "ench){0} : {2}".format(GREEN, YELLOW, END))
            titlesub2 = raw_input("{0}SUBTITLES TRACK 02 TITLE {1}(ex: French"
                                  ".Forced){0} : {2}"
                                  .format(GREEN, YELLOW, END))
        else:
            if (subsource == "4"):
                idsub = raw_input("{0}SUBTITLES TRACK ISO ID {1}(ex: 1){0} : "
                                  "{2}".format(GREEN, YELLOW, END))
            else:
                idsub = raw_input("{0}SUBTITLES TRACK FFMPEG ID {1}(ex: 1){0}"
                                  " : {2}".format(GREEN, YELLOW, END))
            if (subtype == "1"):
                titlesub = "FULL.FRENCH"
            elif (subtype == "2"):
                titlesub = "FRENCH.FORCED"
            idsub2 = ""
            titlesub2 = ""

        infos_subs_in = (idsub, titlesub, idsub2, titlesub2)
        return (infos_subs_in)

    def infos_subs_out():
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)

        if (subtype == "3"):
            ub = raw_input("{0}SUBTITLES TRACK 01 SOURCE > \n{1}"
                           .format(GREEN, END))
            ub2 = raw_input("{0}SUBTITLES TRACK 02 SOURCE > \n{1}"
                            .format(GREEN, END))
            readline.parse_and_bind("tab: ")
            idsub = "{0}{1}".format(folder, ub)
            idsub2 = "{0}{1}".format(folder, ub2)
            if (subsource == "3"):
                titlesub = raw_input("{0}SUBTITLES TRACK 01 TITLE {1}"
                                     "(ex: Full.French){0} : {2}"
                                     .format(GREEN, YELLOW, END))
                titlesub2 = raw_input("{0}SUBTITLES TRACK 02 TITLE {1}"
                                      "(ex: French.Forced){0} : {2}"
                                      .format(GREEN, YELLOW, END))
        else:
            ub = raw_input("{0}SUBTITLES TRACK SOURCE > \n{1}"
                           .format(GREEN, END))
            readline.parse_and_bind("tab: ")
            idsub = "{0}{1}".format(folder, ub)
            if (subtype == "1"):
                titlesub = "FULL.FRENCH"
            elif (subtype == "2"):
                titlesub = "FRENCH.FORCED"
            idsub2 = ""
            titlesub2 = ""

        if (subtype == "3"):
            idcharset = raw_input("{0}SUBTITLES 01 CHARSET ANSI {1}(y/n){0} :"
                                  " {2}".format(GREEN, YELLOW, END))
            idcharset2 = raw_input("{0}SUBTITLES 02 CHARSET ANSI {1}(y/n){0} "
                                   ": {2}".format(GREEN, YELLOW, END))
        else:
            idcharset = raw_input("{0}SUBTITLES CHARSET ANSI {1}(y/n){0} : "
                                  "{2}".format(GREEN, YELLOW, END))

        if (idcharset == "y"):
            charset = " --sub-charset '0:cp1252'"
        else:
            charset = ""

        if (subtype == "3"):
            if idcharset2 == "y":
                charset2 = " --sub-charset '0:cp1252'"
        else:
            charset2 = ""

        subsync = raw_input("{0}SUBTITLES DELAY {1}(y/n){0} : {2}"
                            .format(GREEN, YELLOW, END))
        if (subsync == "y"):
            if (subtype == "3"):
                subdelay1 = raw_input("{0}SUBTITLES 01 DELAY {1}(ex: -200){0}"
                                      " : {2}".format(GREEN, YELLOW, END))
                subdelay2 = raw_input("{1}SUBTITLES 02 DELAY {1}(ex: -200){1}"
                                      " : {1}".format(GREEN, YELLOW, END))
                sync = "--sync 0:{0}".format(subdelay1)
                sync2 = "--sync 0:{0} ".format(subdelay2)
            else:
                subdelay = raw_input("{0}SUBTITLES DELAY {1}(ex: -200){0} : "
                                     "{2}".format(GREEN, YELLOW, END))
                sync = "--sync 0:{0} ".format(subdelay)
                sync2 = ""
        else:
            sync = ""
            sync2 = ""

        infos_subs_out = (idsub, titlesub, idsub2, titlesub2,
                          charset, charset2, sync, sync2)
        return (infos_subs_out)

    # Subtitles Extract
    def iso_extract():
        if (subtype == "3"):    # EXTRACT ISO MULTi Subs
            return (
                "sudo mount -o loop -t iso9660 {0} /media/ && cd {1} && menco"
                "der -dvd-device /media/ dvd://1 -vobsubout {2}1 -vobsuboutin"
                "dex 0 -sid {3} -o /dev/null -nosound -ovc frameno && mencode"
                "r -dvd-device /media/ dvd://1 -vobsubout {2}2 -vobsuboutinde"
                "x 0 -sid {4} -o /dev/null -nosound -ovc frameno && sudo umou"
                "nt -f /media*".format(source, thumb, title, idsub, idsub2))

        else:                   # EXTRACT ISO FR/VO Subs
            return (
                "sudo mount -o loop -t iso9660 {0} /media/ && cd {1} && menco"
                "der -dvd-device /media/ dvd://1 -vobsubout {2} -vobsuboutind"
                "ex 0 -sid {3} -o /dev/null -nosound -ovc frameno && sudo umo"
                "unt -f /media*".format(source, thumb, title, idsub))

    def m2ts_extract():
        if (subtype == "3"):    # EXTRACT M2TS MULTi Subs
            return (
                "cd {0} && ffmpeg -i {1} -vn -an -map 0:{2} -scodec copy {3}1"
                ".mkv && ffmpeg -i {1} -vn -an -map 0:{4} -scodec copy {3}2.m"
                "kv && mkvextract tracks {3}1.mkv 0:{3}1.pgs && mkvextract tr"
                "acks {3}2.mkv 0:{3}2.pgs && mv {3}1.pgs {3}1.sup && mv {3}2."
                "pgs {3}2.sup && rm -f {3}1.mkv && rm -f {3}2.mkv"
                .format(thumb, source, idsub, title, idsub2))

        else:                   # EXTRACT M2TS FR/VO Subs
            return (
                "cd {0} && ffmpeg -i {1} -vn -an -map 0:{2} -scodec copy {3}."
                "mkv && mkvextract tracks {3}.mkv 0:{3}.pgs && mv {3}.pgs {3}"
                ".sup && rm -f {3}.mkv".format(thumb, source, idsub, title))

    def mkv_format():
        if (subtype == "3"):
            ext = raw_input("{0}SUBTITLES 01 FORMAT > \n{1}PGS {0}[1]{1} - "
                            "VOBSUB {0}[2]{1} - ASS {0}[3]{1} - SRT {0}[4] "
                            ": {2}".format(GREEN, YELLOW, END))
            ext2 = raw_input("{0}SUBTITLES 02 FORMAT > \n{1}PGS {0}[1]{1} -"
                             " VOBSUB {0}[2]{1} - ASS {0}[3]{1} - SRT {0}[4]"
                             " : {2}".format(GREEN, YELLOW, END))
        else:
            ext = raw_input("{0}SUBTITLES FORMAT > \n{1}PGS {0}[1]{1} - VOBS"
                            "UB {0}[2]{1} - ASS {0}[3]{1} - SRT {0}[4] : {2}"
                            .format(GREEN, YELLOW, END))
            ext2 = ""

        ext_resp = [1, 2, 3, 4]
        ext_values = ["", ".pgs", ".vobsub", ".ass", ".srt"]
        if (ext in ext_resp):
            ext = ext_values[ext]
        else:
            ext = ext_values[4]
        if (ext2 in ext_resp):
            ext2 = ext_values[ext2]
        else:
            ext2 = ""

        subext = (ext, ext2)
        return (subext)

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
            if (ext == "1"):        # EXTRACT FR/VO PGS
                return (
                    "cd {0} && mkvextract tracks {1} {2}:{3}{4} && mv {3}1{4}"
                    " {3}1.sup".format(thumb, source, idsub, title, ext))

            else:                   # EXTRACT FR/VO SRT/ASS/VOBSUB
                return (
                    "cd {0} && mkvextract tracks {1} {2}:{3}{4}"
                    .format(thumb, source, idsub, title, ext))

    def internal_subs():
        if (subtype == "3"):        # CONFIG MULTI Subs
            sub_config = " -map 0:{0} -metadata:s:s:0 title='{1}' -metadata:"\
                         "s:s:0 language= -c:s:0 srt -map 0:{2} -metadata:s:"\
                         "s:1 title='{3}' -metadata:s:s:1 language= -c:s:1 s"\
                         "rt".format(idsub, titlesub, idsub2, titlesub2)

        else:                       # CONFIG FR/VO Subs
            sub_config = " -map 0:{0} -metadata:s:s:0 title='{1}' -metadata:"\
                         "s:s:0 language= -c:s:0 srt".format(idsub, titlesub)

        return (sub_config)

    # Subtitles infos
    subsource = raw_input("{0}SUBTITLES FROM > \n{1}SOURCE {0}[1]{1} - NONE "
                          "{0}[2]{1} - FILE {0}[3]\n{1}ISO/IMG {0}[4]{1} - M"
                          "KV {0}[5]{1} - M2TS {0}[6] : {2}"
                          .format(GREEN, YELLOW, END))

    if (subsource == "1" or subsource == "3" or subsource == "4"
            or subsource == "5" or subsource == "6"):
        subtype = raw_input("{0}SUBTITLES TYPE > \n{1}FR {0}[1]{1} - FORCED "
                            "{0}[2]{1} - MULTi {0}[3] : {2}"
                            .format(GREEN, YELLOW, END))
        if (subsource == "1"):
            if (audiotype == "4"):
                if (subtype == "1"):
                    forced = "--forced-track 3:no "
                elif (subtype == "2"):
                    forced = "--forced-track 3:yes "
                else:
                    stforced = raw_input("{0}USE FORCED TRACK {1}(y/n){0} : "
                                         "{2}".format(GREEN, YELLOW, END))
                    if (stforced == "y"):
                        forced = "--forced-track 4:yes "
                    else:
                        forced = "--forced-track 4:no "
            else:
                if (subtype == "1"):
                    forced = "--forced-track 2:no "
                elif (subtype == "2"):
                    forced = "--forced-track 2:yes "
                else:
                    stforced = raw_input("{0}USE FORCED TRACK {1}(y/n){0} : "
                                         "{2}".format(GREEN, YELLOW, END))
                    if (stforced == "y"):
                        forced = "--forced-track 3:yes "
                    else:
                        forced = "--forced-track 3:no "
        elif (subsource == "3" or subsource == "4"
                or subsource == "5" or subsource == "6"):
            if (subtype == "1"):
                forced = "--forced-track '0:no' "
            elif (subtype == "2"):
                forced = "--forced-track '0:yes' "
            else:
                stforced = raw_input("{0}USE FORCED TRACK {1}(y/n){0} : "
                                     "{2}".format(GREEN, YELLOW, END))
                if (stforced == "y"):
                    forced = "--forced-track '0:yes' "
                else:
                    forced = "--forced-track '0:no' "
        if (subtype == "3"):
            if (stforced == "y"):
                subforced = "YES"
            else:
                subforced = "N/A"
        elif (subtype == "2"):
            subforced = "YES"
        else:
            subforced = "N/A"

        # Subtitles Process
        def subextract_message():
            print (
                "{0}\n ->{1} EXTRACTION DONE, CHECK RESULT FOLDER & RUN OCR I"
                "F NEEDED !{0}\n ->{1} WARNING > PUT FINAL SRT IN SOURCE FOLD"
                "ER FOR NEXT STEP !\n{2}".format(RED, GREEN, END))

        if (subsource == "1"):          # SOURCE
            (idsub, titlesub, idsub2, titlesub2) = infos_subs_in()
            sub_config = internal_subs()
            sub_remux = remux_int()

        elif (subsource == "4"):        # ISO
            (idsub, titlesub, idsub2, titlesub2) = infos_subs_in()
            extract_iso = iso_extract()
            os.system(extract_iso)
            subextract_message()

            (
                idsub, titlesub, idsub2, titlesub2,
                charset, charset2, sync, sync2
            ) = infos_subs_out()

            sub_config = ""
            sub_remux = remux_ext()

        elif (subsource == "5"):        # MKV
            (idsub, titlesub, idsub2, titlesub2) = infos_subs_in()
            (ext, ext2) = mkv_format()
            extract_mkv = mkv_extract()
            os.system(extract_mkv)
            subextract_message()

            (
                idsub, titlesub, idsub2, titlesub2,
                charset, charset2, sync, sync2
            ) = infos_subs_out()

            sub_config = ""
            sub_remux = remux_ext()

        elif (subsource == "6"):        # M2TS
            (idsub, titlesub, idsub2, titlesub2) = infos_subs_in()
            extract_m2ts = m2ts_extract()
            os.system(extract_m2ts)
            subextract_message()

            (
                idsub, titlesub, idsub2, titlesub2,
                charset, charset2, sync, sync2
            ) = infos_subs_out()

            sub_config = ""
            sub_remux = remux_ext()

        else:                           # FILE
            (
                idsub, titlesub, idsub2, titlesub2,
                charset, charset2, sync, sync2
            ) = infos_subs_out()

            sub_config = ""
            sub_remux = remux_ext()

    else:
        sub_config = ""
        sub_remux = ""
        titlesub = "N/A"
        subforced = "N/A"

    # Aspect Ratio
    def custom():
        W = raw_input("{0}RESOLUTION WIDTH : {1}".format(GREEN, END))
        H = raw_input("{0}RESOLUTION HEIGHT : {1}".format(GREEN, END))
        reso = " -s {0}x{1}{2}".format(W, H, crop)
        return (reso)

    def DVD():
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
        else:
            reso = custom()
        return (reso)

    def BLURAY():
        perso = raw_input("{0}CUSTOM RESOLUTION {1}(y/n){0} : {2}"
                          .format(GREEN, YELLOW, END))
        if (perso == "y"):
            reso = custom()
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

    scan = raw_input("{0}SCAN AUTOCROP SOURCE {1}(y/n){0} : {2}"
                     .format(GREEN, YELLOW, END))
    if (scan == "y"):
        os.system("HandBrakeCLI -t 0 --scan -i{0}".format(source))

    ask_screen = raw_input("{0}SCREENSHOT VERIFICATION {1}(y/n){0} : {2}"
                           .format(GREEN, YELLOW, END))
    if (ask_screen == "y"):
        os.system("./thumbnails.py {0} 5 2".format(source))

    man_crop = raw_input("{0}MANUAL SOURCE CROP {1}(y/n){0} : {2}"
                         .format(GREEN, YELLOW, END))
    if (man_crop == "y"):
        w_crop = raw_input("{0}SOURCE CROP WIDTH {1}(ex: 1920){0} : {2}"
                           .format(GREEN, YELLOW, END))
        h_crop = raw_input("{0}SOURCE CROP HEIGHT {1}(ex: 800){0} : {2}"
                           .format(GREEN, YELLOW, END))
        x_crop = raw_input("{0}PIXELS CROP LEFT/RIGHT {1}(ex: 0){0} : {2}"
                           .format(GREEN, YELLOW, END))
        y_crop = raw_input("{0}PIXELS CROP TOP/BOTTOM {1}(ex: 140){0} : {2}"
                           .format(GREEN, YELLOW, END))

        crop = " -filter:v crop={0}:{1}:{2}:{3}"\
               .format(w_crop, h_crop, x_crop, y_crop)
    else:
        crop = ""
    if (format == "4"):
        reso = DVD()
    elif (format == "6"):
        reso = custom()
    else:
        reso = BLURAY()

    # x264/x265 Params
    level = raw_input("{0}VIDEO FORMAT PROFILE {1}(ex: 3.1){0} : {2}"
                      .format(GREEN, YELLOW, END))
    preset = raw_input("{0}CUSTOM PRESET X264/X265 > \n{1}FAST {0}[1]{1} - SL"
                       "OW {0}[2]{1} - SLOWER {0}[3]\n{1}VERYSLOW {0}[4]{1} -"
                       " PLACEBO {0}[5]{1} - NONE {0}[6] : {2}"
                       .format(GREEN, YELLOW, END))

    preset_resp = [1, 2, 3, 4, 5]
    preset_values = ["", "fast", "slow", "slower", "veryslow", "placebo"]
    if (preset in preset_resp):
        preset = " -preset {0}".format(preset_values[preset])
    else:
        preset = ""

    tuned = raw_input("{0}X264/X265 TUNE > \n{1}FILM {0}[1]{1} - ANIMATION "
                      "{0}[2]{1} - GRAIN {0}[3]\n{1}STILLIMAGE {0}[4]{1} - "
                      "PSNR {0}[5]{1} - SSIM {0}[6]\n{1}FASTDECODE {0}[7]{1}"
                      " - {0}[8]{1} - NONE {0}[9] : {2}"
                      .format(GREEN, YELLOW, END))

    tuned_resp = [1, 2, 3, 4, 5, 6, 7, 8]
    tuned_values = ["", "film", "animation", "grain", "stillimage", "psnr",
                    "ssim", "fastdecode", "zerolatency"]
    if (tuned in tuned_resp):
        tune = " -tune {0}".format(tuned_values[tuned])
    else:
        tune = ""

    # Expert Mode ___#
    x264 = raw_input("{0}X264/X265 EXPERT MODE {1}(y/n){0} : {2}"
                     .format(GREEN, YELLOW, END))
    if (x264 == "y"):
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

        refs_ = raw_input("{0}REFERENCE FRAMES {1}(ex: 8){0} : {2}"
                          .format(GREEN, YELLOW, END))
        if not (refs_):
            refs = ""
        else:
            refs = " -refs {0}".format(refs_)

        mixed_ = raw_input("{0}MIXED REFERENCES {1}(y/n){0} : {2}"
                           .format(GREEN, YELLOW, END))
        if (mixed_ == "n"):
            mixed = " -mixed-refs 0"
        elif (mixed_ == "y"):
            mixed = " -mixed-refs 1"
        else:
            mixed = ""

        bf_ = raw_input("MAXIMUM B-FRAMES {1}(ex: 16){0} : {2}"
                        .format(GREEN, YELLOW, END))
        if not (bf_):
            bf = ""
        else:
            bf = " -bf {0}".format(bf_)

        pyramid_ = raw_input("{0}PYRAMIDAL METHOD > \n{1}NONE {0}[1]{1} - NOR"
                             "MAL {0}[2]{1} - STRICT {0}[3] : {2}"
                             .format(GREEN, YELLOW, END))

        pyramid_resp = [1, 2, 3]
        pyramid_values = ["", "none", "normal", "strict"]
        if (pyramid_ in pyramid_resp):
            pyramid = " -b-pyramid {0}".format(pyramid_values[pyramid_])
        else:
            pyramid = ""

        weightb_ = raw_input("{0}WEIGHTED B-FRAMES {1}(y/n){0} : {2}"
                             .format(GREEN, YELLOW, END))
        if (weightb_ == "n"):
            weightb = " -weightb 0"
        elif (weightb_ == "y"):
            weightb = " -weightb 1"
        else:
            weightb = ""

        weightp_ = raw_input("{0}WEIGHTED P-FRAMES > \n{1}NONE {0}[1]{1} - SI"
                             "MPLE {0}[2]{1} - SMART {0}[3] : {2}"
                             .format(GREEN, YELLOW, END))

        weightp_resp = [1, 2, 3]
        weightp_values = ["", "none", "simple", "smart"]
        if (weightp_ in weightp_resp):
            weightp = " -weightp {0}".format(weightp_values[weightp_])
        else:
            weightp = ""

        dct_ = raw_input("{0}ENABLE 8x8 TRANSFORM {1}(y/n){0} : {2}"
                         .format(GREEN, YELLOW, END))
        if (dct_ == "n"):
            dct = " -8x8dct 0"
        elif (dct_ == "y"):
            dct = " -8x8dct 1"
        else:
            dct = ""

        cabac_ = raw_input("{0}ENABLE CABAC {1}(y/n){0} : {2}"
                           .format(GREEN, YELLOW, END))
        if (cabac_ == "n"):
            cabac = " -coder vlc"
        elif (cabac_ == "y"):
            cabac = " -coder ac"
        else:
            cabac = ""

        b_strat = raw_input("{0}ADAPTIVE B-FRAMES > \n{0}VERYFAST {0}[1]"
                            "{1} - FAST {0}[2]{1} - SLOWER {0}[3] : {2}"
                            .format(GREEN, YELLOW, END))

        b_strategy_resp = [1, 2, 3]
        b_strategy_values = ["", "0", "1", "2"]
        if (b_strat in b_strategy_resp):
            b_strategy = " -b_strategy {0}".format(b_strategy_values[b_strat])
        else:
            b_strategy = ""

        direct_ = raw_input("{0}ADAPTIVE DIRECT MODE > \n{1}NONE {0}[1]{1} - "
                            "SPATIAL {0}[2]\n{1}TEMPORAL {0}[3]{1} - AUTO {0}"
                            "[4] : {2}".format(GREEN, YELLOW, END))

        direct_resp = [1, 2, 3, 4]
        direct_values = ["", "none", "spatial", "temporal", "auto"]
        if (direct_ in direct_resp):
            direct = " -direct-pred {0}".format(direct_values[direct_])
        else:
            direct = ""

        me_method_ = raw_input("{0}MOTION ESTIMATION METHOD > \n{1}DIA {0}[1]"
                               "{1} - HEX {0}[2]\n{1}UMH {0}[3]{1} - ESA {0}["
                               "4]{1} - TESA {0}[5] : {2}"
                               .format(GREEN, YELLOW, END))

        me_resp = [1, 2, 3, 4, 5]
        me_values = ["", "dia", "hex", "umh", "esa", "tesa"]
        if (me_method_ in me_resp):
            me_method = " -me_method {0}".format(me_values[me_method_])
        else:
            me_method = ""

        subq_ = raw_input("{0}SUBPIXEL MOTION ESTIMATION {1}(ex: 11){0} : {2}"
                          .format(GREEN, YELLOW, END))
        if not (subq_):
            subq = ""
        else:
            subq = " -subq {0}".format(subq_)

        me_range_ = raw_input("{0}MOTION ESTIMATION RANGE {1}(ex: 16){0} : "
                              "{2}".format(GREEN, YELLOW, END))
        if not (me_range_):
            me_range = ""
        else:
            me_range = " -me_range {0}".format(me_range_)

        parts_ = raw_input("PARTITIONS TYPE > \n{1}ALL {0}[1]{1} - p8x8 {0}[2"
                           "]{1} - p4x4 {0}[3]\n{1}NONE {0}[4]{1} - b8x8 {0}["
                           "5]{1} - i8x8 {0}[6]{1} - i4x4 {0}[7] : {2}"
                           .format(GREEN, YELLOW, END))

        parts_resp = [1, 2, 3, 4, 5, 6, 7]
        p_values = ["", "all", "p8x8", "p4x4", "none", "b8x8", "i8x8", "i4x4"]
        if (parts_ in parts_resp):
            partitions = " -partitions {0}".format(p_values[parts_])
        else:
            partitions = ""

        trellis_ = raw_input("{0}TRELLIS MODE > \n{1}OFF {0}[1]{1} - DEFAULT "
                             "{0}[2]{1} - ALL {0}[3] : {2}"
                             .format(GREEN, YELLOW, END))

        trellis_resp = [1, 2, 3]
        trellis_values = ["", "0", "1", "2"]
        if (trellis_ in trellis_resp):
            trellis = " -trellis {0}".format(trellis_values[trellis_])
        else:
            trellis = ""

        aq_ = raw_input("{0}ADAPTIVE QUANTIZATION {1}(ex: 1.5){0} : {2}"
                        .format(GREEN, YELLOW, END))
        if not (aq_):
            aq = ""
        else:
            aq = " -aq-strength {0}".format(aq_)

        psy_ = raw_input("{0}PSYCHOVISUAL OPTIMIZATION {1}(y/n){0} : {2}"
                         .format(GREEN, YELLOW, END))
        if (psy_) == "n":
            psy = " -psy 0"
        elif (psy_) == "y":
            psy = " -psy 1"
        else:
            psy = ""

        psy1 = raw_input("{0}RATE DISTORTION [psy-rd] {1}(ex: 1.00){0} : {2}"
                         .format(GREEN, YELLOW, END))
        if not (psy1):
            psyrd = ""
        else:
            psy2 = raw_input("{0}PSYCHOVISUAL TRELLIS [psy-rd] {1}(ex: 0.15)"
                             "{0} : {2}".format(GREEN, YELLOW, END))
            if not (psy2):
                psyrd = ""
            else:
                psyrd = " -psy-rd {0}:{1}".format(psy1, psy2)

        deblock_ = raw_input("{0}DEBLOCKING {1}(ex: -1:-1){0} : {2}"
                             .format(GREEN, YELLOW, END))
        if not (deblock_):
            deblock = ""
        else:
            deblock = " -deblock {0}".format(deblock_)

        lookahead_ = raw_input("{0}FRAMES LOOKAHEAD {1}(ex: 60){0} : {2}"
                               .format(GREEN, YELLOW, END))
        if not (lookahead_):
            lookahead = ""
        else:
            lookahead = " -rc-lookahead {0}".format(lookahead_)

        bluray_ = raw_input("{0}BLURAY COMPATIBILITY {1}(y/n){0} : {2}"
                            .format(GREEN, YELLOW, END))
        if (bluray_ == "y"):
            bluray = " -bluray-compat 1"
        elif (bluray_ == "n"):
            bluray = " -bluray-compat 0"
        else:
            bluray = ""

        fastpskip_ = raw_input("{0}FAST SKIP on P-FRAMES {1}(y/n){0} : {2}"
                               .format(GREEN, YELLOW, END))
        if (fastpskip_ == "y"):
            fastpskip = " -fast-pskip 1"
        elif (fastpskip_ == "n"):
            fastpskip = " -fast-pskip 0"
        else:
            fastpskip = ""

        g_ = raw_input("{0}KEYFRAME INTERVAL {1}(ex: 250){0} : {2}"
                       .format(GREEN, YELLOW, END))
        if not (g_):
            g = ""
        else:
            g = " -g {0}".format(g_)

        keyint_min_ = raw_input("{0}MINIMAL KEY INTERVAL {1}(ex: 25){0} : {2}"
                                .format(GREEN, YELLOW, END))
        if not (keyint_min_):
            keyint_min = ""
        else:
            keyint_min = " -keyint_min {0}".format(keyint_min_)

        scenecut_ = raw_input("{0}SCENECUT DETECTION {1}(ex: 40){0} : {2}"
                              .format(GREEN, YELLOW, END))
        if not (scenecut_):
            scenecut = ""
        else:
            scenecut = " -sc_threshold {0}".format(scenecut_)

        cmp_ = raw_input("{0}CHROMA MOTION ESTIMATION {1}(y/n){0} : {2}"
                         .format(GREEN, YELLOW, END))
        if (cmp_ == "n"):
            cmp = " -cmp sad"
        elif (cmp_ == "y"):
            cmp = " -cmp chroma"
        else:
            cmp = ""

        param = "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}{15}"\
                "{16}{17}{18}{19}{20}{21}{22}{23}{24}{25}{26}{27}{28}{29}"\
                .format(preset, tune, threads, thread_type, fastfirstpass,
                        refs, mixed, bf, pyramid, weightb, weightp, dct,
                        cabac, b_strategy, direct, me_method, subq, me_range,
                        partitions, trellis, aq, psy, psyrd, deblock,
                        lookahead, bluray, fastpskip, g, keyint_min,
                        scenecut, cmp)

        pass1 = "{0}{1}{2}{3}{4}".format(preset, tune, threads,
                                         thread_type, fastfirstpass)

    else:
        param = "{0}{1} -threads 0".format(preset, tune)
        pass1 = "{0}{1} -threads 0".format(preset, tune)

    # Prez / Torrent
    nfosource = raw_input("{0}RELEASE SOURCE {1}(ex: 1080p.HDZ){0} : {2}"
                          .format(GREEN, YELLOW, END))
    nfoimdb = raw_input("{0}RELEASE IMDB ID {1}(ex: 6686697){0} : {2}"
                        .format(GREEN, YELLOW, END))

    if (len(nfoimdb) == 7 and nfoimdb.isdigit()):

        searchIMDB = "http://deanclatworthy.com/imdb/?id=tt{0}"\
                     .format(nfoimdb)
        try:
            data1 = loads(urlopen(searchIMDB).read())
        except (HTTPError, ValueError, URLError):
            data1 = ""
            pass

        searchTMDB = "http://api.themoviedb.org/3/movie/tt{0}?api_key={1}&"\
                     "language=fr".format(nfoimdb, tmdb_api_key)
        dataTMDB = urllib2.Request(searchTMDB,
                                   headers={"Accept": "application/json"})
        try:
            data2 = loads(urllib2.urlopen(dataTMDB).read())
        except (HTTPError, ValueError, URLError):
            data2 = ""
            pass

        searchOMDB = "http://www.omdbapi.com/?i=tt{0}".format(nfoimdb)
        try:
            data3 = loads(urlopen(searchOMDB).read())
        except (HTTPError, ValueError, URLError):
            data3 = ""
            pass

        searchAPI = "http://www.myapifilms.com/imdb?idIMDB=tt{0}&format=JSON"\
                    "&aka=0&business=0&seasons=0&seasonYear=0&technical=0&la"\
                    "ng=en-us&actors=N&biography=0&trailer=0&uniqueName=0&fi"\
                    "lmography=0&bornDied=0&starSign=0&actorActress=0&actorT"\
                    "rivia=0&movieTrivia=0".format(nfoimdb)
        try:
            data4 = loads(urlopen(searchAPI).read())
        except(HTTPError, ValueError, URLError):
            data4 = ""
            pass

        tit = ["title", "original_title", "Title", "title"]

        if (tit[0] in data1):
            dir = "{0}".format(data1['title'])
        elif (tit[1] in data2):
            dir = "{0}".format(data2['original_title'])
        elif (tit[2] in data3):
            dir = "{0}".format(data3['Title'])
        elif (tit[3] in data4):
            dir = "{0}".format(data4['title'])
        else:
            nfoimdb = ""

        if (tit[0] in data1 or tit[1] in data2
                or tit[3] in data3 or tit[4] in data4):
            name = dir.replace(' ', '.').replace('/', '').replace('(', '')\
                      .replace(')', '').replace('"', '').replace(':', '')\
                      .replace("'", "").replace("[", "").replace("]", "")\
                      .replace(";", "").replace(",", "")
        else:
            name = ""
    else:
        name = ""

    tsize = raw_input("{0}RELEASE SIZE > \n{1}SD - 350 - 550 - 700 - 1.37"
                      " - 2.05 - 2.74 - 4.37 - 6.56 - HD{0} : {2}"
                      .format(GREEN, YELLOW, END))

    tsize = tsize.lower()
    if (tsize == "350"):
        pieces = "18"
        prezsize = "350Mo"
    elif (tsize == "550"):
        pieces = "18"
        prezsize = "550Mo"
    elif (tsize == "700"):
        pieces = "19"
        prezsize = "700Mo"
    elif (tsize == "1.37"):
        pieces = "20"
        prezsize = "1.37Go"
    elif (tsize == "2.05"):
        pieces = "20"
        prezsize = "2.05Go"
    elif (tsize == "2.74"):
        pieces = "21"
        prezsize = "2.74Go"
    elif (tsize == "4.37"):
        pieces = "22"
        prezsize = "4.37Go"
    elif (tsize == "6.56"):
        pieces = "22"
        prezsize = "6.56Go"
    elif (tsize == "hd"):
        pieces = "22"
        prezsize = "..Go"
    else:
        pieces = "20"
        prezsize = "..Go"

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

# ANKOA_PROCESS

banner()
(
    source, thumb, team, announce, title, year, stag, string, codec,
    encode_type, crf, bit, level, idvideo, fps, interlace, interlace2,
    audiolang, audio_config, sub_config, sub_remux, reso, param, pass1,
    mark, nfoimdb, nfosource, titlesub, subforced, prezquality, prezsize,
    pieces, name, pprint
) = main()

run_ffmpeg = [ffmpeg(), "", "", "", "", "", "", "", "",
              "", "", "", "", "", "", "", "", "", "", ""]

run_data = [data(), "", "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "", "", "", ""]

n = 1
if (pprint == "y"):
    print (ffmpeg())

again = raw_input("{0}NEXT ENCODE {1}(y/n){0} : {2}"
                  .format(GREEN, YELLOW, END))

while (again != "n"):
    next()
    (
        source, thumb, team, announce, title, year, stag, string, codec,
        encode_type, crf, bit, level, idvideo, fps, interlace, interlace2,
        audiolang, audio_config, sub_config, sub_remux, reso, param, pass1,
        mark, nfoimdb, nfosource, titlesub, subforced, prezquality, prezsize,
        pieces, name, pprint, pending
    ) = main()

    run_ffmpeg[n] = ffmpeg()
    run_data[n] = data()
    n = n + 1

    if (n != 20):
        again = raw_input("{0}NEXT ENCODE {1}(y/n){0} : {2}"
                          .format(GREEN, YELLOW, END))
    else:
        break

for i in range(n):
    os.system(run_ffmpeg[i])
    os.system(run_data[i])
    i = i + 1

print ("{0}\n ->{1} ALL JOBS DONE, CONGRATULATIONS !\n{0} ->{1} NFO, THUMB"
       "NAILS, (PREZ) & TORRENT CREATED !\n{2}".format(RED, GREEN, END))

sys.exit()

if (__name__ == "__main__"):
    main()
