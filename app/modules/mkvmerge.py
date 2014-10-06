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

# --------- SUBTITLES FROM SOURCE ( INT ) ----------


# INT > MULTi Audio / MULTi SUBS
def INT_mA_mS(thumb, title, year, stag, mark, extend, forced):
    return (
        "mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}.{2}{3}{4} --comp"
        "ression -1:none --default-track 0:yes --forced-track 0:no --default-"
        "track 1:yes --forced-track 1:no --default-track 2:no --forced-track "
        "2:no --default-track 3:yes --forced-track 3:no --default-track 4:no "
        "{6}{0}{1}{5} && rm -f {0}{1}{5}"
        .format(thumb, title, year, stag, mark, extend, forced))


# INT > Single Audio / MULTi SUBS
def INT_sA_mS(thumb, title, year, stag, mark, extend, forced):
    return (
        "mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}.{2}{3}{4} --comp"
        "ression -1:none --default-track 0:yes --forced-track 0:no --default-"
        "track 1:yes --forced-track 1:no --default-track 2:yes --forced-track"
        " 2:no --default-track 3:no {6}{0}{1}{5} && rm -f {0}{1}{5}"
        .format(thumb, title, year, stag, mark, extend, forced))


# INT > NOAUDIO / Multi Subs
def INT_NA_mS(thumb, title, year, stag, mark, extend, forced):
    return (
        "mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}.{2}{3}{4} --comp"
        "ression -1:none --default-track 0:yes --forced-track 0:no --default-"
        "track 1:yes --forced-track 1:no --default-track 2:no {6}{0}{1}{5} &&"
        " rm -f {0}{1}{5}"
        .format(thumb, title, year, stag, mark, extend, forced))


# INT > MULTi Audio / Single SUBS
def INT_mA_sS(thumb, title, year, stag, mark, extend, forced):
    return (
        "mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}.{2}{3}{4} --comp"
        "ression -1:none --default-track 0:yes --forced-track 0:no --default-"
        "track 1:yes --forced-track 1:no --default-track 2:no --forced-track "
        "2:no --default-track 3:yes {6}{0}{1}{5} && rm -f {0}{1}{5}"
        .format(thumb, title, year, stag, mark, extend, forced))


# INT > Single Audio / Single SUBS
def INT_sA_sS(thumb, title, year, stag, mark, extend, forced):
    return (
        "mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}.{2}{3}{4} --comp"
        "ression -1:none --default-track 0:yes --forced-track 0:no --default-"
        "track 1:yes --forced-track 1:no --default-track 2:yes {6}{0}{1}{5} &"
        "& rm -f {0}{1}{5}".format(thumb, title, year, stag,
                                   mark, extend, forced))


# INT > NOAUDIO / Single Subs
def INT_NA_sS(thumb, title, year, stag, mark, extend, forced):
    return (
        "mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}.{2}{3}{4} --comp"
        "ression -1:none --default-track 0:yes --forced-track 0:no --default-"
        "track 1:yes {6}{0}{1}{5} && rm -f {0}{1}{5}"
        .format(thumb, title, year, stag, mark, extend, forced))

# --------- SUBTITLES FROM FILE ( EXT ) ----------


# EXT > MULTi Audio / MULTi SUBS
def EXT_mA_mS(thumb, title, year, stag, mark, extend, sync, titlesub, charset,
              idsub, forced, sync2, titlesub2, charset2, idsub2):
    return (
        "mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}.{2}{3}{4} --comp"
        "ression -1:none --default-track 0:yes --forced-track 0:no --default-"
        "track 1:yes --forced-track 1:no --default-track 2:no --forced-track "
        "2:no {0}{1}{5} --default-track '0:yes' --forced-track '0:no' --langu"
        "age '0:und' {6}--track-name '0:{7}'{8} {9} --default-track '0:no' "
        "{10}--language '0:und' {11}--track-name '0:{12}'{13} {14} && rm -f "
        "{0}{1}{5}".format(thumb, title, year, stag, mark, extend, sync,
                           titlesub, charset, idsub, forced, sync2,
                           titlesub2, charset2, idsub2))


# EXT > Single Audio / MULTi SUBS
def EXT_sA_mS(thumb, title, year, stag, mark, extend, sync, titlesub, charset,
              idsub, forced, sync2, titlesub2, charset2, idsub2):
    return (
        "mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}.{2}{3}{4} --comp"
        "ression -1:none --default-track 0:yes --forced-track 0:no --default-"
        "track 1:yes --forced-track 1:no {0}{1}{5} --default-track '0:yes' --"
        "forced-track '0:no' --language '0:und' {6}--track-name '0:{7}'{8} {9}"
        " --default-track '0:no' {10}--language '0:und' {11}--track-name '0:"
        "{12}'{13} {14} && rm -f {0}{1}{5}"
        .format(thumb, title, year, stag, mark, extend, sync, titlesub,
                charset, idsub, forced, sync2, titlesub2, charset2, idsub2))


# EXT > NOAUDIO / Multi Subs
def EXT_NA_mS(thumb, title, year, stag, mark, extend, sync, titlesub, charset,
              idsub, forced, sync2, titlesub2, charset2, idsub2):
    return (
        "mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}.{2}{3}{4} --comp"
        "ression -1:none --default-track 0:yes --forced-track 0:no {0}{1}{5} "
        "--default-track '0:yes' --forced-track '0:no' --language '0:und' {6}"
        "--track-name '0:{7}'{8} {9} --default-track '0:no' {10}--language '0"
        ":und' {11}--track-name '0:{12}'{13} {14} && rm -f {0}{1}{5}"
        .format(thumb, title, year, stag, mark, extend, sync, titlesub,
                charset, idsub, forced, sync2, titlesub2, charset2, idsub2))


# EXT > MULTi Audio / Single SUBS
def EXT_mA_sS(thumb, title, year, stag, mark, extend, forced,
              sync, titlesub, charset, idsub):
    return (
        "mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}.{2}{3}{4} --comp"
        "ression -1:none --default-track 0:yes --forced-track 0:no --default-"
        "track 1:yes --forced-track 1:no --default-track 2:no --forced-track "
        "2:no {0}{1}{5} --default-track '0:yes' {6}--language '0:und' {7}--tr"
        "ack-name '0:{8}'{9} {10} && rm -f {0}{1}{5}"
        .format(thumb, title, year, stag, mark, extend, forced,
                sync, titlesub, charset, idsub))


# EXT > Single Audio / Single SUBS
def EXT_sA_sS(thumb, title, year, stag, mark, extend, forced,
              sync, titlesub, charset, idsub):
    return (
        "mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}.{2}{3}{4} --comp"
        "ression -1:none --default-track 0:yes --forced-track 0:no --default-"
        "track 1:yes --forced-track 1:no {0}{1}{5} --default-track '0:yes' {6}"
        "--language '0:und' {7}--track-name '0:{8}'{9} {10} && rm -f {0}{1}{5}"
        .format(thumb, title, year, stag, mark, extend, forced,
                sync, titlesub, charset, idsub))


# EXT > NOAUDIO / Single Subs
def EXT_NA_sS(thumb, title, year, stag, mark, extend, forced,
              sync, titlesub, charset, idsub):
    return (
        "mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}.{2}{3}{4} --comp"
        "ression -1:none --default-track 0:yes --forced-track 0:no {0}{1}{5} "
        "--default-track '0:yes' {6}--language '0:und' {7}--track-name '0:{8}"
        "'{9} {10} && rm -f {0}{1}{5}"
        .format(thumb, title, year, stag, mark, extend,
                forced, sync, titlesub, charset, idsub))

# --------- NO SUBTITLES ( INT ) ----------


# INT > Multi Audio / NOSUBS
def INT_mA_NA(thumb, title, year, stag, mark, extend):
    return (
        "mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}.{2}{3}{4} --comp"
        "ression -1:none --default-track 0:yes --forced-track 0:no --default-"
        "track 1:yes --forced-track 1:no --default-track 2:no --forced-track "
        "2:no {0}{1}{5} && rm -f {0}{1}{5}"
        .format(thumb, title, year, stag, mark, extend))


# INT > Single Audio / NOSUBS
def INT_sA_NA(thumb, title, year, stag, mark, extend):
    return (
        "mv {0}{1}.{2}{3}{4} {0}{1}{5} && mkvmerge -o {0}{1}.{2}{3}{4} --comp"
        "ression -1:none --default-track 0:yes --forced-track 0:no --default-"
        "track 1:yes --forced-track 1:no {0}{1}{5} && rm -f {0}{1}{5}"
        .format(thumb, title, year, stag, mark, extend))
