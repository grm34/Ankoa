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
import json
import socket
import urllib2
import readline
import optparse
import commands
import subprocess
from json import loads
from urllib2 import (Request, urlopen, URLError, HTTPError, unquote)
from django.utils.encoding import (smart_str, smart_unicode)
from settings import (option, bad_chars, regex)
from bitrate import (calcul, calc)
from advanced import advanced_mode
from genprez import api_connexion
from inputs import *
from events import *

deleted = bad_chars()
(hb_regex, crf_regex, delay_regex, fp_regex, aq_regex) = regex()
(folder, thumb, tag, team, announce, tmdb_api_key, tag_thumb) = option()


def ANKOA_SYSTEM():

    # Auto Complete
    def completer(text, state):
        return (
            [entry.replace(' ', '\ ') for entry in os.listdir(
                folder + os.path.dirname(
                    readline.get_line_buffer())
                ) if entry.startswith(text)][state])

    # Select Source
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)
    prefix = ask_source()
    while not prefix or os.path.isfile(folder+prefix) is False:
        bad_source()
        prefix = ask_source()
    readline.parse_and_bind("tab: ")
    source = "{0}{1}".format(folder, prefix)

    # Release Title
    title = ask_title()
    while not title:
        bad_title()
        title = ask_title()

    # Clean Title
    for d_char in deleted:
        if d_char in title.strip():
            title = smart_str(title).strip().replace(' ', '.')\
                                            .replace(d_char, '')
        else:
            title = smart_str(title).strip().replace(' ', '.')

    # Release Year ( min: 1895 [1st movie] / max: 2080 ? )
    year = ask_year()
    while not year or year.isdigit() is False or len(year) != 4\
            or int(year) < 1895 or int(year) > 2080:
        bad_year()
        year = ask_year()

    # Special Tag
    special = ask_tag()
    if not (special):
        stag = ""
    else:

        # Clean Special Tag
        for d_char in deleted:
            if d_char in special.strip():
                special = smart_str(special).strip().replace(' ', '.')\
                                                    .replace(d_char, '')
            else:
                special = smart_str(special).strip().replace(' ', '.')

        stag = ".{0}".format(special)

    # Scan commands
    scan = [
        "HandBrakeCLI -t 0 --scan -i " + source,
        "ffmpeg -i " + source,
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

    # Scan Process
    scan_again = "y"
    while (scan_again == "y"):
        type = ask_scan_type()
        try:

            # Get FFMPEG / HANDBRAKE infos
            if (type == "1" or type == "2"):
                hb = smart_str(commands.getoutput("{0}"
                                                  .format(scan[int(type)-1])))

            # Get MEDIAINFO infos
            else:
                hb = ""
                for x in range(2, 16):
                    hb += "\n" +\
                          smart_str(commands.getoutput("{0}".format(scan[x])))
                    x = x + 1

            # Write infos
            hb_out = file("{0}{1}.{2}_scan.txt"
                          .format(thumb, title, year), "w").write(hb)
            hb_data = file("{0}{1}.{2}_scan.txt"
                           .format(thumb, title, year), "r").readlines()

            # Run HANDBRAKE Scan
            if (type == "1"):
                for lines in hb_data:
                    verif0 = re.compile(hb_regex, flags=0).search(lines)
                    if ("+ duration:" in lines or "Stream #" in lines
                            or "+ size:" in lines or "autocrop" in lines
                            or verif0 is not None):
                        print lines.strip().replace('\n', '')

            # Run FFMPEG Scan
            elif (type == "2"):
                for lines in hb_data:
                    if ("Duration:" in lines or "Stream #" in lines):
                        print lines.strip().replace('\n', '')

            # Run MEDIAINFO Scan
            else:
                for lines in hb_data:
                    if (lines != "\n" and lines.strip() != "-"):
                        print lines.strip()

            os.system("rm -f {0}{1}.{2}_scan.txt".format(thumb, title, year))

        # Scan Error
        except (OSError) as e:
            global_error()
            sys.exit()

        # Scan again ?
        scan_again = ask_scan_again()

    # Video Codec
    codec_type = ask_video_codec()
    if (codec_type == "2"):
        codec = "libx265"
        xcod = "x265"
    else:
        codec = "libx264"
        xcod = "x264"

    # CRF / 2PASS ?
    encode_type = ask_2pass_crf()

    # FFMPEG CRF
    if (encode_type == "2"):
        bit = ""
        crf = ask_crf_level()
        verif1a = re.compile(crf_regex, flags=0).search(crf)
        while not crf or len(crf) > 2 or crf.isdigit() is False\
                or verif1a is not None or int(crf) > 51:
            bad_crf()
            crf = ask_crf_level()
            verif1a = re.compile(crf_regex, flags=0).search(crf)

    # FFMPEG 2PASS
    else:
        crf = ""
        calculator = ask_bitrate_calculator()

        # Birate Calculator
        if (calculator == "y"):
            next = "y"
            while (next == "y"):
                HH, MM, SS, audiobit, rls_size, calsize = calcul()
                run_calc = calc(HH, MM, SS, audiobit, rls_size, calsize)
                try:
                    os.system(run_calc)
                except OSError as e:
                    global_error()
                    sys.exit()
                next = ask_try_again()

        # Video bitrate ( min: 750Kbps / max: 100Mbps )
        bit = ask_video_bitrate()
        verif1b = re.compile(crf_regex, flags=0).search(bit)
        while not bit or bit.isdigit() is False or verif1b is not None\
                or int(bit) < 750 or int(bit) > 100000:
            bad_video_bitrate()
            bit = ask_video_bitrate()
            verif1b = re.compile(crf_regex, flags=0).search(bit)

    # Video Format
    format = ask_rls_format()
    form_resp = ["1", "2", "3", "4", "5", "6", "7"]
    form_values = ["", "HDTV", "PDTV", "BDRip", "DVDRip",
                   "BRRip", "720p.BluRay", "HR.PDTV"]
    if (format in form_resp):
        form = form_values[int(format)]
    else:
        form = form_values[5]

    # HR.PDTV ?
    if (format == "2"):
        hr = ask_HR_PDTV()
        if (hr == "y"):
            format = "7"

    # Video Container ( mp4 or mkv )
    rlstype = ask_rls_container()
    if (rlstype == "1"):
        string = "mp4"
        extend = ".mp4"
    else:
        string = "matroska"
        extend = ".mkv"

    # Scan Source Tracks
    scan2 = ask_ffmpeg_scan()
    if (scan2 == "y"):
        try:
            hb = smart_str(commands.getoutput("{0}".format(scan[1])))
            hb_out = file("{0}{1}.{2}_scan.txt"
                          .format(thumb, title, year), "w").write(hb)
            hb_data = file("{0}{1}.{2}_scan.txt"
                           .format(thumb, title, year), "r").readlines()
            for lines in hb_data:
                if ("Stream #" in lines):
                    print lines.strip().replace('\n', '')
            os.system("rm -f {0}{1}.{2}_scan.txt".format(thumb, title, year))

        # Scan Error
        except OSError as e:
            global_error()
            sys.exit()

    # Select Video Track
    idvideo = ask_ffmped_ID()
    verif_t0 = re.compile(crf_regex, flags=0).search(idvideo)
    while not idvideo or len(idvideo) > 2 or idvideo.isdigit() is False\
            or verif_t0 is not None:
        bad_video_ID()
        idvideo = ask_ffmped_ID()
        verif_t0 = re.compile(crf_regex, flags=0).search(idvideo)

    # Change Video FPS
    modif_fps = ask_modif_fps()
    if (modif_fps == "y"):
        set_fps = ask_video_fps()
        fps_val = ['24', '25', '23.98', '29.97', '30', '50',
                   '59.94', '60', '72', '120', '300']

        while set_fps not in fps_val or not set_fps:
            bad_fps()
            set_fps = ask_video_fps()

        fps = " -r {0}".format(set_fps)
    else:
        fps = ""

    # Deinterlace Video ( yadif filter )
    deinterlace = ask_deinterlace()
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
    audiotype = ask_audio_type()

    # Single Audio Track
    if (audiotype == "1" or audiotype == "2" or audiotype == "3"):

        # Select Audio Track
        audionum = ask_audio_track00()
        verif_t1 = re.compile(crf_regex, flags=0).search(audionum)
        while not audionum or len(audionum) > 2\
                or audionum.isdigit() is False or verif_t1 is not None:
            bad_audio_ID()
            audionum = ask_audio_track00()
            verif_t1 = re.compile(crf_regex, flags=0).search(audionum)

        # Audio Track Title
        if (audiotype == "3"):
            audiolang = ask_audiolang00()
            while not audiolang:
                bad_audio_title()
                audiolang = ask_audiolang00()

            # Clean Audio Track Title
            for d_char in deleted:
                if d_char in audiolang.strip():
                    audiolang = smart_str(audiolang).strip()\
                                                    .replace(' ', '.')\
                                                    .replace(d_char, '')
                else:
                    audiolang = smart_str(audiolang).strip().replace(' ', '.')

        # Audio Track Codec
        audiocodec = ask_audio_codec00()
        while audiocodec not in codec_resp:
            bad_audio_codec()
            audiocodec = ask_audio_codec00()

        # Audio Codec AC3
        if (audiocodec == "2"):

            # Audio Track bitrate ( min: 96Kbps / max: 3000Kbps )
            abitrate = ask_audio_bitrate00()
            verif_b0 = re.compile(crf_regex, flags=0).search(abitrate)
            while not abitrate or abitrate.isdigit() is False\
                    or verif_b0 is not None\
                    or int(abitrate) < 96 or int(abitrate) > 3000:
                bad_audio_bitrate()
                abitrate = ask_audio_bitrate00()
                verif_b0 = re.compile(crf_regex, flags=0).search(abitrate)

            # Audio Track Channels ( max 11 [9.2] )
            surround = ask_audio_channels00()
            verif_s0 = re.compile(crf_regex, flags=0).search(abitrate)
            while not surround or surround.isdigit() is False\
                    or verif_s0 is not None or int(surround) > 11:
                bad_audio_surround()
                surround = ask_audio_channels00()
                verif_s0 = re.compile(crf_regex, flags=0).search(abitrate)

    # Multi Audio Tracks
    elif (audiotype == "4"):

        # Select Audio Track 01
        audionum = ask_audio_track01()
        verif_t2 = re.compile(crf_regex, flags=0).search(audionum)
        while not audionum or len(audionum) > 2\
                or audionum.isdigit() is False or verif_t2 is not None:
            bad_audio_ID()
            audionum = ask_audio_track01()
            verif_t2 = re.compile(crf_regex, flags=0).search(audionum)

        # Audio Track 01 Title
        audiolang = ask_audiolang01()
        while not audiolang:
            bad_audio_title()
            audiolang = ask_audiolang01()

        # Clean Audio Track 01 Title
        for d_char in deleted:
            if d_char in audiolang.strip():
                audiolang = smart_str(audiolang).strip()\
                                                .replace(' ', '.')\
                                                .replace(d_char, '')
            else:
                audiolang = smart_str(audiolang).strip().replace(' ', '.')

        # Audio Track 01 Codec
        audiocodec = ask_audio_codec01()
        while audiocodec not in codec_resp:
            bad_audio_codec()
            audiocodec = ask_audio_codec01()

        # Track 01 Codec AC3
        if (audiocodec == "2"):

            # Audio Track 01 bitrate ( min: 96Kbps / max: 3000Kbps )
            abitrate = ask_audio_bitrate01()
            while not abitrate or abitrate.isdigit() is False\
                    or int(abitrate) < 96 or int(abitrate) > 3000:
                bad_audio_bitrate()
                abitrate = ask_audio_bitrate01()

            # Audio Track 01 channels
            surround = ask_audio_channels01()
            while not surround or surround.isdigit() is False\
                    or innt(surround) > 11:
                bad_audio_surround()
                surround = ask_audio_channels01()

        # Select Audio Track 02
        audionum2 = ask_audio_track02()
        verif_t3 = re.compile(crf_regex, flags=0).search(audionum2)
        while not audionum2 or len(audionum2) > 2\
                or audionum2.isdigit() is False or verif_t3 is not None:
            bad_audio_ID()
            audionum2 = ask_audio_track02()
            verif_t3 = re.compile(crf_regex, flags=0).search(audionum2)

        # Audio Track 02 Title
        audiolang2 = ask_audiolang02()
        while not audiolang2:
            bad_audio_title()
            audiolang2 = ask_audiolang02()

        # Clean Audio Track 01 Title
        for d_char in deleted:
            if d_char in audiolang2.strip():
                audiolang2 = smart_str(audiolang2).strip()\
                                                  .replace(' ', '.')\
                                                  .replace(d_char, '')
            else:
                audiolang2 = smart_str(audiolang2).strip().replace(' ', '.')

        # Audio Track 02 Codec
        audiocodec2 = ask_audio_codec02()
        while audiocodec2 not in codec_resp:
            bad_audio_codec()
            audiocodec2 = ask_audio_codec02()

        # Track 02 Codec AC3
        if (audiocodec2 == "2"):

            # Audio Track 02 bitrate ( min: 96Kbps / max: 3000Kbps )
            abitrate2 = ask_audio_bitrate02()
            verif_b1 = re.compile(crf_regex, flags=0).search(abitrate2)
            while not abitrate or abitrate.isdigit() is False\
                    or verif_b1 is not None\
                    or int(abitrate) < 96 or int(abitrate) > 3000:
                bad_audio_bitrate()
                abitrate2 = ask_audio_bitrate02()
                verif_b1 = re.compile(crf_regex, flags=0).search(abitrate2)

            # Audio Track 02 channels
            surround2 = ask_audio_channels02()
            verif_s1 = re.compile(crf_regex, flags=0).search(surround2)
            while not surround2 or surround2.isdigit() is False\
                    or verif_s1 is not None or int(surround2) > 11:
                bad_audio_surround()
                surround2 = ask_audio_channels02()
                verif_s1 = re.compile(crf_regex, flags=0).search(surround2)
    # No Audio
    else:
        audiocodec = ""

    # Change Audio Sampling Rate ( min: 16k / max: 192k )
    if (audiotype == "1" or audiotype == "2"
            or audiotype == "3" or audiotype == "4"):
        audiox = ask_modif_sampling_rate()
        if (audiox == "y"):
            sampling_val = ['16', '32', '44', '48', '96', '192']

            # Multi Audio Tracks
            if (audiotype == "4"):

                # Audio Track 01 Sampling Rate
                ar1 = ask_audio_sampling_rate01()
                while ar1 not in sampling_val or not ar1:
                    bad_audio_sampling_rate()
                    ar1 = ask_audio_sampling_rate01()
                audiox = " -ar:a:0 {0}k".format(ar1)

                # Audio Track 02 Sampling Rate
                ar2 = ask_audio_sampling_rate02()
                while ar2 not in sampling_val or not ar2:
                    bad_audio_sampling_rate()
                    ar2 = ask_audio_sampling_rate02()
                    audiox2 = " -ar:a:1 {0}k".format(ar2)

            # Single Audio Track
            else:

                # Audio Track Sampling Rate
                ar = ask_audio_sampling_rate00()
                while ar not in sampling_val or not ar:
                    bad_audio_sampling_rate()
                    ar = ask_audio_sampling_rate00()
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
    if (audiocodec == "3"):                 # DTS
        mark = ".{0}.DTS.{1}-{2}{3}".format(lang, form, xcod, tag, extend)
        prezquality = "{0} DTS.{1}".format(form, xcod)
    elif (audiocodec == "2"):              # AC3
        mark = ".{0}.{1}.AC3.{2}-{3}{4}".format(lang, form, xcod, tag, extend)
        prezquality = "{0} AC3.{1}".format(form, xcod)
    else:                                 # MP3
        mark = ".{0}.{1}.{2}-{3}{4}".format(lang, form, xcod, tag, extend)
        prezquality = "{0} {1}".format(form, xcod)

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

    # Manual Subtitles Titles
    def manual_title_subs():

        # Subs Track 01 Title
        titlesub = ask_title_subs01()
        while not titlesub:
            bad_subs_title()
            titlesub = ask_title_subs01()

        # Clean Subs Track 01 Title
        for d_char in deleted:
            if d_char in titlesub.strip():
                titlesub = smart_str(titlesub).strip().replace(' ', '.')\
                                                      .replace(d_char, '')
            else:
                titlesub = smart_str(titlesub).strip().replace(' ', '.')

        # Subs Track 02 Title
        titlesub2 = ask_title_subs02()
        while not titlesub2:
            bad_subs_title()
            titlesub2 = ask_title_subs02()

        # Clean Subs Track 02 Title
        for d_char in deleted:
            if d_char in titlesub2.strip():
                titlesub2 = smart_str(titlesub2).strip().replace(' ', '.')\
                                                        .replace(d_char, '')
            else:
                titlesub2 = smart_str(titlesub2).strip().replace(' ', '.')

    # Subtitles Infos From Source
    def infos_subs_in():

        # MULTi SUBS (from Source)
        if (subtype == "3"):

            # From ISO/IMG
            if (subsource == "4"):

                # Subtitles Track 01 ISO ID
                idsub = ask_subs_ISO_ID01()
                verif_t4 = re.compile(crf_regex, flags=0).search(idsub)
                while not idsub or len(idsub) > 2\
                        or verif_t4 is not None or idsub.isdigit() is False:
                    bad_subtitles_ID()
                    idsub = ask_subs_ISO_ID01()
                    verif_t4 = re.compile(crf_regex, flags=0).search(idsub)

                # Subtitles Tracks 02 ISO ID
                idsub2 = ask_subs_ISO_ID02()
                verif_t5 = re.compile(crf_regex, flags=0).search(idsub2)
                while not idsub2 or len(idsub2) > 2\
                        or verif_t5 is not None or idsub2.isdigit() is False:
                    bad_subtitles_ID()
                    idsub2 = ask_subs_ISO_ID02()
                    verif_t5 = re.compile(crf_regex, flags=0).search(idsub2)

            # From MKV or M2TS
            else:

                # Subtitles Track 01 FFMPEG ID
                idsub = ask_subs_FFMPEG_ID01()
                verif_t6 = re.compile(crf_regex, flags=0).search(idsub)
                while not idsub or len(idsub) > 2\
                        or verif_t6 is not None or idsub.isdigit() is False:
                    bad_subtitles_ID()
                    idsub = ask_subs_FFMPEG_ID01()
                    verif_t6 = re.compile(crf_regex, flags=0).search(idsub)

                # Subtitles Track 02 FFMPEG ID
                idsub2 = ask_subs_FFMPEG_ID02()
                verif_t7 = re.compile(crf_regex, flags=0).search(idsub2)
                while not idsub2 or len(idsub2) > 2\
                        or verif_t7 is not None or idsub2.isdigit() is False:
                    bad_subtitles_ID()
                    idsub2 = ask_subs_FFMPEG_ID02()
                    verif_t7 = re.compile(crf_regex, flags=0).search(idsub2)
                manual_title_subs()

        # Single SUBS (from Source)
        else:

            # From ISO/IMG
            if (subsource == "4"):

                # Subtitles Track ISO ID
                idsub = ask_subs_ISO_ID00()
                verif_t8 = re.compile(crf_regex, flags=0).search(idsub)
                while not idsub or len(idsub) > 2\
                        or verif_t8 is not None or idsub.isdigit() is False:
                    bad_subtitles_ID()
                    idsub = ask_subs_ISO_ID00()
                    verif_t8 = re.compile(crf_regex, flags=0).search(idsub)

            # From MKV or M2TS
            else:

                # Subtitles Track FFMPEG ID
                idsub = ask_subs_FFMPEG_ID00()
                verif_t9 = re.compile(crf_regex, flags=0).search(idsub)
                while not idsub or len(idsub) > 2\
                        or verif_t9 is not None or idsub.isdigit() is False:
                    bad_subtitles_ID
                    idsub = ask_subs_FFMPEG_ID00()
                    verif_t9 = re.compile(crf_regex, flags=0).search(idsub)

            # Subtitles Track Title
            if (subtype == "1"):
                titlesub = "FULL.FRENCH"
            elif (subtype == "2"):
                titlesub = "FRENCH.FORCED"
            idsub2 = ""
            titlesub2 = ""

        # RETURN Subtitles Infos From Source
        infos_subs_in = (idsub, titlesub, idsub2, titlesub2)
        return (infos_subs_in)

    # Subtitles Infos From Location
    def infos_subs_out():
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)

        # MULTi SUBS (from Location)
        if (subtype == "3"):

            # Subtitles Track 01 Location
            ub = ask_subs_source01()
            while not ub or os.path.isfile(folder+ub) is False:
                bad_subtitles_source()
                ub = ask_subs_source01()

            # Subtitles Track 02 Location
            ub2 = ask_subs_source02()
            while not ub2 or os.path.isfile(folder+ub2) is False:
                bad_subtitles_source()
                ub2 = ask_subs_source02()

            readline.parse_and_bind("tab: ")
            idsub = "{0}{1}".format(folder, ub)
            idsub2 = "{0}{1}".format(folder, ub2)

            # Subtitles Tracks Titles (from Location)
            if (subsource == "3"):
                manual_title_subs()

        # Single SUBS (from Location)
        else:

            # Subtitles Track Location
            ub = ask_subs_source00()
            while not ub or os.path.isfile(folder+ub) is False:
                bad_subtitles_source()
                ub = ask_subs_source00()

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
            idcharset = ask_subcharset01()
            idcharset2 = ask_subcharset02()

        # Subtitles Charset - Single SUBS
        else:
            idcharset = ask_subcharset00()

        # Subtitles Charset Config
        if (idcharset == "y"):
            charset = " --sub-charset '0:cp1252'"
        else:
            charset = ""
        if (subtype == "3" and idcharset2 == "y"):
            charset2 = " --sub-charset '0:cp1252'"
        else:
            charset2 = ""

        # Subtitles Delay
        subsync = ask_apply_subdelay()
        if (subsync == "y"):

            # Delay MULTi SUBS
            if (subtype == "3"):
                subdelay1 = ask_subs_delay01()
                verif2 = re.compile(delay_regex, flags=0).search(subdelay1)
                while not subdelay1 or verif2 is None:
                    bad_subs_delay()
                    subdelay1 = ask_subs_delay01()
                    verif2 = re.compile(delay_regex, flags=0).search(subdelay1)
                sync = "--sync 0:{0}".format(subdelay1)

                subdelay2 = ask_subs_delay02()
                verif3 = re.compile(delay_regex, flags=0).search(subdelay2)
                while not subdelay1 or verif3 is None:
                    bad_subs_delay()
                    subdelay2 = ask_subs_delay02()
                    verif3 = re.compile(delay_regex, flags=0).search(subdelay2)
                sync2 = "--sync 0:{0} ".format(subdelay2)

            # Delay Single SUBS
            else:
                subdelay = ask_subs_delay00()
                verif4 = re.compile(delay_regex, flags=0).search(subdelay)
                while not subdelay or verif4 is None:
                    bad_subs_delay()
                    subdelay = ask_subs_delay00()
                    verif4 = re.compile(delay_regex, flags=0).search(subdelay)
                sync = "--sync 0:{0}".format(subdelay)
                sync2 = ""
        else:
            sync = ""
            sync2 = ""

        # RETURN Subtitles Infos From Location
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

    # Subtitles Format (from MKV)
    def mkv_format():

        # MULTi SUBS (from mkv)
        if (subtype == "3"):
            ext = ask_subs_format01()
            ext2 = ask_subs_format02()

        # Single SUBS (from mkv)
        else:
            ext = ask_subs_format00()
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

        # RETURN Subtitles Format (from MKV )
        subext = (ext, ext2)
        return (subext)

    # Subtitles Extract from MKV
    def mkv_extract():
        if (subtype == "3"):
            if (ext == "1" and ext2 == "1"):   # EXTRACT MULTi PGS
                return (
                    "cd {0} && mkvextract tracks {1} {2}:{3}1{4} && mkvex"
                    "tract tracks {1} {5}:{3}2{6} && mv {3}1{4} {3}1.sup "
                    "&& mv {3}2{6} {3}2.sup"
                    .format(thumb, source, idsub,
                            title, ext, idsub2, ext2))

            else:                           # EXTRACT MULTi SRT/ASS/VOBSUB
                return (
                    "cd {0} && mkvextract tracks {1} {2}:{3}1{4} && mkvextrac"
                    "t tracks {1} {5}:{3}2{6}"
                    .format(thumb, source, idsub,
                            title, ext, idsub2, ext2))
        else:
            if (ext == "1"):            # EXTRACT SINGLE PGS
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
    subsource = ask_subs_from()

    if (subsource == "1" or subsource == "3" or subsource == "4"
            or subsource == "5" or subsource == "6"):

        # Subtitles Type
        subtype = ask_subs_type()

        # from SOURCE
        if (subsource == "1"):

            # Subforced MULTi AUDIO
            if (audiotype == "4"):
                if (subtype == "1"):        # FRENCH
                    forced = "--forced-track 3:no "
                elif (subtype == "2"):      # FORCED
                    forced = "--forced-track 3:yes "
                else:                       # MULTi
                    ask_subforced()
                    if (stforced == "y"):
                        forced = "--forced-track 4:yes "
                    else:
                        forced = "--forced-track 4:no "

            # Subforced SINGLE AUDIO
            else:
                if (subtype == "1"):        # FRENCH
                    forced = "--forced-track 2:no "
                elif (subtype == "2"):      # FORCED
                    forced = "--forced-track 2:yes "
                else:                       # MULTi
                    ask_subforced()
                    if (stforced == "y"):
                        forced = "--forced-track 3:yes "
                    else:
                        forced = "--forced-track 3:no "

        # from FILE or ISO/IMG or M2TS or MKV
        elif (subsource == "3" or subsource == "4"
                or subsource == "5" or subsource == "6"):

            if (subtype == "1"):            # FRENCH
                forced = "--forced-track '0:no' "
            elif (subtype == "2"):          # FORCED
                forced = "--forced-track '0:yes' "
            else:                           # MULTi
                ask_subforced()
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
                global_error()
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
                global_error()
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
                global_error()
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

    # Custom Aspect Ratio ( min: 320x200 / max: 3840x2160 [4K] )
    def custom():

        # Resolution WIDTH
        W = ask_reso_width()
        verif_W = re.compile(crf_regex, flags=0).search(W)
        while not W or W.isdigit() is False or verif_W is not None\
                or int(W) < 320 or int(W) > 3840:
            bad_reso_width()
            W = ask_reso_width()
            verif_W = re.compile(crf_regex, flags=0).search(W)

        # Resolution HEIGHT
        H = ask_reso_height()
        verif_H = re.compile(crf_regex, flags=0).search(H)
        while not H or H.isdigit() is False or verif_H is not None\
                or int(H) < 200 or int(H) > 2160:
            bad_reso_height()
            H = ask_reso_height()
            verif_H = re.compile(crf_regex, flags=0).search(H)

        reso = " -s {0}x{1}{2}".format(W, H, crop)
        return (reso)

    # DVD Aspect Ratio
    def DVD():

        # Custom Resolution
        perso = ask_custom_reso()
        if (perso == "y"):
            reso = custom()
        else:

            # Sample Aspect Ratio
            ask_sar = ask_use_reso_sar()
            if (ask_sar == "y"):
                sar = ask_reso_sar()
                sar_resp = ["1", "2", "3", "4"]
                sar_val = ["", "64:45", "16:15", "32:27", "8:9"]

                while sar not in sar_resp:
                    bad_sar()
                    ask_sar = ask_use_reso_sar()
                reso = " -sar {0}{1}".format(sar_val[int(sar)], crop)

            # Standard reso
            else:
                reso = BLURAY()
        return (reso)

    # BluRay Aspect Ratio
    def BLURAY():

        # Custom Resolution
        perso = ask_custom_reso()
        if (perso == "y"):
            reso = custom()

        # Standard Resolution ( reso scene 2013 )
        else:
            ratio = ask_aspect_ratio()
            ratio_resp = ["1", "2", "3", "4", "5", "6"]
            ratio_val = ["", "720x540", "720x432", "720x404",
                         "720x390", "720x306", "720x300"]

            while ratio not in ratio_resp:
                bad_ar()
                ratio = ask_aspect_ratio()
            reso = " -s {0}".format(ratio_val[int(ratio)])
        return (reso)

    # Scan Autocrop
    scan_crop = ask_scan_autocrop()
    if (scan_crop == "y"):
        try:
            hb = smart_str(commands.getoutput("{0}".format(scan[0])))
            hb_out = file("{0}{1}.{2}_scan.txt"
                          .format(thumb, title, year), "w").write(hb)
            hb_data = file("{0}{1}.{2}_scan.txt"
                           .format(thumb, title, year), "r").readlines()

            for lines in hb_data:
                if ("size:" in lines or "autocrop" in lines):
                    print lines.strip().replace('\n', '')

            os.system("rm -f {0}{1}.{2}_scan.txt".format(thumb, title, year))

        # Scan Error
        except OSError as e:
            global_error()
            sys.exit()

    # Screenshots Verification
    ask_screen = ask_screenshots()
    if (ask_screen == "y"):
        try:
            os.system("./thumbnails.py {0} 5 2".format(source))

        # Screenshots Error
        except OSError as e:
            global_error()
            sys.exit()

    # Manual CROP ( min: 320x200 / max 3840x2160 [4K] )
    man_crop = ask_manual_crop()
    if (man_crop == "y"):

        # CROP Width
        w_crop = ask_W_crop()
        verif_crop1 = re.compile(crf_regex, flags=0).search(w_crop)
        while not w_crop or w_crop.isdigit() is False\
                or verif_crop1 is not None\
                or int(w_crop) < 320 or int(w_crop) > 3840:
            bad_crop_width()
            w_crop = ask_W_crop()
            verif_crop1 = re.compile(crf_regex, flags=0).search(w_crop)

        # CROP Height
        h_crop = ask_H_crop()
        verif_crop2 = re.compile(crf_regex, flags=0).search(h_crop)
        while not h_crop or h_crop.isdigit() is False\
                or verif_crop2 is not None\
                or int(h_crop) < 200 or int(h_crop) > 2160:
            bad_crop_height()
            h_crop = ask_H_crop()
            verif_crop2 = re.compile(crf_regex, flags=0).search(h_crop)

        # CROP Pixels LEFT/RIGHT
        x_crop = ask_LR_crop()
        verif_crop3 = re.compile(crf_regex, flags=0).search(x_crop)
        while not x_crop or x_crop.isdigit() is False\
                or verif_crop3 is not None or int(x_crop) > 1920:
            bad_crop_LR()
            x_crop = ask_LR_crop()
            verif_crop3 = re.compile(crf_regex, flags=0).search(x_crop)

        # CROP Pixels TOP/BOTTOM
        y_crop = ask_TB_crop()
        verif_crop4 = re.compile(crf_regex, flags=0).search(y_crop)
        while not y_crop or y_crop.isdigit() is False\
                or verif_crop4 is not None or int(y_crop) > 1080:
            bad_crop_TB()
            y_crop = ask_TB_crop()
            verif_crop4 = re.compile(crf_regex, flags=0).search(y_crop)

        # CROP Values
        crop = " -filter:v crop={0}:{1}:{2}:{3}"\
               .format(w_crop, h_crop, x_crop, y_crop)

    # No Crop
    else:
        crop = ""

    # Resolution PROCESS
    if (format == "4"):
        reso = DVD()
    elif (format == "6"):
        reso = custom()
    else:
        reso = BLURAY()

    # Video Format Profile ( min 1.1 / max: 5.2 )
    level = ask_format_profile()
    verif5 = re.compile(fp_regex, flags=0).search(level)
    while not level or len(level) != 3 or verif5 is None:
        bad_format_profile()
        level = ask_format_profile()
        verif5 = re.compile(fp_regex, flags=0).search(level)

    # Preset x264/x265
    preset = ask_x264_preset()
    preset_resp = ["1", "2", "3", "4", "5"]
    preset_values = ["", "fast", "slow", "slower", "veryslow", "placebo"]
    if (preset in preset_resp):
        preset = " -preset {0}".format(preset_values[int(preset)])
    else:
        preset = ""

    # Tune x264/x265
    tuned = ask_x264_tune()
    tuned_resp = ["1", "2", "3", "4", "5", "6", "7", "8"]
    tuned_values = ["", "film", "animation", "grain", "stillimage", "psnr",
                    "ssim", "fastdecode", "zerolatency"]
    if (tuned in tuned_resp):
        tune = " -tune {0}".format(tuned_values[int(tuned)])
    else:
        tune = ""

    # ADVANCED x264 MODE
    x264 = ask_advanced_mode()
    if (x264 == "y"):
        (param, pass1) = advanced_mode()

    # Default Threads Values
    else:
        param = "{0}{1} -threads 0".format(preset, tune)
        pass1 = "{0}{1} -threads 0".format(preset, tune)

    # Release SOURCE
    nfosource = ask_rls_source()
    while not nfosource:
        bad_nfosource()
        nfosource = ask_rls_source()

    # Clean NFOSOURCE
    for d_char in deleted:
        if d_char in nfosource.strip():
            nfosource = smart_str(nfosource).strip().replace(' ', '.')\
                                                    .replace(d_char, '')
        else:
            nfosource = smart_str(nfosource).strip().replace(' ', '.')

    # Release IMDB ID
    nfoimdb = ask_rls_imdb()

    # Find Release Title
    if (len(nfoimdb) == 7 and nfoimdb.isdigit() is True):
        imdb = nfoimdb
        scanning()
        (data_IMDB, data_TMDB,
         data_OMDB, data_API) = api_connexion(imdb)

        # Parse PREZ Title
        tit = ["title", "original_title", "Title", "title"]

        if (tit[0] in data_IMDB):
            dir = "{0}".format(smart_str(data_IMDB['title']))
        elif (tit[1] in data_TMDB):
            dir = "{0}".format(smart_str(data_TMDB['original_title']))
        elif (tit[2] in data_OMDB):
            dir = "{0}".format(smart_str(data_OMDB['Title']))
        elif (tit[3] in data_API):
            dir = "{0}".format(smart_str(data_API['title']))
        else:
            nfoimdb = ""

        # Clean PREZ Title
        if (tit[0] in data_IMDB or tit[1] in data_TMDB
                or tit[2] in data_OMDB or tit[3] in data_API):
            name = dir.replace(' ', '.').replace('/', '').replace('(', '')\
                      .replace(')', '').replace('"', '').replace(':', '')\
                      .replace("'", "").replace("[", "").replace("]", "")\
                      .replace(";", "").replace(",", "")
        else:
            name = "unknown"

    # while no prez
    else:
        nfoimdb = "empty"
        name = "unknown"

    # Print FFMPEG Command
    pprint = ask_print_ffmpeg()

    # Return Global Values
    info_main = (
        source, thumb, team, announce, title, year, stag, string, codec,
        encode_type, crf, bit, level, idvideo, fps, interlace, interlace2,
        audiolang, audio_config, sub_config, sub_remux, reso, param, pass1,
        mark, nfoimdb, nfosource, titlesub, subforced, prezquality,
        name, pprint
    )

    return (info_main)
