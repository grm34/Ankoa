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
from app.skin.style import (color, help)

(BLUE, RED, YELLOW, GREEN, BOLD, END) = color()


# SOURCE INPUTS
def ask_source():
    prefix = raw_input("{0}RELEASE SOURCE > \n{1}".format(GREEN, END))
    return prefix


def ask_title():
    title = raw_input("{0}RELEASE TITLE {1}(ex: Hudson.Hawk){0} : {2}"
                      .format(GREEN, YELLOW, END))
    return title


def ask_year():
    year = raw_input("{0}RELEASE PRODUCTION YEAR : {1}".format(GREEN, END))
    return year


def ask_tag():
    special = raw_input("{0}SPECIAL TAG {1}(ex: EXTENDED.CUT){0} : {2}"
                        .format(GREEN, YELLOW, END))
    return special


# SCAN INPUTS
def ask_scan_type():
    type = raw_input("{0}SCAN INFOS SOURCE > \n{1}HANDBRAKE {0}[1]{1} - "
                     "FFMPEG {0}[2]{1} - MEDIAINFO {0}[3] : {2}"
                     .format(GREEN, YELLOW, END))
    return type


def ask_scan_again():
    scan_again = raw_input("{0}SCAN AGAIN {1}(y/n){0} : {2}"
                           .format(GREEN, YELLOW, END))
    return scan_again


def ask_ffmpeg_scan():
    scan2 = raw_input("{0}FFMPEG SCAN TRACKS {1}(y/n){0} : {2}"
                      .format(GREEN, YELLOW, END))
    return scan2


def ask_scan_autocrop():
    scan_crop = raw_input("{0}SCAN AUTOCROP SOURCE {1}(y/n){0} : {2}"
                          .format(GREEN, YELLOW, END))
    return scan_crop


# VIDEO INPUTS
def ask_2pass_crf():
    encode_type = raw_input("{0}ENCODING MODE > \n{1}MUX {0}[1]{1} - DUALPASS"
                            " {0}[2]{1} - CRF {0}[3] : {2}"
                            .format(GREEN, YELLOW, END))
    return encode_type


def ask_crf_level():
    crf = raw_input("{0}CRF LEVEL {1}(0 to 51){0} : {2}"
                    .format(GREEN, YELLOW, END))
    return crf


def ask_bitrate_calculator():
    calculator = raw_input("{0}BITRATE CALCULATOR {1}(y/n){0} : {2}"
                           .format(GREEN, YELLOW, END))
    return calculator


def ask_try_again():
    next = raw_input("{0}TRY AGAIN {1}(y/n){0} : {2}"
                     .format(GREEN, YELLOW, END))
    return next


def ask_video_bitrate():
    bit = raw_input("{0}VIDEO BITRATE Kbps {1}(min 750){0} : {2}"
                    .format(GREEN, YELLOW, END))
    return bit


def ask_rls_format():
    format = raw_input("{0}RELEASE FORMAT > \n{1}HDTV {0}[1]{1} - PDTV {0}[2]"
                       "{1} - BDRip {0}[3]\n{1}DVDRip {0}[4]{1} - BRRip {0}[5"
                       "]{1} - BluRay {0}[6] : {2}".format(GREEN, YELLOW, END))
    return format


def ask_HR_PDTV():
    hr = raw_input("{0}PDTV HIGH RESOLUTION {1}(y/n){0} : {2}"
                   .format(GREEN, YELLOW, END))
    return hr


def ask_HD_size():
    hd_hdtv = raw_input("{0}RESOLUTION FORMAT : {1}720p {0}[1]{1} - {1}1080p"
                        " {0}[2]{0} : {2}".format(GREEN, YELLOW, END))
    return hd_hdtv


def ask_HD_HDTV():
    hd_size = raw_input("{0}HDTV HIGHT RESOLUTION {1}(y/n){0} : {2}"
                        .format(GREEN, YELLOW, END))
    return hd_size


def ask_video_codec():
    codec_type = raw_input("{0}VIDEO CODEC : {1}x264 {0}[1]{1} - x265 {0}"
                           "[2] : {2}".format(GREEN, YELLOW, END))
    return codec_type


def ask_rls_container():
    rlstype = raw_input("{0}RELEASE CONTAINER > \n{1}MPEG4 {0}[1]{1} - "
                        "MATROSKA {0}[2] : {2}".format(GREEN, YELLOW, END))
    return rlstype


def ask_ffmped_ID():
    idvideo = raw_input("{0}VIDEO TRACK FFMPEG ID {1}(ex: 0){0} : {2}"
                        .format(GREEN, YELLOW, END))
    return idvideo


def ask_modif_fps():
    modif_fps = raw_input("{0}CHANGE VIDEO FRAMERATE {1}(y/n){0} : {2}"
                          .format(GREEN, YELLOW, END))
    return modif_fps


def ask_video_fps():
    set_fps = raw_input("{0}VIDEO FRAMERATE {1}(ex: 23.98){0} : {2}"
                        .format(GREEN, YELLOW, END))
    return set_fps


def ask_deinterlace():
    deinterlace = raw_input("{0}DEINTERLACE VIDEO {1}(y/n){0} : {2}"
                            .format(GREEN, YELLOW, END))
    return deinterlace


# AUDIO INPUTS
def ask_audio_type():
    audiotype = raw_input("{0}RELEASE AUDIO TYPE > \n{1}FRENCH {0}[1]{1} - EN"
                          "GLiSH {0}[2]\n{1}OTHER {0}[3]{1} - MULTi {0}[4]"
                          "{1} - N/A {0}[5] : {2}"
                          .format(GREEN, YELLOW, END))
    return audiotype


def ask_audio_track00():
    audionum = raw_input("{0}AUDIO TRACK FFMPEG ID {1}(ex: 1){0} : {2}"
                         .format(GREEN, YELLOW, END))
    return audionum


def ask_audio_track01():
    audionum = raw_input("{0}AUDIO TRACK 01 FFMPEG ID {1}(ex: 1){0} :"
                         " {2}".format(GREEN, YELLOW, END))
    return audionum


def ask_audio_track02():
    audionum2 = raw_input("{0}AUDIO TRACK 02 FFMPEG ID {1}(ex: 0){0} :"
                          " {2}".format(GREEN, YELLOW, END))
    return audionum2


def ask_audiolang00():
    audiolang = raw_input("{0}AUDIO TRACK TITLE {1}(ex: Espagnol){0} "
                          ": {2}".format(GREEN, YELLOW, END))
    return audiolang


def ask_audiolang01():
    audiolang = raw_input("{0}AUDIO TRACK 01 TITLE {1}(ex: English){0} :"
                          " {2}".format(GREEN, YELLOW, END))
    return audiolang


def ask_audiolang02():
    audiolang2 = raw_input("{0}AUDIO TRACK 02 TITLE {1}(ex: English){0} :"
                           " {2}".format(GREEN, YELLOW, END))
    return audiolang2


def ask_audio_codec00():
    audiocodec = raw_input("{0}AUDIO TRACK CODEC > \n{1}MP3 {0}[1]{1} - A"
                           "C3 {0}[2]{1} - DTS/COPY {0}[3] : {2}"
                           .format(GREEN, YELLOW, END))
    return audiocodec


def ask_audio_codec01():
    audiocodec = raw_input("{0}AUDIO TRACK 01 CODEC > \n{1}MP3 {0}[1]{1}"
                           " - AC3 {0}[2]{1} - DTS/COPY {0}[3] : {2}"
                           .format(GREEN, YELLOW, END))
    return audiocodec


def ask_audio_codec02():
    audiocodec2 = raw_input("{0}AUDIO TRACK 02 CODEC > \n{1}MP3 {0}[1]{1}"
                            " - AC3 {0}[2]{1} - DTS/COPY {0}[3] : {2}"
                            .format(GREEN, YELLOW, END))
    return audiocodec2


def ask_audio_bitrate00():
    abitrate = raw_input("{0}AUDIO TRACK BITRATE Kbps {1}(ex: 448){0}"
                         " : {2}".format(GREEN, YELLOW, END))
    return abitrate


def ask_audio_bitrate01():
    abitrate = raw_input("{0}AUDIO TRACK 01 BITRATE Kbps {1}(ex: 448)"
                         "{0} : {2}".format(GREEN, YELLOW, END))
    return abitrate


def ask_audio_bitrate02():
    abitrate2 = raw_input("{0}AUDIO TRACK 02 BITRATE Kbps {1}(ex: 448"
                          "){0} : {2}".format(GREEN, YELLOW, END))
    return abitrate2


def ask_audio_channels00():
    surround = raw_input("{0}AUDIO TRACK CHANNELS {1}(ex: 2){0} : {2}"
                         .format(GREEN, YELLOW, END))
    return surround


def ask_audio_channels01():
    surround = raw_input("{0}AUDIO TRACK 01 CHANNELS {1}(ex: 2){0} :"
                         " {2}".format(GREEN, YELLOW, END))
    return surround


def ask_audio_channels02():
    surround2 = raw_input("{0}AUDIO TRACK 02 CHANNELS {1}(ex: 2){0} :"
                          " {2}".format(GREEN, YELLOW, END))
    return surround2


def ask_modif_sampling_rate():
    audiox = raw_input("{0}CHANGE SAMPLING RATE {1}(y/n){0} : {2}"
                       .format(GREEN, YELLOW, END))
    return audiox


def ask_audio_sampling_rate00():
    ar = raw_input("{0}AUDIO TRACK SAMPLING RATE {1}(ex: 48){0} :"
                   " {2}".format(GREEN, YELLOW, END))
    return ar


def ask_audio_sampling_rate01():
    ar1 = raw_input("{0}AUDIO TRACK 01 SAMPLING RATE {1}(ex: 48)"
                    "{0} : {2}".format(GREEN, YELLOW, END))
    return ar1


def ask_audio_sampling_rate02():
    ar2 = raw_input("{0}AUDIO TRACK 02 SAMPLING RATE {1}(ex: 48)"
                    "{0} : {2}".format(GREEN, YELLOW, END))
    return ar2


# SUBTITLES INPUTS
def ask_title_subs01():
    titlesub = raw_input("{0}SUBTITLES TRACK 01 TITLE {1}(ex: Full.Fr"
                         "ench){0} : {2}".format(GREEN, YELLOW, END))
    return titlesub


def ask_title_subs02():
    titlesub2 = raw_input("{0}SUBTITLES TRACK 02 TITLE {1}(ex: French"
                          ".Forced){0} : {2}".format(GREEN, YELLOW, END))
    return titlesub2


def ask_subs_ISO_ID00():
    idsub = raw_input("{0}SUBTITLES TRACK HANDBRAKE ID {1}(ex: 1){0} : "
                      "{2}".format(GREEN, YELLOW, END))
    return idsub


def ask_subs_ISO_ID01():
    idsub = raw_input("{0}SUBTITLES TRACK 01 HANDBRAKE ID {1}(ex: 1){0}"
                      " : {2}".format(GREEN, YELLOW, END))
    return idsub


def ask_subs_ISO_ID02():
    idsub2 = raw_input("{0}SUBTITLES TRACK 02 HANDBRAKE ID {1}(ex: 2)"
                       "{0} : {2}".format(GREEN, YELLOW, END))
    return idsub2


def ask_subs_FFMPEG_ID00():
    idsub = raw_input("{0}SUBTITLES TRACK FFMPEG ID {1}(ex: 1){0}"
                      " : {2}".format(GREEN, YELLOW, END))
    return idsub


def ask_subs_FFMPEG_ID01():
    idsub = raw_input("{0}SUBTITLES TRACK 01 FFMPEG ID {1}(ex: 1)"
                      "{0} : {2}".format(GREEN, YELLOW, END))
    return idsub


def ask_subs_FFMPEG_ID02():
    idsub2 = raw_input("{0}SUBTITLES TRACK 02 FFMPEG ID {1}(ex: 2"
                       "){0} : {2}".format(GREEN, YELLOW, END))
    return idsub2


def ask_subs_source00():
    ub = raw_input("{0}SUBTITLES TRACK SOURCE > \n{1}"
                   .format(GREEN, END))
    return ub


def ask_subs_source01():
    ub = raw_input("{0}SUBTITLES TRACK 01 SOURCE > \n{1}"
                   .format(GREEN, END))
    return ub


def ask_subs_source02():
    ub2 = raw_input("{0}SUBTITLES TRACK 02 SOURCE > \n{1}"
                    .format(GREEN, END))
    return ub2


def ask_subcharset00():
    idcharset = raw_input("{0}SUBTITLES CHARSET ANSI {1}(y/n){0} : "
                          "{2}".format(GREEN, YELLOW, END))
    return idcharset


def ask_subcharset01():
    idcharset = raw_input("{0}SUBTITLES 01 CHARSET ANSI {1}(y/n){0} :"
                          " {2}".format(GREEN, YELLOW, END))
    return idcharset


def ask_subcharset02():
    idcharset2 = raw_input("{0}SUBTITLES 02 CHARSET ANSI {1}(y/n){0} "
                           ": {2}".format(GREEN, YELLOW, END))
    return idcharset2


def ask_use_subdelay():
    subsync = raw_input("{0}SUBTITLES DELAY {1}(y/n){0} : {2}"
                        .format(GREEN, YELLOW, END))
    return subsync


def ask_subs_delay00():
    subdelay = raw_input("{0}SUBTITLES DELAY {1}(ex: -200){0} : "
                         "{2}".format(GREEN, YELLOW, END))
    return subdelay


def ask_subs_delay01():
    subdelay1 = raw_input("{0}SUBTITLES 01 DELAY {1}(ex: -200){0}"
                          " : {2}".format(GREEN, YELLOW, END))
    return subdelay1


def ask_subs_delay02():
    subdelay2 = raw_input("{1}SUBTITLES 02 DELAY {1}(ex: -200){1}"
                          " : {1}".format(GREEN, YELLOW, END))
    return subdelay2


def ask_subs_format00():
    ext = raw_input("{0}SUBTITLES FORMAT > \n{1}PGS {0}[1]{1} - VOBS"
                    "UB {0}[2]{1} - ASS {0}[3]{1} - SRT {0}[4] : {2}"
                    .format(GREEN, YELLOW, END))
    return ext


def ask_subs_format01():
    ext = raw_input("{0}SUBTITLES 01 FORMAT > \n{1}PGS {0}[1]{1} - "
                    "VOBSUB {0}[2]{1} - ASS {0}[3]{1} - SRT {0}[4] "
                    ": {2}".format(GREEN, YELLOW, END))
    return ext


def ask_subs_format02():
    ext2 = raw_input("{0}SUBTITLES 02 FORMAT > \n{1}PGS {0}[1]{1} -"
                     " VOBSUB {0}[2]{1} - ASS {0}[3]{1} - SRT {0}[4]"
                     " : {2}".format(GREEN, YELLOW, END))
    return ext2


def ask_subs_from():
    subsource = raw_input("{0}SUBTITLES FROM > \n{1}SOURCE {0}[1]{1} - N/A "
                          "{0}[2]{1} - FILE {0}[3]\n{1}ISO/IMG {0}[4]{1} - M"
                          "KV {0}[5]{1} - M2TS {0}[6] : {2}"
                          .format(GREEN, YELLOW, END))
    return subsource


def ask_subs_type():
    subtype = raw_input("{0}SUBTITLES TYPE > \n{1}FR {0}[1]{1} - FORCED "
                        "{0}[2]{1} - MULTi {0}[3] : {2}"
                        .format(GREEN, YELLOW, END))
    return subtype


def ask_subforced():
    stforced = raw_input("{0}USE FORCED TRACK {1}(y/n){0} : "
                         "{2}".format(GREEN, YELLOW, END))
    return stforced


# ASPECT RATIO INPUTS
def ask_reso_width():
    W = raw_input("{0}RESOLUTION WIDTH : {1}".format(GREEN, END))
    return W


def ask_reso_height():
    H = raw_input("{0}RESOLUTION HEIGHT : {1}".format(GREEN, END))
    return H


def ask_use_reso_sar():
    ask_sar = raw_input("{0}USE SAMPLE ASPECT RATIO {1}(y/n){0} : {2}"
                        .format(GREEN, YELLOW, END))
    return ask_sar


def ask_reso_sar():
    sar = raw_input("{0}SOURCE ASPECT RATIO > \n{1}PAL 16:9 {0}[1]{1}"
                    " - PAL 4:3 {0}[2]\n{1}NTSC 16:9 {0}[3]{1} - NTSC"
                    " 4:3 {0}[4] : {2}".format(GREEN, YELLOW, END))
    return sar


def ask_custom_reso():
    perso = raw_input("{0}CUSTOM RESOLUTION {1}(y/n){0} : {2}"
                      .format(GREEN, YELLOW, END))
    return perso


def ask_aspect_ratio():
    ratio = raw_input("{0}RELEASE ASPECT RATIO > \n{1}1.33 {0}[1]{1} - 1.66 "
                      "{0}[2]{1} - 1.78 {0}[3]{1}\n1.85 {0}[4]{1} - 2.35 {0}"
                      "[5]{1} - 2.40 {0}[6] : {2}"
                      .format(GREEN, YELLOW, END))
    return ratio


def ask_screenshots():
    ask_screen = raw_input("{0}SCREENSHOT VERIFICATION {1}(y/n){0} : {2}"
                           .format(GREEN, YELLOW, END))
    return ask_screen


def ask_manual_crop():
    man_crop = raw_input("{0}MANUAL SOURCE CROP {1}(y/n){0} : {2}"
                         .format(GREEN, YELLOW, END))
    return man_crop


def ask_W_crop():
    w_crop = raw_input("{0}SOURCE CROP WIDTH {1}(ex: 1920){0} : {2}"
                       .format(GREEN, YELLOW, END))
    return w_crop


def ask_H_crop():
    h_crop = raw_input("{0}SOURCE CROP HEIGHT {1}(ex: 800){0} : {2}"
                       .format(GREEN, YELLOW, END))
    return h_crop


def ask_LR_crop():
    x_crop = raw_input("{0}PIXELS CROP LEFT/RIGHT {1}(ex: 0){0} : {2}"
                       .format(GREEN, YELLOW, END))
    return x_crop


def ask_TB_crop():
    y_crop = raw_input("{0}PIXELS CROP TOP/BOTTOM {1}(ex: 140){0} : {2}"
                       .format(GREEN, YELLOW, END))
    return y_crop


# x264 INPUTS
def ask_format_profile():
    level = raw_input("{0}VIDEO FORMAT PROFILE {1}(ex: 3.1){0} : {2}"
                      .format(GREEN, YELLOW, END))
    return level


def ask_x264_preset():
    preset = raw_input("{0}CUSTOM PRESET X264/X265 > \n{1}FAST {0}[1]{1} - SL"
                       "OW {0}[2]{1} - SLOWER {0}[3]\n{1}VERYSLOW {0}[4]{1} -"
                       " PLACEBO {0}[5]{1} - NONE {0}[6] : {2}"
                       .format(GREEN, YELLOW, END))
    return preset


def ask_x264_tune():
    tuned = raw_input("{0}CUSTOM X264/X265 TUNE > \n{1}FILM {0}[1]{1} - ANIMA"
                      "TION {0}[2]{1} - GRAIN {0}[3]\n{1}STILLIMAGE {0}[4]{1}"
                      " - PSNR {0}[5]{1} - SSIM {0}[6]\n{1}FASTDECODE {0}[7]"
                      "{1} - {0}[8]{1} - NONE {0}[9] : {2}"
                      .format(GREEN, YELLOW, END))
    return tuned


# ADVANCED MODE INPUTS
def ask_advanced_mode():
    x264 = raw_input("{0}X264/X265 ADVANCED MODE {1}(y/n){0} : {2}"
                     .format(GREEN, YELLOW, END))
    return x264


def ask_threads():
    threads = raw_input("{0}PROCESSOR THREADS {1}(ex: 8){0} : {2}"
                        .format(GREEN, YELLOW, END))
    return threads


def ask_threads_type():
    thread_type = raw_input("{0}PROCESSOR THREAD TYPE > \n{1}SLICE {0}[1]{1}"
                            "- FRAME {0}[2]{1} - DEFAULT {0}[3] : {2}"
                            .format(GREEN, YELLOW, END))
    return thread_type


def ask_fastfirstpass():
    fastfirstpass = raw_input("{0}FAST FIRST PASS {1}(y/n){0} : {2}"
                              .format(GREEN, YELLOW, END))
    return fastfirstpass


def ask_refs():
    refs = raw_input("{0}REFERENCE FRAMES {1}(max: 16){0} : {2}"
                     .format(GREEN, YELLOW, END))
    return refs


def ask_mixed_refs():
    mixed = raw_input("{0}MIXED REFERENCES {1}(y/n){0} : {2}"
                      .format(GREEN, YELLOW, END))
    return mixed


def ask_max_bframes():
    bf = raw_input("{0}MAXIMUM B-FRAMES {1}(max: 16){0} : {2}"
                   .format(GREEN, YELLOW, END))
    return bf


def ask_pyramidal():
    pyramid = raw_input("{0}PYRAMIDAL METHOD > \n{1}NONE {0}[1]{1} - NOR"
                        "MAL {0}[2]{1} - STRICT {0}[3] : {2}"
                        .format(GREEN, YELLOW, END))
    return pyramid


def ask_weight_bframes():
    weightb = raw_input("{0}WEIGHTED B-FRAMES {1}(y/n){0} : {2}"
                        .format(GREEN, YELLOW, END))
    return weightb


def ask_weight_pframes():
    weightp = raw_input("{0}WEIGHTED P-FRAMES > \n{1}NONE {0}[1]{1} - SI"
                        "MPLE {0}[2]{1} - SMART {0}[3] : {2}"
                        .format(GREEN, YELLOW, END))
    return weightp


def ask_8x8_transform():
    dct = raw_input("{0}ENABLE 8x8 TRANSFORM {1}(y/n){0} : {2}"
                    .format(GREEN, YELLOW, END))
    return dct


def ask_cabac():
    cabac = raw_input("{0}ENABLE CABAC {1}(y/n){0} : {2}"
                      .format(GREEN, YELLOW, END))
    return cabac


def ask_bstrategy():
    b_strat = raw_input("{0}ADAPTIVE B-FRAMES > \n{1}VERYFAST {0}[1]"
                        "{1} - FAST {0}[2]{1} - SLOWER {0}[3] : {2}"
                        .format(GREEN, YELLOW, END))
    return b_strat


def ask_direct_mode():
    direct = raw_input("{0}ADAPTIVE DIRECT MODE > \n{1}NONE {0}[1]{1} - "
                       "SPATIAL {0}[2]\n{1}TEMPORAL {0}[3]{1} - AUTO {0}"
                       "[4] : {2}".format(GREEN, YELLOW, END))
    return direct


def ask_me_method():
    me_method = raw_input("{0}MOTION ESTIMATION METHOD > \n{1}DIA {0}[1]"
                          "{1} - HEX {0}[2]\n{1}UMH {0}[3]{1} - ESA {0}["
                          "4]{1} - TESA {0}[5] : {2}"
                          .format(GREEN, YELLOW, END))
    return me_method


def ask_subpixel():
    subq = raw_input("{0}SUBPIXEL MOTION ESTIMATION {1}(max: 11){0} : {2}"
                     .format(GREEN, YELLOW, END))
    return subq


def ask_motion_range():
    me_range = raw_input("{0}MOTION ESTIMATION RANGE {1}(max: 64){0} : "
                         "{2}".format(GREEN, YELLOW, END))
    return me_range


def ask_partitions():
    parts = raw_input("{0}PARTITIONS TYPE > \n{1}ALL {0}[1]{1} - p8x8 "
                      "{0}[2]{1} - p4x4 {0}[3]\n{1}NONE {0}[4]{1} - b8x8"
                      "{0}[5]{1} - i8x8 {0}[6]{1} - i4x4 {0}[7] : {2}"
                      .format(GREEN, YELLOW, END))
    return parts


def ask_trellis():
    trellis = raw_input("{0}TRELLIS MODE > \n{1}OFF {0}[1]{1} - DEFAULT "
                        "{0}[2]{1} - ALL {0}[3] : {2}"
                        .format(GREEN, YELLOW, END))
    return trellis


def ask_aq_mode():
    aq_mod = raw_input("{0}QUANTIZATION MODE > \n{1}NONE {0}[1]{1} - VARIANCE "
                       "{0}[2]{1}\nAUTO-VARIANCE (new) {0}[3] : {2}"
                       .format(GREEN, YELLOW, END))
    return aq_mod


def ask_aq_strength():
    aq = raw_input("{0}QUANTIZATION STRENGTH {1}(ex: 1.5){0} : {2}"
                   .format(GREEN, YELLOW, END))
    return aq


def ask_psy_optimization():
    psy = raw_input("{0}PSYCHOVISUAL OPTIMIZATION {1}(y/n){0} : {2}"
                    .format(GREEN, YELLOW, END))
    return psy


def ask_rate_distortion():
    psy1 = raw_input("{0}RATE DISTORTION [psy-rd] {1}(ex: 1.00){0} : {2}"
                     .format(GREEN, YELLOW, END))
    return psy1


def ask_psy_rd():
    psy2 = raw_input("{0}PSYCHOVISUAL TRELLIS [psy-rd] {1}(ex: 0.15)"
                     "{0} : {2}".format(GREEN, YELLOW, END))
    return psy2


def ask_deblock():
    deblock = raw_input("{0}DEBLOCKING {1}(ex: -1:-1){0} : {2}"
                        .format(GREEN, YELLOW, END))
    return deblock


def ask_lookahead():
    lookahead = raw_input("{0}FRAMES LOOKAHEAD {1}(ex: 60){0} : {2}"
                          .format(GREEN, YELLOW, END))
    return lookahead


def ask_bluray_compatibility():
    bluray = raw_input("{0}BLURAY COMPATIBILITY {1}(y/n){0} : {2}"
                       .format(GREEN, YELLOW, END))
    return bluray


def ask_fast_skip():
    fastpskip = raw_input("{0}FAST SKIP on P-FRAMES {1}(y/n){0} : {2}"
                          .format(GREEN, YELLOW, END))
    return fastpskip


def ask_keyframe_interval():
    g = raw_input("{0}KEYFRAME INTERVAL {1}(ex: 250){0} : {2}"
                  .format(GREEN, YELLOW, END))
    return g


def ask_key_min_interval():
    keyint_min = raw_input("{0}MINIMAL KEY INTERVAL {1}(ex: 25){0} : {2}"
                           .format(GREEN, YELLOW, END))
    return keyint_min


def ask_scenecut():
    scenecut = raw_input("{0}SCENECUT DETECTION {1}(ex: 40){0} : {2}"
                         .format(GREEN, YELLOW, END))
    return scenecut


def ask_chroma_motion():
    cmp = raw_input("{0}CHROMA MOTION ESTIMATION {1}(y/n){0} : {2}"
                    .format(GREEN, YELLOW, END))
    return cmp


def ask_rls_source():
    nfosource = raw_input("{0}RELEASE SOURCE {1}(ex: 1080p.HDZ){0} : {2}"
                          .format(GREEN, YELLOW, END))
    return nfosource


def ask_rls_imdb():
    nfoimdb = raw_input("{0}RELEASE IMDB ID {1}(ex: 6686697){0} : {2}"
                        .format(GREEN, YELLOW, END))
    return nfoimdb


# BIRATE CALCULATOR INPUTS
def ask_HH():
    HH = raw_input("{0}CALCULATOR HOURS : {1}".format(GREEN, END))
    return HH


def ask_MM():
    MM = raw_input("{0}CALCULATOR MINUTES : {1}".format(GREEN, END))
    return MM


def ask_SS():
    SS = raw_input("{0}CALCULATOR SECONDS : {1}".format(GREEN, END))
    return SS


def ask_desired_audio_bitrate():
    audiobit = raw_input("{0}CALCULATOR AUDIO BITRATE : {1}"
                         .format(GREEN, END))
    return audiobit


def ask_desired_size():
    rls_size = raw_input("{0}CALCULATOR SIZE > \n{1}350Mo {0}[1]{1} - 550Mo "
                         "{0}[2]{1} - 700Mo {0}[3]{1} - 1.37Go {0}[4]{1}\n"
                         "2.05Go {0}[5]{1} - 2.74Go {0}[6]{1} - 4.37Go {0}[7]"
                         "{1} - 6.56Go{0} {0}[8] : {2}"
                         .format(GREEN, YELLOW, END))
    return rls_size


# SETUP INPUTS
def ask_source_path():
    source = raw_input("{0}ENTER SOURCE PATH {1}(ex: /home/user/torrent"
                       "s/){0} : {2}".format(GREEN, YELLOW, END))
    return source


def ask_dest_path():
    result = raw_input("{0}ENTER DESTINATION PATH {1}(ex: /home/user/en"
                       "codes/){0} : {2}".format(GREEN, YELLOW, END))
    return result


def ask_user_team():
    team = raw_input("{0}ENTER PERSONAL TEAM NAME {1}(ex: THENiGHTMAREiNHD)"
                     "{0} : {2}".format(GREEN, YELLOW, END))
    return team


def ask_tk_announce():
    tk = raw_input("{0}ENTER URL TRACKER ANNOUNCE {1}(ex: http://tk.com"
                   ":80/announce){0} : {2}".format(GREEN, YELLOW, END))
    return tk


def ask_tmdb_key():
    api = raw_input("{0}ENTER TMDB API KEY {1}(from: {3}https://w"
                    "ww.themoviedb.org/documentation/api{1}){0} : {2}"
                    .format(GREEN, YELLOW, END, BLUE))
    return api


# MODE REMUX INPUTS
def ask_mux_audio_type():
    audiotype = raw_input("{0}AUDIO TYPE : {1}FRENCH {0}[1]{1} - EN"
                          "GLiSH {0}[2] - {1}OTHER {0}[3] : {2}"
                          .format(GREEN, YELLOW, END))
    return audiotype


def ask_remux_start():
    ready = raw_input("{0}READY ? {1}(y/n) {4}||{3} [{2} ENTER to RUN "
                      "{3}]{0} : {4}".format(GREEN, YELLOW, BLUE, RED, END))
    return ready


# CHECK COMMANDS LINES
def check_cmds():
    ask_cmds = raw_input("{0}CHECK COMMANDS LINES {1}(y/n){0} : {2}"
                         .format(GREEN, YELLOW, END))
    return ask_cmds


def ask_print_ffmpeg():
    print_ffmpeg = raw_input("{0}PRINT FFMPEG FINAL COMMAND {1}(y/n){0} : {2}"
                             .format(GREEN, YELLOW, END))
    return print_ffmpeg


def ask_print_mkvmerge():
    print_mkvmerge = raw_input("{0}PRINT MKVMERGE FINAL COMMAND {1}(y/n){0}"
                               " : {2}".format(GREEN, YELLOW, END))
    return print_mkvmerge


def ask_print_tools():
    print_tools = raw_input("{0}PRINT TOOLS FINAL COMMAND {1}(y/n){0} : {2}"
                            .format(GREEN, YELLOW, END))
    return print_tools


# ANKOA QUEUE INPUT
def ask_next_encode():
    again = raw_input("{0}ADD TO QUEUE {1}(y/n) {4}||{3} [{2} ENTER to RUN "
                      "{3}]{0} : {4}".format(GREEN, YELLOW, BLUE, RED, END))
    return again
