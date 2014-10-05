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
from django.utils.encoding import (smart_str, smart_unicode)
from app.main.param import (bad_chars, regex)
from user.settings import option
from app.main.inputs import *
from app.main.events import *

deleted = bad_chars()
(folder, thumb, tag, team, announce, tmdb_api_key, tag_thumb) = option()
(hb_regex, crf_regex, delay_regex, fp_regex, aq_regex, url_regex) = regex()


# Manual Subtitles Titles
def manual_title_subs():

    # Track 01 Title
    titlesub = ask_title_subs01()
    while not titlesub:
        bad_subs_title()
        titlesub = ask_title_subs01()

    # Track 02 Title
    titlesub2 = ask_title_subs02()
    while not titlesub2:
        bad_subs_title()
        titlesub2 = ask_title_subs02()

    # Clean Tracks Titles
    for d_char in deleted:
        if d_char in titlesub.strip():
            titlesub = smart_str(titlesub).strip().replace(' ', '.')\
                                                  .replace(d_char, '')
        else:
            titlesub = smart_str(titlesub).strip().replace(' ', '.')

        if d_char in titlesub2.strip():
            titlesub2 = smart_str(titlesub2).strip().replace(' ', '.')\
                                                    .replace(d_char, '')
        else:
            titlesub2 = smart_str(titlesub2).strip().replace(' ', '.')
    return (titlesub, titlesub2)


# Auto Subtitles Titles
def auto_title_sub(subtype):
    titlesub2 = ""
    if (subtype == "1"):
        titlesub = "FULL.FRENCH"
    elif (subtype == "2"):
        titlesub = "FRENCH.FORCED"
    return (titlesub, titlesub2)


# Subtitles Tracks ID ( from ISO )
def subs_multi_handbrake_ID():

    # Subtitles Track 01 HANDBRAKE ID
    idsub = ask_subs_ISO_ID01()
    verif_t4 = re.compile(crf_regex, flags=0).search(idsub)
    while not idsub or len(idsub) > 2\
            or verif_t4 is not None or idsub.isdigit() is False:
        bad_subtitles_ID()
        idsub = ask_subs_ISO_ID01()
        verif_t4 = re.compile(crf_regex, flags=0).search(idsub)

    # Subtitles Tracks 02 HANDBRAKE ID
    idsub2 = ask_subs_ISO_ID02()
    verif_t5 = re.compile(crf_regex, flags=0).search(idsub2)
    while not idsub2 or len(idsub2) > 2\
            or verif_t5 is not None or idsub2.isdigit() is False:
        bad_subtitles_ID()
        idsub2 = ask_subs_ISO_ID02()
        verif_t5 = re.compile(crf_regex, flags=0).search(idsub2)
    return (idsub, idsub2)


def subs_solo_handbrake_ID():
    [idsub, idsub2] = ["", ] * 2

    # Subtitles Track HANDBRAKE ID
    idsub = ask_subs_ISO_ID00()
    verif_t8 = re.compile(crf_regex, flags=0).search(idsub)
    while not idsub or len(idsub) > 2\
            or verif_t8 is not None or idsub.isdigit() is False:
        bad_subtitles_ID()
        idsub = ask_subs_ISO_ID00()
        verif_t8 = re.compile(crf_regex, flags=0).search(idsub)
    return (idsub, idsub2)


# Subtitles Tracks ID ( from MKV or M2TS )
def subs_multi_ffmpeg_ID():

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
    return (idsub, idsub2)


def subs_solo_ffmpeg_ID():
    [idsub, idsub2] = ["", ] * 2

    # Subtitles Track FFMPEG ID
    idsub = ask_subs_FFMPEG_ID00()
    verif_t9 = re.compile(crf_regex, flags=0).search(idsub)
    while not idsub or len(idsub) > 2\
            or verif_t9 is not None or idsub.isdigit() is False:
        bad_subtitles_ID()
        idsub = ask_subs_FFMPEG_ID00()
        verif_t9 = re.compile(crf_regex, flags=0).search(idsub)
    return (idsub, idsub2)


# Subtitles Location ( from FILE )
def subs_file_multi():

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

    idsub = "{0}{1}".format(folder, ub)
    idsub2 = "{0}{1}".format(folder, ub2)
    return (idsub, idsub2)


def subs_file_solo():
    [idsub, idsub2] = ["", ] * 2

    # Subtitles Track Location
    ub = ask_subs_source00()
    while not ub or os.path.isfile(folder+ub) is False:
        bad_subtitles_source()
        ub = ask_subs_source00()
    idsub = "{0}{1}".format(folder, ub)
    return (idsub, idsub2)


def subcharset_ANSI(idcharset, idcharset2):
    [charset, charset2] = ["", ] * 2
    charset_ANSI = " --sub-charset '0:cp1252'"
    if (idcharset == "y"):
        charset = charset_ANSI
    if idcharset2:
        charset2 = charset_ANSI
    return (charset, charset2)


# Subtitles Delay
def subdelay_multi():
    [sync, sync2] = ["", ] * 2
    subsync = ask_use_subdelay()
    if (subsync == "y"):

        subdelay1 = ask_subs_delay01()
        verif2 = re.compile(delay_regex, flags=0).search(subdelay1)
        while not subdelay1 or verif2 is None:
            bad_subs_delay()
            subdelay1 = ask_subs_delay01()
            verif2 = re.compile(delay_regex, flags=0).search(subdelay1)
        sync = "--sync 0:{0} ".format(subdelay1)

        subdelay2 = ask_subs_delay02()
        verif3 = re.compile(delay_regex, flags=0).search(subdelay2)
        while subdelay2 or verif3 is None:
            bad_subs_delay()
            subdelay2 = ask_subs_delay02()
            verif3 = re.compile(delay_regex, flags=0).search(subdelay2)
        sync2 = "--sync 0:{0} ".format(subdelay2)
    return (sync, sync2)


def subdelay_solo():
    [sync, sync2] = ["", ] * 2
    subsync = ask_use_subdelay()
    if (subsync == "y"):

        subdelay = ask_subs_delay00()
        verif4 = re.compile(delay_regex, flags=0).search(subdelay)
        while not subdelay or verif4 is None:
            bad_subs_delay()
            subdelay = ask_subs_delay00()
            verif4 = re.compile(delay_regex, flags=0).search(subdelay)
        sync = "--sync 0:{0} ".format(subdelay)
    return (sync, sync2)


# Subtitles Format Values
def subtitles_format(subtype):
    ext2 = ""
    ext_resp = ["1", "2", "3", "4"]
    ext_values = ["", ".pgs", ".vobsub", ".ass", ".srt"]

    # When MULTi Subs
    if (subtype == "3"):
        ext = ask_subs_format01()
        while ext not in ext_resp:
            bad_subtitles_format()
            ext = ask_subs_format01()
        ext = ext_values[int(ext)]

        ext2 = ask_subs_format02()
        while ext2 not in ext_resp:
            bad_subtitles_format()
            ext2 = ask_subs_format02()
        ext2 = ext_values[int(ext2)]

    # When single subs
    else:
        ext = ask_subs_format00()
        while ext not in ext_resp:
            bad_subtitles_format()
            ext = ask_subs_format00()
        ext = ext_values[int(ext)]
    return (ext, ext2)


# Subforced Config
def subforced_config_INT(audiotype, subtype):

    # When MULTi AUDIO
    if (audiotype == "4"):
        if (subtype == "1"):        # ST FRENCH
            forced = "--forced-track 3:no "
            stforced = "n"
        elif (subtype == "2"):      # ST FORCED
            forced = "--forced-track 3:yes "
            stforced = "n"
        else:                       # ST MULTi
            stforced = ask_subforced()
            if (stforced == "y"):
                forced = "--forced-track 4:yes "
            else:
                forced = "--forced-track 4:no "

    # When SINGLE AUDIO
    else:
        if (subtype == "1"):        # ST FRENCH
            forced = "--forced-track 2:no "
            stforced = "n"
        elif (subtype == "2"):      # ST FORCED
            forced = "--forced-track 2:yes "
            stforced = "n"
        else:                       # ST MULTi
            stforced = ask_subforced()
            if (stforced == "y"):
                forced = "--forced-track 3:yes "
            else:
                forced = "--forced-track 3:no "
    return (forced, stforced)


def subforced_config_EXT(subtype):
    if (subtype == "1"):            # ST FRENCH
        forced = "--forced-track '0:no' "
        stforced = "n"
    elif (subtype == "2"):          # ST FORCED
        forced = "--forced-track '0:yes' "
        stforced = "n"
    else:                           # ST MULTi
        stforced = ask_subforced()
        if (stforced == "y"):
            forced = "--forced-track '0:yes' "
        else:
            forced = "--forced-track '0:no' "
    return (forced, stforced)


# NFO Subforced Values
def subforced_nfo(subtype, stforced):
    if (subtype == "3"):         # ST MULTi
        if (stforced == "y"):
            subforced = "YES"
        else:
            subforced = "N/A"
    elif (subtype == "2"):     # ST FORCED
        subforced = "YES"
    else:                     # ST FRENCH
        subforced = "N/A"
    return subforced


# FFMPEG Config
def ffmpeg_multi_subs(idsub, titlesub, idsub2, titlesub2):
    sub_config = " -map 0:{0} -metadata:s:s:0 title='{1}' -metadata:"\
                 "s:s:0 language= -c:s:0 srt -map 0:{2} -metadata:s:"\
                 "s:1 title='{3}' -metadata:s:s:1 language= -c:s:1 s"\
                 "rt".format(idsub, titlesub, idsub2, titlesub2)
    return sub_config


def ffmpeg_solo_subs(idsub, titlesub):
    sub_config = " -map 0:{0} -metadata:s:s:0 title='{1}' -metadata:"\
                 "s:s:0 language= -c:s:0 srt".format(idsub, titlesub)
    return sub_config
