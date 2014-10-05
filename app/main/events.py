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

(v, version) = help()
(BLUE, RED, YELLOW, GREEN, BOLD, END) = color()


# HELP USAGE
def ankoa_help():
    usage = "{0}./ankoa.py{1}\n{2}".format(GREEN, END, version)
    return usage


def genprez_help():
    usage = "{0}./genprez.py {4}[{3}LANGUAGE{4}] [{3}FORMAT{4}] [{3}CODECS"\
            "{4}] [{3}SUBS{4}] [{3}SIZE{4}] [{3}ID_IMDB{4}]\n{2}"\
            .format(GREEN, END, version, YELLOW, RED)
    return usage


def imgur_help():
    usage = "{0}./imgur.py {4}[{3}image.png{4}]\n{2}"\
            .format(GREEN, END, version, YELLOW, RED)
    return usage


def make_help():
    usage = "{0}./make.py {4}[{3}video.mkv{4}] [{3}SOURCE{4}] [{3}SUBS"\
            "{4}] [{3}SUBFORCED{4}] [{3}URL{4}]\n{2}"\
            .format(GREEN, END, version, YELLOW, RED)
    return usage


def setup_help():
    usage = "{0}python setup.py {4}[{3}iNSTALL {4}|{3} UPDATE{4}]"\
            "\n{2}".format(GREEN, END, version, YELLOW, RED)
    return usage


def thumbnails_help():
    usage = "{0}./thumbnails.py {4}[{3}video.mkv{4}]{0} 5 2"\
            "{1}\n{2}".format(GREEN, END, version, YELLOW, RED)
    return usage


def nfogen_help():
    usage = "{0}./nfogen.sh {4}[{3}source.mkv{4}] [{3}SOURCE{4}] [{3}SUBS"\
            "{4}] [{3}SUBFORCED{4}] [{3}URL{4}]\n{2}"\
            .format(GREEN, END, version, YELLOW, RED)
    return usage


# SETUP MESSAGES
def setup_success():
    print ("{1} > {0}AnkoA : {2}Installation successful ! {1}[{4}]{3}"
           .format(BLUE, RED, GREEN, END, v))


def setup_error():
    print ("{1} > {0}AnkoA : {2}Setup error, files missing,"
           " fix it with a fresh install !{3}"
           .format(BLUE, RED, GREEN, END))


def update_success():
    print ("{1} > {0}AnkoA : {2}Update successful ! {1}[{4}]{3}"
           .format(BLUE, RED, GREEN, END, v))


def already_up2date():
    print ("{1} > {0}AnkoA : {2}Already up to date ! {1}[{4}]{3}"
           .format(BLUE, RED, YELLOW, END, v))


def update_error():
    print ("{1} > {0}AnkoA : {2}Update error, fix it"
           " with a fresh install !{3}"
           .format(BLUE, GREEN, RED, END))


def setup_bad_source():
    print ("{0} > ERROR : {1}Bad SOURCE PATH, please try"
           " again !{2}".format(RED, BLUE, END))


def setup_bad_dest():
    print ("{0} > ERROR : {1}Bad DESTINATION PATH, please try"
           " again !{2}".format(RED, BLUE, END))


def setup_bad_team():
    print ("{0} > ERROR : {1}Please, specify team name "
           "!{2}".format(RED, BLUE, END))


def setup_bad_tk():
    print ("{0} > ERROR : {1}Please, specify valid tracker url announ"
           "ce !{2}".format(RED, BLUE, END))


def setup_bad_api():
    print ("{0} > ERROR : {1}Please, specify valid TMDB API KEY"
           " !{2}".format(RED, BLUE, END))


# ANKOA SYSTEM ERRORS
def expert_mode_error():
    print ("{1} > ERROR : {2}Bad value, are you sure to be able"
           " to use this mode ?{0}".format(END, RED, BLUE))


def bad_source():
    print ("{1} > ERROR : {2}Bad source selection, please try"
           " again !{0}".format(END, RED, BLUE))


def bad_title():
    print ("{1} > ERROR : {2}Please, specify release title !{0}"
           .format(END, RED, BLUE))


def bad_year():
    print ("{1} > ERROR : {2}Please, specify valid release year !"
           "{0}".format(END, RED, BLUE))


def bad_crf():
    print ("{1} > ERROR : {2}Please, specify valid crf value ! "
           "{0}".format(END, RED, BLUE))


def bad_hd_size():
    print ("{1} > ERROR : {2}Bad format choice, please try again ! "
           "{0}".format(END, RED, BLUE))


def bad_video_bitrate():
    print ("{1} > ERROR : {2}Please, specify valid video "
           "bitrate !{0}".format(END, RED, BLUE))


def bad_video_ID():
    print ("{1} > ERROR : {2}Please, specify valid video ID !{0}"
           .format(END, RED, BLUE))


def bad_fps():
    print ("{1} > ERROR : {2}Please, specify valid video FPS !"
           "{0}".format(END, RED, BLUE))


def bad_audio_ID():
    print ("{1} > ERROR : {2}Please, specify valid audio ID !"
           "{0}".format(END, RED, BLUE))


def bad_audio_title():
    print ("{1} > ERROR : {2}Please, specify audio title !"
           "{0}".format(END, RED, BLUE))


def bad_audio_codec():
    print ("{1} > ERROR : {2}Please, specify valid audio codec !"
           "{0}".format(END, RED, BLUE))


def bad_audio_bitrate():
    print ("{1} > ERROR : {2}Please, specify valid audio bi"
           "trate !{0}".format(END, RED, BLUE))


def bad_audio_surround():
    print ("{1} > ERROR : {2}Please, specify valid audio su"
           "rround !{0}".format(END, RED, BLUE))


def bad_audio_sampling_rate():
    print ("{1} > ERROR : {2}Please, specify valid sampling"
           " rate !{0}".format(END, RED, BLUE))


def bad_subs_title():
    print ("{1} > ERROR : {2}Please, specify subtitles "
           "track title !{0}".format(END, RED, BLUE))


def bad_subtitles_ID():
    print ("{1} > ERROR : {2}Please, specify valid subt"
           "itles track !{0}".format(END, RED, BLUE))


def bad_subtitles_source():
    print ("{1} > ERROR : {2}Bad subtitles source, please try"
           " again !{0}".format(END, RED, BLUE))


def bad_subtitles_format():
    print ("{1} > ERROR : {2}Bad subtitles format, please try"
           " again !{0}".format(END, RED, BLUE))


def bad_subs_delay():
    print ("{1} > ERROR : {2}Please specify valid delay value !"
           "{0}".format(END, RED, BLUE))


def bad_subs_type():
    print ("{1} > ERROR : {2}Please specify valid subtitles type !"
           "{0}".format(END, RED, BLUE))


def bad_ar():
    print ("{1} > ERROR : {2}Bad Aspect Ratio choice, please try"
           " again !{0}".format(END, RED, BLUE))


def bad_sar():
    print ("{1} > ERROR : {2}Bad Sample Aspect Ratio choice, please try"
           " again !{0}".format(END, RED, BLUE))


def bad_reso_width():
    print ("{1} > ERROR : {2}Bad WIDTH entry, please try"
           " again !{0}".format(END, RED, BLUE))


def bad_reso_height():
    print ("{1} > ERROR : {2}Bad HEIGHT entry, please try"
           " again !{0}".format(END, RED, BLUE))


def bad_crop_width():
    print ("{1} > ERROR : {2}Bad CROP WIDTH entry, please try"
           " again !{0}".format(END, RED, BLUE))


def bad_crop_height():
    print ("{1} > ERROR : {2}Bad CROP HEIGHT entry, please try"
           " again !{0}".format(END, RED, BLUE))


def bad_crop_LR():
    print ("{1} > ERROR : {2}Bad CROP LEFT/RIGHT entry, please "
           "try again !{0}".format(END, RED, BLUE))


def bad_crop_TB():
    print ("{1} > ERROR : {2}Bad CROP TOP/BOTTOM entry, please "
           "try again !{0}".format(END, RED, BLUE))


def bad_format_profile():
    print ("{1} > ERROR : {2}Bad FORMAT PROFILE entry, please "
           "try again !{0}".format(END, RED, BLUE))


def bad_nfosource():
    print ("{1} > ERROR : {2}Please, specify RELEASE SOURCE !{0}"
           .format(END, RED, BLUE))


# BITRATE CALCULATOR ERRORS
def bitrate_time_error():
    print ("{1} > ERROR : {2}Please, specify valid time !"
           "{0}".format(END, RED, BLUE))


def bitrate_audio_error():
    print ("{1} > ERROR : {2}Please, specify audio bitrate !"
           "{0}".format(END, RED, BLUE))


def bitrate_size_error():
    print ("{1} > ERROR : {2}Bad size selection, please try again !"
           "{0}".format(END, RED, BLUE))


# GENPREZ MESSAGES
def genprez_error():
    print ("\n{1} > Genprez ERROR : {2}Movie not found, please try "
           "again !\n{0}".format(END, RED, BLUE))


def genprez_success():
    print ("{0} > {1}Presentation created !{2}".format(RED, GREEN, END))


def genprez_process():
    print ("{0} > {1}Creating presentation...{2}".format(RED, BLUE, END))


# IMGUR MESSAGES
def imgur_process():
    print ("{0} > {1}Uploading Thumbnails...{2}".format(RED, BLUE, END))


def imgur_print_url(thumb_link):
    print ("{1} > {0}Thumbnails url : {4}{2}{3}"
           .format(GREEN, RED, thumb_link, END, YELLOW))


def imgur_upload_error(e):
    print ("{3} > {0}Thumbnails Upload Error : {1}{2}{3}"
           .format(RED, BLUE, str(e), END))


def imgur_timeout_error():
    print ("{2} > {0}Thumbnails Upload Error : {1} Connexion timeout !{2}"
           .format(RED, BLUE, END))


def imgur_source_error():
    print ("{0} > ERROR : {1}Bad thumbnails selection, please try"
           " again !{2}".format(RED, BLUE, END))


# THUMBNAILS MESSAGES
def bad_thumbs(e):
    print ("{0} > Thumbnails ERROR : {1}{2}{3}"
           .format(RED, BLUE, str(e), END))


def thumbnails_process():
    print ("{0} > {1}Creating thumbnails...{2}".format(RED, BLUE, END))


def thumbnails_success():
    print ("{0} > {1}Thumbnails created !{2}".format(RED, GREEN, END))


# MKVMERGE MESSAGES
def muxing_process():
    print ("{0} > {1}Mkvmerge is running, be patient...{2}"
           .format(RED, BLUE, END))


def muxing_success():
    print ("{0} > {1}Mkvmerge remux done !{2}".format(RED, GREEN, END))


# ANKOA GLOBAL MESSAGES
def global_error(e):
    print ("{1} > ERROR : {2}{4}\n{1} > {0}Please try again, or report "
           "this error on {3}: {5}https://github.com/grm34/AnkoA/issues{3}"
           .format(GREEN, RED, BLUE, END, str(e), YELLOW))


def subextract_message():
    print ("{0} > {1}Extraction(s) done, check your folder & run OCR if"
           " required !{2}\n >{0} WARNING :{3} put final srt in source"
           " folder before next step !{2}".format(RED, GREEN, END, BLUE))


def extracting():
    print ("{0} > {1}Extracting subtitles...{2}".format(RED, BLUE, END))


def scanning():
    print ("{0} > {1}Scanning API Databases...{2}".format(RED, BLUE, END))


def ffmpeg_success():
    print ("{0} > {1}FFmpeg release created !{2}"
           .format(RED, GREEN, END))


def ankoa_success():
    print ("{0} > {1}All jobs done, congratulations !{2}"
           .format(RED, GREEN, END))
