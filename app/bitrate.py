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
    modify and/ or redistribute the software under the terms of the CeCILL-C
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
    MM = raw_input("{0}CALCULATOR MINUTES : {1}".format(GREEN, END))
    SS = raw_input("{0}CALCULATOR SECONDS : {1}".format(GREEN, END))
    audiobit = raw_input("{0}CALCULATOR AUDIO BITRATE : {1}"
                         .format(GREEN, END))
    rls_size = raw_input("{0}CALCULATOR SIZE > \n{1}350 - 550 - 700 - 1.37 - "
                         "2.05 - 2.74 - 4.37 - 6.56{0} : {2}"
                         .format(GREEN, YELLOW, GREEN, END))

    if (rls_size == "350"):
        calsize = "357.8"
    elif (rls_size == "550"):
        calsize = "562.9"
    elif (rls_size == "700"):
        calsize = "716.3"
    elif (rls_size == "1.37"):
        calsize = "1439.3"
    elif (rls_size == "2.05"):
        calsize = "2151"
    elif (rls_size == "2.74"):
        calsize = "2875.5"
    elif (rls_size == "4.37"):
        calsize = "4585.2"
    elif (rls_size == "6.56"):
        calsize = "6881.5"
    else:
        calsize = "1439.3"

    info_calcul = (HH, MM, SS, audiobit, rls_size, calsize)
    return (info_calcul)


def calc(HH, MM, SS, audiobit, rls_size, calsize):
    return (
        "wcalc [{{0}-[{{1}/8}/1024*[{{2}*3600}+{{3}*60}+{4}]]}/[{{2}*3600}+{"
        "{3}*60}+{4}]]*8*1024".format(calsize, audiobit, HH, MM, SS))
