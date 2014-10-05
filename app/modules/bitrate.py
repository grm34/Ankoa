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
from app.main.inputs import (ask_HH, ask_MM, ask_SS,
                             ask_desired_audio_bitrate, ask_desired_size)
from app.main.events import (bitrate_time_error, bitrate_size_error,
                             bitrate_audio_error)
from app.main.param import regex

(hb_regex, crf_regex, delay_regex, fp_regex, aq_regex, url_regex) = regex()


def calcul():

    # Hours
    HH = ask_HH()
    verif_HH = re.compile(crf_regex, flags=0).search(HH)
    while not HH or HH.isdigit() is False\
            or verif_HH is not None or int(HH) > 23:
        bitrate_time_error()
        HH = ask_HH()
        verif_HH = re.compile(crf_regex, flags=0).search(HH)

    # Minutes
    MM = ask_MM()
    verif_MM = re.compile(crf_regex, flags=0).search(MM)
    while not MM or MM.isdigit() is False\
            or verif_MM is not None or int(MM) > 59:
        bitrate_time_error()
        MM = ask_MM()
        verif_MM = re.compile(crf_regex, flags=0).search(MM)

    # Seconds
    SS = ask_SS()
    verif_SS = re.compile(crf_regex, flags=0).search(SS)
    while not SS or SS.isdigit() is False\
            or verif_SS is not None or int(SS) > 59:
        bitrate_time_error()
        SS = ask_SS()
        verif_SS = re.compile(crf_regex, flags=0).search(SS)

    # Audio bitrate
    audiobit = ask_desired_audio_bitrate()
    verif_bits = re.compile(crf_regex, flags=0).search(audiobit)
    while not audiobit or audiobit.isdigit() is False\
            or verif_bits is not None or int(audiobit) > 3000:
        bitrate_audio_error()
        audiobit = ask_desired_audio_bitrate()
        verif_bits = re.compile(crf_regex, flags=0).search(audiobit)

    # Release desired size
    resp = ["1", "2", "3", "4", "5", "6", "7", "8"]
    values = ["", "357.8", "562.9", "716.3", "1439.3",
              "2151", "2875.5", "4585.2", "6881.5"]
    rls_size = ask_desired_size()
    while rls_size not in resp:
        bitrate_size_error()
        rls_size = ask_desired_size()
    calsize = values[int(rls_size)]
    return (HH, MM, SS, audiobit, rls_size, calsize)


# RUN CALCUL
def calc(HH, MM, SS, audiobit, rls_size, calsize):
    return (
        "wcalc [{" + calsize + "-[{" + audiobit + "/8}/1024*[{" + HH +
        "*3600}+{" + MM + "*60}+" + SS + "]]}/[{" + HH + "*3600}+{" +
        MM + "*60}+" + SS + "]]*8*1024")
