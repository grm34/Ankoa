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


# FFMPEG CLI
def ffmpeg_crf(thumb, source, title, year, team, idvideo, interlace,
               fps, string, reso, codec, crf, level, param, audio_config,
               sub_config, stag, mark):
    return (
        "cd {0} && ffmpeg -i {1} -metadata title='{2}.{3}' -metadata "
        "proudly.presented.by='{4}' -map 0:{5}{6}{7} -metadata:s:v:0 "
        "title= -metadata:s:v:0 language= -f {8}{9} -c:v:0 {10} -crf "
        "{11} -level {12}{13}{14}{15} -passlogfile {2}.{3}.log "
        "{2}.{3}{16}{17}"
        .format(thumb, source, title, year, team, idvideo, interlace,
                fps, string, reso, codec, crf, level, param,
                audio_config, sub_config, stag, mark))


# FFMPEG 2PASS
def ffmpeg_2pass(thumb, source, idvideo, interlace2, fps, string, reso,
                 codec, bit, level, pass1, title, year, stag, mark,
                 team, interlace, param, audio_config, sub_config):
    return (
        "cd {0} && ffmpeg -i {1} -pass 1 -map 0:{2}{3}{4} -f {5}{6} -"
        "c:v:0 {7} -b:v:0 {8}k -level {9}{10} -an -sn -passlogfile "
        "{11}.{12}.log {11}.{12}{13}{14} && ffmpeg -y -i {1} -pass 2 "
        "-metadata title='{11}.{12}' -metadata proudly.presented.by='"
        "{15}' -map 0:{2}{16}{4} -metadata:s:v:0 title= -metadata:s:v"
        ":0 language= -f {5}{6} -c:v:0 {7} -b:v:0 {8}k -level {9}{17}"
        "{18}{19} -passlogfile {11}.{12}.log {11}.{12}{13}{14}"
        .format(thumb, source, idvideo, interlace2, fps, string, reso,
                codec, bit, level, pass1, title, year, stag, mark,
                team, interlace, param, audio_config, sub_config))
