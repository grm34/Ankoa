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


iNFOS:

    folder........: source path (ex: /home/toto/torrents/)
    thumb.........: result path (ex: /home/toto/encodes/)
    tag...........: your team name (ex: KULTURA)
    team..........: MEDIAINFO 'Proudly Present' Tag (ex: TEAM KULTURA)
    announce......: your favorite tracker url announce
    tmdb_api_key..: API Key from https://www.themoviedb.org/documentation/api
    tag_thumb.....: Thumbnails tag (ex: <KULTURA PROUDLY PRESENT>)

"""

from django.utils.encoding import (smart_str, smart_unicode)


def bad_chars():

    # Forbidden Chars
    deleted = ['!', '?', ',', ';', '%', '^', '$', '(', ')', '[', ']',
               '{', '}', '+', '=', '*', '&', '#', '@', '<', '>']

    return (smart_str(deleted))


def regex():

    # Regex HANDBRAKE Scan ( match tracks infos )
    hb_regex = (r"[+]\s[0-9]{1,3},\s.+?\s[(].+?[)]")

    # Regex CRF & Reso & Crop & Tracks bit, channels, ID
    # Expert Mode Values & HH, MM, SS ( match 0xxx start )
    crf_regex = (r"^[0].+")

    # Regex Subdelay ( max 5 int with or without "-" in first )
    delay_regex = (r"^[-]?[0-9]{1,5}$")

    # Regex Format Profile ( match 1.1 to 5.2 witout bad FP vals )
    fp_regex = (r"^[1-5]{1}[.][1-2]{1}$")

    # Regex Quantization ( match 0.0 to 2.9 )
    aq_regex = (r"^[0-2]{1}[.][0-9]{1}$")

    # Regex URL ( match valid tracker url )
    url_regex = (r"http[s]?:(?:[a-zA-Z]|[0-9]|[$-_@.&+]|"
                 "[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

    return (hb_regex, crf_regex, delay_regex, fp_regex, aq_regex, url_regex)
