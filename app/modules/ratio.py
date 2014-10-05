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
import sys
from app.main.param import regex
from app.main.events import *
from app.main.inputs import *

(hb_regex, crf_regex, delay_regex, fp_regex, aq_regex, url_regex) = regex()


# Custom Aspect Ratio ( min: 320x200 / max: 1920x1080 )
def custom(crop):

    # Resolution WIDTH
    W = ask_reso_width()
    verif_W = re.compile(crf_regex, flags=0).search(W)
    while not W or W.isdigit() is False or verif_W is not None\
            or int(W) < 320 or int(W) > 1920:
        bad_reso_width()
        W = ask_reso_width()
        verif_W = re.compile(crf_regex, flags=0).search(W)

    # Resolution HEIGHT
    H = ask_reso_height()
    verif_H = re.compile(crf_regex, flags=0).search(H)
    while not H or H.isdigit() is False or verif_H is not None\
            or int(H) < 200 or int(H) > 1080:
        bad_reso_height()
        H = ask_reso_height()
        verif_H = re.compile(crf_regex, flags=0).search(H)

    reso = " -s {0}x{1}{2}".format(W, H, crop)
    return (reso)


# DVD Sample Aspect Ratio
def DVD(crop):
    ask_sar = ask_use_reso_sar()
    if (ask_sar == "y"):
        sar = ask_reso_sar()
        sar_resp = ["1", "2", "3", "4"]
        sar_val = ["", "64:45", "16:15", "32:27", "8:9"]

        while sar not in sar_resp:
            bad_sar()
            ask_sar = ask_use_reso_sar()
        reso = " -sar {0}{1}".format(sar_val[int(sar)], crop)
    else:
        reso = standard_SD(crop)
    return (reso)


# Standard SD Aspect Ratio
def standard_SD(crop):
    ratio = ask_aspect_ratio()
    ratio_resp = ["1", "2", "3", "4", "5", "6"]
    ratio_val = ["", "720x540", "720x432", "720x404",
                 "720x390", "720x306", "720x300"]

    while ratio not in ratio_resp:
        bad_ar()
        ratio = ask_aspect_ratio()
    reso = " -s {0}{1}".format(ratio_val[int(ratio)], crop)
    return (reso)


# Standard 720p Aspect Ratio
def standard_720p(crop):
    ratio = ask_aspect_ratio()
    ratio_resp = ["1", "2", "3", "4", "5", "6"]
    ratio_val = ["", "1280x960", "1280x768", "1280x720",
                 "1280x690", "1280x544", "1280x536"]

    while ratio not in ratio_resp:
        bad_ar()
        ratio = ask_aspect_ratio()
    reso = " -s {0}{1}".format(ratio_val[int(ratio)], crop)
    return (reso)


# Standard 1080p Aspect Ratio
def standard_1080p(crop):
    ratio = ask_aspect_ratio()
    ratio_resp = ["1", "2", "3", "4", "5", "6"]
    ratio_val = ["", "1440x1080", "1800x1080", "1920x1080",
                 "1920x1040", "1920x816", "1920x800"]

    while ratio not in ratio_resp:
        bad_ar()
        ratio = ask_aspect_ratio()
    reso = " -s {0}{1}".format(ratio_val[int(ratio)], crop)
    return (reso)


# Screenshots Verification
def screenshots_verif(source):
    ask_screen = ask_screenshots()
    if (ask_screen == "y"):
        try:
            os.system("./thumbnails.py {0} 5 2".format(source))

        # Screenshots Error
        except OSError as e:
            global_error(e)
            sys.exit()


# Manual CROP ( min: 320x200 / max 1920x1080 )
def manual_crop():
    crop = ""
    man_crop = ask_manual_crop()
    if (man_crop == "y"):

        # CROP Width
        w_crop = ask_W_crop()
        verif_crop1 = re.compile(crf_regex, flags=0).search(w_crop)
        while not w_crop or w_crop.isdigit() is False\
                or verif_crop1 is not None\
                or int(w_crop) < 320 or int(w_crop) > 1920:
            bad_crop_width()
            w_crop = ask_W_crop()
            verif_crop1 = re.compile(crf_regex, flags=0).search(w_crop)

        # CROP Height
        h_crop = ask_H_crop()
        verif_crop2 = re.compile(crf_regex, flags=0).search(h_crop)
        while not h_crop or h_crop.isdigit() is False\
                or verif_crop2 is not None\
                or int(h_crop) < 200 or int(h_crop) > 1080:
            bad_crop_height()
            h_crop = ask_H_crop()
            verif_crop2 = re.compile(crf_regex, flags=0).search(h_crop)

        # CROP Pixels LEFT/RIGHT
        x_crop = ask_LR_crop()
        verif_crop3 = re.compile(crf_regex, flags=0).search(x_crop)
        while not x_crop or x_crop.isdigit() is False\
                or verif_crop3 is not None or int(x_crop) > 320:
            bad_crop_LR()
            x_crop = ask_LR_crop()
            verif_crop3 = re.compile(crf_regex, flags=0).search(x_crop)

        # CROP Pixels TOP/BOTTOM
        y_crop = ask_TB_crop()
        verif_crop4 = re.compile(crf_regex, flags=0).search(y_crop)
        while not y_crop or y_crop.isdigit() is False\
                or verif_crop4 is not None or int(y_crop) > 200:
            bad_crop_TB()
            y_crop = ask_TB_crop()
            verif_crop4 = re.compile(crf_regex, flags=0).search(y_crop)

        # CROP Values
        crop = " -filter:v crop={0}:{1}:{2}:{3}"\
               .format(w_crop, h_crop, x_crop, y_crop)
    return crop
