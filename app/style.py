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


def color():
    BLUE = '\033[36m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    GREEN = '\033[32m'
    END = '\033[0;0m'
    values = (BLUE, RED, YELLOW, GREEN, END)
    return (values)

(BLUE, RED, YELLOW, GREEN, END) = color()

def version():
    v = "AnkoA v3.2.2"
    version = "Version:{0} {3}{1}\n".format(RED, END, v)
    copying = "Copying:{0} CeCILL-C License{1}\n".format(YELLOW, END)
    author = "Author:{0} grm34 {1}(FRIPOUILLEJACK)\n".format(YELLOW, END)
    email = "Email:{0} fripouillejack@gmail.com{1}\n".format(YELLOW, END)
    git_url = "Link:{0} https://github.com/grm34/AnkoA{1}\n".format(BLUE, END)
    git_info = "Infos:{0} FFMPEG Easy Encoding Tools{1}\n".format(YELLOW, END)
    opts = \
        "MEMENTO :\n\n"\
        "SOURCE..............: release source     →  1080p.THENiGHTMAREiNHD"\
        "SUBS................: subtitles source   →  FULL.FRENCH.Z1"\
        "SUBFORCED...........: forced subtitles   →  FRENCH.FORCED or N/A"\
        "LANGUAGE............: release language   →  ENGLiSH"\
        "FORMAT..............: release format     →  720p.BluRay"\
        "CODECS..............: release codecs     →  AC3.x264"\
        "SiZE................: release size       →  1.37Go"\
        "iD_iMDB.............: release iMDB iD    →  1121931 (without 'tt')"\
        "URL.................: release infos url  →  http://www.imdb.com/title/tt0315733"

    values = (v, version, copying, author, email, git_url, git_info, opts)
    return values

def banner():
    print(
    """
                                 ####    #####
        #########   ############ ####  #####  #############   #########
       ####   ####   ####   #### #### #####    ####   ####   ####   ####
      #####   #####  ####   #### ####  ######  ####   ####  #####   #####
     ############### ####   #### ####    ##### ########### ###############
    #####       ####""" + BLUE + """FRIPOUILLEJACK""" + END +
    """###     #####""" + BLUE + """AUTO-FFMPEG""" + END +
    """#####       #####""" + RED + """
    ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦
    #######################################################################
    #########################  """ + YELLOW + """[ """ + v + """ ]""" + RED +
    """  ##########################
    #######################################################################
    ######### """ + GREEN +
    """-> USE TAB OR TAB+TAB FOR SOURCES AUTOCOMPLETION <-""" + RED +
    """ #########
    ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦
    """ + END)


def next():
    print(
    RED + """
    ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦
    #######################################################################
    ########################## """ + YELLOW + """-- NEXT ENCODE --""" + RED +
    """ ##########################
    #######################################################################
    ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦
    """ + END)
