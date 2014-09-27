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

from style import color

(BLUE, RED, YELLOW, GREEN, END) = color()


def calcul():
    HH = raw_input("{0}CALCULATOR HOURS : {1}".format(GREEN, END))
    while not HH or HH.isdigit() is False or int(HH) > 23:
        print ("{0} -> {1}ERROR : {2}Please, specify valid entry !"
               " {1}(ex: 1){3}".format(GREEN, BLUE, RED, END))
        HH = raw_input("{0}CALCULATOR HOURS : {1}".format(GREEN, END))

    MM = raw_input("{0}CALCULATOR MINUTES : {1}".format(GREEN, END))
    while not MM or MM.isdigit() is False or int(MM) > 59:
        print ("{0} -> {1}ERROR : {2}Please, specify valid entry !"
               " {1}(ex: 15){3}".format(GREEN, BLUE, RED, END))
        MM = raw_input("{0}CALCULATOR MINUTES : {1}".format(GREEN, END))

    SS = raw_input("{0}CALCULATOR SECONDS : {1}".format(GREEN, END))
    while not SS or SS.isdigit() is False or int(SS) > 59:
        print ("{0} -> {1}ERROR : {2}Please, specify valid entry !"
               " {1}(ex: 53){3}".format(GREEN, BLUE, RED, END))
        SS = raw_input("{0}CALCULATOR SECONDS : {1}".format(GREEN, END))

    audiobit = raw_input("{0}CALCULATOR AUDIO BITRATE : {1}"
                         .format(GREEN, END))
    while not audiobit or audiobit.isdigit() is False:
        print ("{0} -> {1}ERROR : {2}Please, specify valid entry !"
               " {1}(ex: 448){3}".format(GREEN, BLUE, RED, END))
        audiobit = raw_input("{0}CALCULATOR AUDIO BITRATE : {1}"
                             .format(GREEN, END))

    rls_size = raw_input("{0}CALCULATOR SIZE > \n{1}350Mo {0}[1]{1} - 550Mo "
                         "{0}[2]{1} - 700Mo {0}[3]{1} - 1.37Go {0}[4]{1} -\n"
                         "2.05Go {0}[5]{1} - 2.74Go {0}[6]{1} - 4.37Go {0}[7]"
                         "{1} - 6.56Go{0} {0}[8] : {2}"
                         .format(GREEN, YELLOW, END))

    resp = ["1", "2", "3", "4", "5", "6", "7", "8"]

    values = ["", "357.8", "562.9", "716.3", "1439.3",
              "2151", "2875.5", "4585.2", "6881.5"]

    if (rls_size in resp):
        calsize = values[int(rls_size)]
    else:
        calsize = values[4]

    info_calcul = (HH, MM, SS, audiobit, rls_size, calsize)
    return (info_calcul)


def calc(HH, MM, SS, audiobit, rls_size, calsize):
    return (
        "wcalc [{" + calsize + "-[{" + audiobit + "/8}/1024*[{" + HH +
        "*3600}+{" + MM + "*60}+" + SS + "]]}/[{" + HH + "*3600}+{" +
        MM + "*60}+" + SS + "]]*8*1024")
