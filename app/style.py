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

from django.utils.encoding import (smart_str, smart_unicode)


def color():
    BLUE = '\033[36m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    GREEN = '\033[32m'
    END = '\033[0;0m'
    values = (BLUE, RED, YELLOW, GREEN, END)
    return (values)

(BLUE, RED, YELLOW, GREEN, END) = color()


def help():
    v = "AnkoA v3.2.2"
    help = "{0}\nVersion.....:{2}   {5}\n"\
           "{0}Copying.....:{1}   CeCILL-C License\n"\
           "{0}Author......:{1}   grm34 (FRIPOUILLEJACK)\n"\
           "{0}Email.......:{1}   fripouillejack@gmail.com\n"\
           "{0}Link........:{3}   https://github.com/grm34/AnkoA\n"\
           "{0}Infos.......:{4}   FFMPEG Easy Encoding Tools\n\n"\
           "{2} MEMENTO :\n\n"\
           "{4}   SOURCE..............:  {1}release source     {3}ex:{1}  10"\
           "80p.THENiGHTMAREiNHD\n"\
           "{4}   SUBS................:  {1}subtitles source   {3}ex:{1}  FU"\
           "LL.FRENCH.Z1\n"\
           "{4}   SUBFORCED...........:  {1}forced subtitles   {3}ex:{1}  FR"\
           "ENCH.FORCED or N/A\n"\
           "{4}   LANGUAGE............:  {1}release language   {3}ex:{1}  EN"\
           "GLiSH\n"\
           "{4}   FORMAT..............:  {1}release format     {3}ex:{1}  72"\
           "0p.BluRay\n"\
           "{4}   CODECS..............:  {1}release codecs     {3}ex:{1}  AC"\
           "3.x264\n"\
           "{4}   SiZE................:  {1}release size       {3}ex:{1}  1."\
           "37Go\n"\
           "{4}   iD_iMDB.............:  {1}release iMDB iD    {3}ex:{1}  11"\
           "21931 (without 'tt')\n"\
           "{4}   URL.................:  {1}release infos url  {3}ex:{1}  ht"\
           "tp://www.imdb.com/title/tt0315733"\
           .format(BLUE, END, RED, YELLOW, GREEN, v)

    values = (v, help)
    return values

(v, version) = help()


def banner():
    print(smart_str(
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
    """ + END))


def next():
    print(smart_str(
    RED + """
    ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦
    #######################################################################
    ########################## """ + YELLOW + """-- NEXT ENCODE --""" + RED +
    """ ##########################
    #######################################################################
    ¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦
    """ + END))
