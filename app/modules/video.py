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

from __future__ import absolute_import
import re
import os
from app.main.param import regex
from app.modules.bitrate import *
from app.main.inputs import *
from app.main.events import *

(hb_regex, crf_regex, delay_regex, fp_regex, aq_regex, url_regex) = regex()


# Select Video Track ID
def select_video_ID():
    idvideo = ask_ffmped_ID()
    verif_t0 = re.compile(crf_regex, flags=0).search(idvideo)
    while not idvideo or len(idvideo) > 2 or idvideo.isdigit() is False\
            or verif_t0 is not None:
        bad_video_ID()
        idvideo = ask_ffmped_ID()
        verif_t0 = re.compile(crf_regex, flags=0).search(idvideo)
    return idvideo


# Video Format
def video_format():
    format = ask_rls_format()
    form_resp = ["1", "2", "3", "4", "5", "6", "7"]
    form_values = ["", "HDTV", "PDTV", "BDRip", "DVDRip",
                   "BRRip", "BluRay", "720p", "1080p", "HR"]
    hd = False

    # When PDTV
    if (format == "2"):

        # HR.PDTV ?
        hr = ask_HR_PDTV()
        if (hr == "y"):
            form = "{0}.{1}".format(form_values[9], form_values[2])
            hd_size = "sd"
        else:
            form = form_values[2]
            hd_size = "sd"

    # When BluRay or HDTV
    elif (format == "6" or format == "1"):

        # When HDTV
        if (format == "1"):

            # HDTV 720p or 1080p ?
            hd_hdtv = ask_HD_HDTV()
            if (hd_hdtv == "y"):
                hd = True
            else:
                form = form_values[1]
                hd_size = "sd"

        # When BluRay
        elif (format == "6"):
            hd = True

        # 720p or 1080p ?
        if (hd is True):

            hd_size = ask_HD_size()
            while not hd_size or len(hd_size) != 1\
                    or hd_size.isdigit() is False\
                    or int(hd_size) < 1 or int(hd_size) > 2:
                bad_hd_size()
                hd_size = ask_HD_size()

            # 1080p
            if (hd_size == "2"):
                form = "{0}.{1}".format(form_values[8],
                                        form_values[int(format)])

            # 720p
            else:
                form = "{0}.{1}".format(form_values[7],
                                        form_values[int(format)])
    # Else and when match list
    elif (format in form_resp):
        form = form_values[int(format)]
        hd_size = "sd"

    # Nothing or error -> BBRip
    else:
        form = form_values[5]
        hd_size = "sd"

    return (format, form, hd_size)


# Video Codec
def video_codec():
    codec_type = ask_video_codec()
    if (codec_type == "2"):
        codec = "libx265"
        xcod = "x265"
    else:
        codec = "libx264"
        xcod = "x264"
    codec_val = (codec, xcod)
    return codec_val


# Video Container ( mp4 or mkv )
def video_container():
    rlstype = ask_rls_container()
    if (rlstype == "1"):
        string = "mp4"
        extend = ".{0}".format(string)
    else:
        string = "matroska"
        extend = ".mkv"
    container_val = (string, extend)
    return container_val


# CRF Value
def ffmpeg_crf():
    crf = ask_crf_level()
    verif1a = re.compile(crf_regex, flags=0).search(crf)
    while not crf or len(crf) > 2 or crf.isdigit() is False\
            or verif1a is not None or int(crf) > 51:
        bad_crf()
        crf = ask_crf_level()
        verif1a = re.compile(crf_regex, flags=0).search(crf)
    return crf


# 2PASS bitrate
def ffmpeg_2pass(calculator):

    # Birate Calculator
    if (calculator == "y"):
        next = "y"
        while (next == "y"):
            HH, MM, SS, audiobit, rls_size, calsize = calcul()
            run_calc = calc(HH, MM, SS, audiobit, rls_size, calsize)
            try:
                os.system(run_calc)
            except OSError as e:
                global_error(e)
                sys.exit()
            next = ask_try_again()

    # Video bitrate ( min: 750Kbps / max: 30Mbps )
    bit = ask_video_bitrate()
    verif1b = re.compile(crf_regex, flags=0).search(bit)

    while not bit or bit.isdigit() is False or verif1b is not None\
            or int(bit) < 750 or int(bit) > 30000:
        bad_video_bitrate()
        bit = ask_video_bitrate()
        verif1b = re.compile(crf_regex, flags=0).search(bit)

    return bit


# Change Video FPS
def video_fps():
    fps = ""
    modif_fps = ask_modif_fps()
    if (modif_fps == "y"):
        set_fps = ask_video_fps()
        fps_val = ['24', '25', '23.98', '29.97', '30', '50',
                   '59.94', '60', '72', '120', '300']

        while set_fps not in fps_val or not set_fps:
            bad_fps()
            set_fps = ask_video_fps()

        fps = " -r {0}".format(set_fps)

    return fps


# Deinterlace Video ( yadif filter )
def deinterlace(encode_type):
    [interlace, interlace2] = ["", ] * 2
    deinterlace = ask_deinterlace()
    if (deinterlace == "y"):
        interlace = " -filter:v yadif=deint=0 "
        if (encode_type != "3"):
            interlace2 = " -filter:v yadif=deint=1 "

    return (interlace, interlace2)
