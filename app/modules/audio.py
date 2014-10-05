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
from django.utils.encoding import (smart_str, smart_unicode)
from app.main.param import regex
from app.main.inputs import *
from app.main.events import *

(hb_regex, crf_regex, delay_regex, fp_regex, aq_regex, url_regex) = regex()


# Select Audio Tracks ID
def select_audio_ID():
    audionum = ask_audio_track00()
    verif_t1 = re.compile(crf_regex, flags=0).search(audionum)
    while not audionum or len(audionum) > 2\
            or audionum.isdigit() is False or verif_t1 is not None:
        bad_audio_ID()
        audionum = ask_audio_track00()
        verif_t1 = re.compile(crf_regex, flags=0).search(audionum)
    return audionum


def select_audio_ID_01():
    audionum = ask_audio_track01()
    verif_t2 = re.compile(crf_regex, flags=0).search(audionum)
    while not audionum or len(audionum) > 2\
            or audionum.isdigit() is False or verif_t2 is not None:
        bad_audio_ID()
        audionum = ask_audio_track01()
        verif_t2 = re.compile(crf_regex, flags=0).search(audionum)
    return audionum


def select_audio_ID_02():
    audionum2 = ask_audio_track02()
    verif_t3 = re.compile(crf_regex, flags=0).search(audionum2)
    while not audionum2 or len(audionum2) > 2\
            or audionum2.isdigit() is False or verif_t3 is not None:
        bad_audio_ID()
        audionum2 = ask_audio_track02()
        verif_t3 = re.compile(crf_regex, flags=0).search(audionum2)
    return audionum2


# Audio Tracks Titles
def audio_track_title(deleted):
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
    return audiolang


def audio_track_title_01(deleted):
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
    return audiolang


def audio_track_title_02(deleted):
    audiolang2 = ask_audiolang02()
    while not audiolang2:
        bad_audio_title()
        audiolang2 = ask_audiolang02()

    # Clean Audio Track 02 Title
    for d_char in deleted:
        if d_char in audiolang2.strip():
            audiolang2 = smart_str(audiolang2).strip()\
                                              .replace(' ', '.')\
                                              .replace(d_char, '')
        else:
            audiolang2 = smart_str(audiolang2).strip().replace(' ', '.')
    return audiolang2


# Codec Values
codec_resp = ["1", "2", "3"]


# Audio Tracks Codecs
def audio_track_codec(codec_resp):
    audiocodec = ask_audio_codec00()
    while audiocodec not in codec_resp:
        bad_audio_codec()
        audiocodec = ask_audio_codec00()
    return audiocodec


def audio_track_codec_01(codec_resp):
    audiocodec = ask_audio_codec01()
    while audiocodec not in codec_resp:
        bad_audio_codec()
        audiocodec = ask_audio_codec01()
    return audiocodec


def audio_track_codec_02(codec_resp):
    audiocodec2 = ask_audio_codec02()
    while audiocodec2 not in codec_resp:
        bad_audio_codec()
        audiocodec2 = ask_audio_codec02()
    return audiocodec2


# Audio Tracks bitrate ( min: 96Kbps / max: 3000Kbps )
def audio_track_bitrate():
    abitrate = ask_audio_bitrate00()
    verif_b0 = re.compile(crf_regex, flags=0).search(abitrate)
    while not abitrate or abitrate.isdigit() is False\
            or verif_b0 is not None\
            or int(abitrate) < 96 or int(abitrate) > 3000:
        bad_audio_bitrate()
        abitrate = ask_audio_bitrate00()
        verif_b0 = re.compile(crf_regex, flags=0).search(abitrate)
    return abitrate


def audio_track_bitrate_01():
    abitrate = ask_audio_bitrate01()
    verif_b1 = re.compile(crf_regex, flags=0).search(abitrate)
    while not abitrate or abitrate.isdigit() is False\
            or verif_b1 is not None\
            or int(abitrate) < 96 or int(abitrate) > 3000:
        bad_audio_bitrate()
        abitrate = ask_audio_bitrate02()
        verif_b1 = re.compile(crf_regex, flags=0).search(abitrate)
    return abitrate


def audio_track_bitrate_02():
    abitrate2 = ask_audio_bitrate02()
    verif_b2 = re.compile(crf_regex, flags=0).search(abitrate2)
    while not abitrate2 or abitrate2.isdigit() is False\
            or verif_b2 is not None\
            or int(abitrate2) < 96 or int(abitrate2) > 3000:
        bad_audio_bitrate()
        abitrate2 = ask_audio_bitrate02()
        verif_b2 = re.compile(crf_regex, flags=0).search(abitrate2)
    return abitrate2


# Audio Track Channels ( max 11 [9.2] )
def audio_track_channels():
    surround = ask_audio_channels00()
    verif_s0 = re.compile(crf_regex, flags=0).search(surround)
    while not surround or surround.isdigit() is False\
            or verif_s0 is not None or int(surround) > 11:
        bad_audio_surround()
        surround = ask_audio_channels00()
        verif_s0 = re.compile(crf_regex, flags=0).search(surround)
    return surround


def audio_track_channels_01():
    surround = ask_audio_channels01()
    verif_s1 = re.compile(crf_regex, flags=0).search(surround)
    while not surround or surround.isdigit() is False\
            or verif_s1 is not None or int(surround) > 11:
        bad_audio_surround()
        surround = ask_audio_channels01()
        verif_s1 = re.compile(crf_regex, flags=0).search(surround)
    return surround


def audio_track_channels_02():
    surround2 = ask_audio_channels02()
    verif_s2 = re.compile(crf_regex, flags=0).search(surround2)
    while not surround2 or surround2.isdigit() is False\
            or verif_s2 is not None or int(surround2) > 11:
        bad_audio_surround()
        surround2 = ask_audio_channels02()
        verif_s2 = re.compile(crf_regex, flags=0).search(surround2)
    return surround2

# Sampling Rate Values
sampling_val = ['16', '32', '44', '48', '96', '192']


# Audio Tracks Sampling Rate
def audio_track_sampling_rate(sampling_val):
    audiox2 = ""
    ar = ask_audio_sampling_rate00()
    while ar not in sampling_val or not ar:
        bad_audio_sampling_rate()
        ar = ask_audio_sampling_rate00()
    audiox = " -ar:a:0 {0}k".format(ar)
    return (audiox, audiox2)


def audio_track_sampling_rate_01(sampling_val):
    ar1 = ask_audio_sampling_rate01()
    while ar1 not in sampling_val or not ar1:
        bad_audio_sampling_rate()
        ar1 = ask_audio_sampling_rate01()
    audiox = " -ar:a:0 {0}k".format(ar1)
    return audiox


def audio_track_sampling_rate_02(sampling_val):
    ar2 = ask_audio_sampling_rate02()
    while ar2 not in sampling_val or not ar2:
        bad_audio_sampling_rate()
        ar2 = ask_audio_sampling_rate02()
    audiox2 = " -ar:a:1 {0}k".format(ar2)
    return audiox2


# Default Sampling rate values
def default_sampling_rate():
    audiox = " -ar:a:0 48k"
    audiox2 = " -ar:a:1 48k"
    return (audiox, audiox2)


# Config Audio Tracks Codecs
def audio_codec_MP3_01(audiox):
    config = "-c:a:0 mp3 -b:a:0 128k -ac:a:0 2{0}".format(audiox)
    return config


def audio_codec_AC3_01(abitrate, surround, audiox):
    config = "-c:a:0 ac3 -b:a:0 {0}k -ac:a:0 {1}{2}"\
             .format(abitrate, surround, audiox)
    return config


def audio_codec_DTS_01():
    config = "-c:a:0 copy"
    return config


def audio_codec_MP3_02(audiox2):
    config2 = "-c:a:1 mp3 -b:a:1 128k -ac:a:1 2{0}".format(audiox2)
    return config2


def audio_codec_AC3_02(abitrate, surround, audiox):
    config2 = "-c:a:1 ac3 -b:a:1 {0}k -ac:a:1 {1}{2}"\
              .format(abitrate2, surround2, audiox2)
    return config2


def audio_codec_DTS_02():
    config = "-c:a:1 copy"
    return config2


# Language Values
def audio_language_values(audiotype, audiolang):
    lang_val = ["", "FRENCH", "VOSTFR", "VOSTFR", "MULTi"]
    audiolang_val = ["", "FRENCH", "ENGLiSH"]
    atype_resp = ["1", "2", "3", "4"]
    altype_resp = ["1", "2"]
    if (audiotype in atype_resp):
        lang = lang_val[int(audiotype)]
        if (audiotype in altype_resp):
            audiolang = audiolang_val[int(audiotype)]
    else:
        lang = "NOAUDIO"
        audiolang = "NOAUDIO"
    return (lang, audiolang)


# Audio Tracks FFMPEG Config
def audio_multi_config(audionum, audiolang, config,
                       audionum2, audiolang2, config2):
    audio_config = " -map 0:{0} -metadata:s:a:0 title='{1}' -metadata:s:"\
                   "a:0 language= {2} -map 0:{3} -metadata:s:a:1 title='"\
                   "{4}' -metadata:s:a:1 language= {5}"\
                   .format(audionum, audiolang, config,
                           audionum2, audiolang2, config2)
    return audio_config


def audio_solo_config(audionum, audiolang, config):
    audio_config = " -map 0:{0} -metadata:s:a:0 title='{1}' -metadata:s:"\
                   "a:0 language= {2}".format(audionum, audiolang, config)
    return audio_config
