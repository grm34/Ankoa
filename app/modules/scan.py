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
import readline
import commands
from user.settings import option
from app.main.param import regex
from app.main.events import (global_error)
from app.main.inputs import (ask_scan_type, ask_scan_again,
                             ask_ffmpeg_scan, ask_scan_autocrop)
from django.utils.encoding import (smart_str, smart_unicode)

(folder, thumb, tag, team, announce, tmdb_api_key, tag_thumb) = option()
(hb_regex, crf_regex, delay_regex, fp_regex, aq_regex, url_regex) = regex()


# Scan commands
def scan_command(source):
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
    return scan


# Scan Source Global Infos
def source_scan(source, title, year):
    scan = scan_command(source)
    scan_again = "y"
    while (scan_again == "y"):

        # Ask scan type
        type = ask_scan_type()
        try:

            # Get HANDBRAKE infos
            if (type == "1"):
                hb = smart_str(commands.getoutput("{0}".format(scan[0])))

            # Get MEDIAINFO infos
            elif (type == "3"):
                hb = ""
                for x in range(2, 16):
                    hb += "\n" +\
                          smart_str(commands.getoutput("{0}".format(scan[x])))
                    x = x + 1

            else:
                hb = smart_str(commands.getoutput("{0}".format(scan[1])))

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

            # Run MEDIAINFO Scan
            elif (type == "3"):
                for lines in hb_data:
                    if (lines != "\n" and lines.strip() != "-"):
                        print lines.strip()

            # Run FFMPEG Scan
            else:
                for lines in hb_data:
                    if ("Duration:" in lines or "Stream #" in lines):
                        print lines.strip().replace('\n', '')

            os.system("rm -f {0}{1}.{2}_scan.txt".format(thumb, title, year))

        # Scan Error
        except (OSError) as e:
            global_error(e)
            sys.exit()

        # Scan again ?
        scan_again = ask_scan_again()


# Scan Source Tracks
def ffmpeg_scan_tracks(source, title, year):
    scan = scan_command(source)
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
            global_error(e)
            sys.exit()


# Scan Aspect Ratio & autocrop
def scan_autocrop(source, title, year):
    scan = scan_command(source)
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
            global_error(e)
            sys.exit()
