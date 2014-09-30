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

from style import (color, help)

(v, version) = help()
(BLUE, RED, YELLOW, GREEN, END) = color()


# HELP USAGE VALUES
def ankoa_help():
    usage = "{0}./ankoa.py{1}\n{2}".format(GREEN, END, version)
    return usage


def genprez_help():
    usage = "{0}./genprez.py LANGUAGE FORMAT CODECS SUBS SIZE ID_IMDB"\
            "{1}\n{2}".format(GREEN, END, version)
    return usage


def imgur_help():
    usage = "{0}./imgur.py /path/to/image.png"\
            "{1}\n{2}".format(GREEN, END, version)
    return usage


def make_help():
    usage = "{0}./make.py SOURCE.mkv SOURCE SUBS SUBFORCED URL"\
            "{1}\n{2}".format(GREEN, END, version)
    return usage


def setup_help():
    usage = "{0}python setup.py [{3}install{0}] | [{3}update{0}]"\
            "{1}\n{2}".format(GREEN, END, version, YELLOW)
    return usage


def thumbnails_help():
    usage = "./thumbnails.py source.video 5 2"\
            "{1}\n{2}".format(GREEN, END, version)
    return usage


# ANKOA SYSTEM ERRORS
def global_error():
    print ("{0} -> {1}ERROR : {2}{4}{3}"
           .format(GREEN, RED, BLUE, END, str(e)))


def expert_mode_error():
    print ("{0} -> {1}ERROR : {2}Bad value, are you sure to be able"
           " to use this mode ?{3}".format(GREEN, RED, BLUE, END))


def bad_source():
    print ("{0} -> {1}ERROR : {2}Bad source selection, please try"
           " again !{3}".format(GREEN, RED, BLUE, END))


def bad_title():
    print ("{0} -> {1}ERROR : {2}Please, specify release title !{3}"
           .format(GREEN, RED, BLUE, END))


def bad_year():
    print ("{0} -> {1}ERROR : {2}Please, specify valid release year !"
           "{3}".format(GREEN, RED, BLUE, END))


def bad_crf():
    print ("{0} -> {1}ERROR : {2}Please, specify valid crf value ! "
           "{3}".format(GREEN, RED, BLUE, END))


def bad_video_bitrate():
    print ("{0} -> {1}ERROR : {2}Please, specify valid video "
           "bitrate !{3}".format(GREEN, RED, BLUE, END))


def bad_video_ID():
    print ("{0} -> {1}ERROR : {2}Please, specify valid video ID !{3}"
           .format(GREEN, RED, BLUE, END))


def bad_fps():
    print ("{0} -> {1}ERROR : {2}Please, specify valid video FPS !"
           "{3}".format(GREEN, RED, BLUE, END))


def bad_audio_ID():
    print ("{0} -> {1}ERROR : {2}Please, specify valid audio ID !"
           "{3}".format(GREEN, RED, BLUE, END))


def bad_audio_title():
    print ("{0} -> {1}ERROR : {2}Please, specify audio title !"
           "{3}".format(GREEN, RED, BLUE, END))


def bad_audio_codec():
    print ("{0} -> {1}ERROR : {2}Please, specify valid codec !"
           "{3}".format(GREEN, RED, BLUE, END))


def bad_audio_bitrate():
    print ("{0} -> {1}ERROR : {2}Please, specify valid audio bi"
           "trate !{3}".format(GREEN, RED, BLUE, END))


def bad_audio_surround():
    print ("{0} -> {1}ERROR : {2}Please, specify valid audio su"
           "rround !{3}".format(GREEN, RED, BLUE, END))


def bad_audio_sampling_rate():
    print ("{0} -> {1}ERROR : {2}Please, specify valid sampling"
           " rate !{3}".format(GREEN, RED, BLUE, END))


def bad_subs_title():
    print ("{0} -> {1}ERROR : {2}Please, specify subtitles "
           "track title !{3}".format(GREEN, RED, BLUE, END))


def bad_subtitles_ID():
    print ("{0} -> {1}ERROR : {2}Please, specify valid subt"
           "itles track !{3}".format(GREEN, RED, BLUE, END))


def bad_subtitles_source():
    print ("{0} -> {1}ERROR : {2}Bad subtitles source, please try"
           " again !{3}".format(GREEN, RED, BLUE, END))


def bad_subs_delay():
    print ("{0} -> {1}ERROR : {2}Please specify valid delay value !"
           "{3}".format(GREEN, RED, BLUE, END))


def bad_ar():
    print ("{0} -> {1}ERROR : {2}Bad Aspect Ratio choice, please try"
           " again !{3}".format(GREEN, RED, BLUE, END))


def bad_sar():
    print ("{0} -> {1}ERROR : {2}Bad Sample Aspect Ratio choice, please try"
           " again !{3}".format(GREEN, RED, BLUE, END))


def bad_reso_width():
    print ("{0} -> {1}ERROR : {2}Bad WIDTH entry, please try"
           " again !{3}".format(GREEN, RED, BLUE, END))


def bad_reso_height():
    print ("{0} -> {1}ERROR : {2}Bad HEIGHT entry, please try"
           " again !{3}".format(GREEN, RED, BLUE, END))


def bad_crop_width():
    print ("{0} -> {1}ERROR : {2}Bad CROP WIDTH entry, please try"
           " again !{3}".format(GREEN, RED, BLUE, END))


def bad_crop_height():
    print ("{0} -> {1}ERROR : {2}Bad CROP HEIGHT entry, please try"
           " again !{3}".format(GREEN, RED, BLUE, END))


def bad_crop_LR():
    print ("{0} -> {1}ERROR : {2}Bad CROP LEFT/RIGHT entry, please "
           "try again !{3}".format(GREEN, RED, BLUE, END))


def bad_crop_TB():
    print ("{0} -> {1}ERROR : {2}Bad CROP TOP/BOTTOM entry, please "
           "try again !{3}".format(GREEN, RED, BLUE, END))


def bad_format_profile():
    print ("{0} -> {1}ERROR : {2}Bad FORMAT PROFILE entry, please "
           "try again !{3}".format(GREEN, RED, BLUE, END))


def bad_nfosource():
    print ("{0} -> {1}ERROR : {2}Please, specify RELEASE SOURCE !{3}"
           .format(GREEN, RED, BLUE, END))


# ANKOA GLOBAL MESSAGES
def subextract_message():
    print ("{0}\n ->{1} EXTRACTION DONE, CHECK RESULT FOLDER & RUN OCR I"
           "F NEEDED !{0}\n ->{1} WARNING > PUT FINAL SRT IN SOURCE FOLD"
           "ER FOR NEXT STEP !{2}\n".format(RED, GREEN, END))


def scanning():
    print ("{0} -> {1}Scanning API Databases...{2}".format(RED, BLUE, END))


# BITRATE CALCULATOR ERROR
def bitrate_entry_error():
    print ("{0} -> {1}ERROR : {2}Please, specify valid entry !"
           "{3}".format(GREEN, RED, BLUE, END))


# GENPREZ MESSAGES
def genprez_error():
    print ("\n{0} -> {1}Genprez ERROR : {2}Movie not found, please try "
           "again !\n{3}".format(GREEN, RED, BLUE, END))


def genprez_success():
    print ("{0} -> {1}PREZ CREATED, CONGRATULATIONS !{2}"
           .format(RED, GREEN, END))


# IMGUR MESSAGES
def imgur_print_url():
    print ("\n{0} Thumbnails url > {1}{2}\n{3}"
           .format(GREEN, BLUE, thumb_link, END))


def imgur_upload_error():
    print ("{0} Thumbnails Upload Error > {1}{2}{3}"
           .format(RED, BLUE, str(e), END))


def imgur_timeout_error():
    print ("{0} Thumbnails Upload Error > {1} TIMEOUT !{2}"
           .format(RED, BLUE, END))


def imgur_source_error():
    print ("{0} -> {1}ERROR : {2}Bad thumbnails selection, please try"
           " again !{3}".format(GREEN, RED, BLUE, END))


# MAKE SUCCESS MESSAGE
def make_success():
    print ("{0} -> {1}NFO, THUMBNAILS & TORRENT CREATED !{2}"
           .format(RED, GREEN, END))


# SETUP MESSAGES
def setup_success():
    print ("{0} AnkoA {1}-> {2}Installation successful !{3}"
           .format(BLUE, RED, GREEN, END))


def setup_error():
    print ("{0} AnkoA {1}-> {2}Setup error, files missing,"
           " fix it with a fresh install !{3}"
           .format(BLUE, RED, GREEN, END))


def update_success():
    print ("{0} AnkoA {1}-> {2}Update successful !{3}"
           .format(BLUE, RED, GREEN, END))


def update_error():
    print ("{0} AnkoA {1}-> {2}Update error, fix it"
           " with a fresh install !{3}"
           .format(BLUE, GREEN, RED, END))


def setup_bad_source():
    print ("{0} -> {1}ERROR : {2}Bad SOURCE PATH, please try"
           " again !{3}".format(GREEN, RED, BLUE, END))


def setup_bad_dest():
    print ("{0} -> {1}ERROR : {2}Bad DESTINATION PATH, please try"
           " again !{3}".format(GREEN, RED, BLUE, END))


def setup_bad_team():
    print ("{0} -> {1}ERROR : {2}Please, specify team name "
           "!{3}".format(GREEN, RED, BLUE, END))


def setup_bad_tk():
    print ("{0} -> {1}ERROR : {2}Please, specify valid tracker url announ"
           "ce !{3}".format(GREEN, RED, BLUE, END))


def setup_bad_api():
    print ("{0} -> {1}ERROR : {2}Please, specify valid TMDB API KEY"
           " !{3}".format(GREEN, RED, BLUE, END))


# THUMBNAILS ERROR
def bad_thumbs():
    print ("{0} ->{1} BAD THUMBS : {1}str(e){2}{3}"
           .format(GREEN, RED, BLUE, str(e), END))


# ANKOA SUCCESS
def ankoa_success():
    print ("{0} ->{1} ENCODE(s) DONE, CONGRATULATIONS !\n{0} ->{1} NFO, THU"
           "MBNAILS, (PREZ) & TORRENT CREATED !{2}".format(RED, GREEN, END))
