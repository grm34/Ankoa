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
import os
from app.main.inputs import *
from app.main.events import *
from user.settings import option
from app.main.param import bad_chars
from genprez import api_connexion
from django.utils.encoding import (smart_str, smart_unicode)

deleted = bad_chars()
(folder, thumb, tag, team, announce, tmdb_api_key, tag_thumb) = option()


# Select Source
def select_source(folder):
    prefix = ask_source()
    while not prefix or os.path.isfile(folder+prefix) is False:
        bad_source()
        prefix = ask_source()
    source = "{0}{1}".format(folder, prefix)
    return source


# Release Title
def release_title(deleted):
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
    return title


# Release Year ( min: 1895 [1st movie] / max: 2080 ? )
def release_year():
    year = ask_year()
    while not year or year.isdigit() is False or len(year) != 4\
            or int(year) < 1895 or int(year) > 2080:
        bad_year()
        year = ask_year()
    return year


# Special Tag
def release_tag():
    stag = ""
    special = ask_tag()
    if special:

        # Clean Special Tag
        for d_char in deleted:
            if d_char in special.strip():
                special = smart_str(special).strip().replace(' ', '.')\
                                                    .replace(d_char, '')
            else:
                special = smart_str(special).strip().replace(' ', '.')

        stag = ".{0}".format(special)
    return stag


# Release Title
def rls_title_codec(lang, form, xcod, tag, extend, xcod2):
    mark = ".{0}.{1}.{2}{3}-{4}{5}".format(lang, form, xcod2,
                                           xcod, tag, extend)
    prezquality = "{0} {1}{2}".format(form, xcod2, xcod)
    return (mark, prezquality)


# Release SOURCE
def release_source(deleted):
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
    return nfosource


# Find Release Title
def find_release_title(nfoimdb):
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

        # Clean PREZ Title
        if (tit[0] in data_IMDB or tit[1] in data_TMDB
                or tit[2] in data_OMDB or tit[3] in data_API):
            name = dir.replace(' ', '.').replace('/', '').replace('(', '')\
                      .replace(')', '').replace('"', '').replace(':', '')\
                      .replace("'", "").replace("[", "").replace("]", "")\
                      .replace(";", "").replace(",", "")
        else:
            name = "unknow"
    else:
        name = "no_prez"
        nfoimdb = "no_imdb"

    return (name, nfoimdb)
