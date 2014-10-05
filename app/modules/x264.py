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
from app.main.inputs import *
from app.main.param import regex
from app.main.events import (expert_mode_error, bad_format_profile)

(hb_regex, crf_regex, delay_regex, fp_regex, aq_regex, url_regex) = regex()


# Format Profile ( min 1.1 / max: 5.2 )
def format_profile():
    level = ask_format_profile()
    verif5 = re.compile(fp_regex, flags=0).search(level)
    while not level or len(level) != 3 or verif5 is None:
        bad_format_profile()
        level = ask_format_profile()
        verif5 = re.compile(fp_regex, flags=0).search(level)
    return level


# Preset x264/x265
def x264_preset():
    preset = ""
    preset = ask_x264_preset()
    preset_resp = ["1", "2", "3", "4", "5"]
    preset_values = ["", "fast", "slow", "slower", "veryslow", "placebo"]
    if (preset in preset_resp):
        preset = " -preset {0}".format(preset_values[int(preset)])
    return preset


# Tune x264/x265
def x264_tune():
    tune = ""
    tuned = ask_x264_tune()
    tuned_resp = ["1", "2", "3", "4", "5", "6", "7", "8"]
    tuned_values = ["", "film", "animation", "grain", "stillimage", "psnr",
                    "ssim", "fastdecode", "zerolatency"]
    if (tuned in tuned_resp):
        tune = " -tune {0}".format(tuned_values[int(tuned)])

    return tune


# Default Threads
def default_threads(preset, tune):
    param = "{0}{1} -threads 0".format(preset, tune)
    pass1 = "{0}{1} -threads 0".format(preset, tune)
    return (param, pass1)


# Advanced Mode
def advanced_mode(encode_type):

    # Threads ( max: 32 / default: 0 )
    threads = ask_threads()
    verif_z0 = re.compile(crf_regex, flags=0).search(threads)
    while not threads or threads.isdigit() is False\
            or verif_z0 is not None or int(threads) > 32:
        expert_mode_error()
        threads = ask_threads()
        verif_z0 = re.compile(crf_regex, flags=0).search(threads)
    threads = " -threads {0}".format(threads)

    # Threads Type
    thread_type = ask_threads_type()
    while not thread_type or len(thread_type) != 1\
            or thread_type.isdigit() is False\
            or int(thread_type) < 1 or int(thread_type) > 3:
        expert_mode_error()
        thread_type = ask_threads_type()

    if (thread_type == "1"):
        thread_type = " -thread_type slice"
    elif (thread_type == "2"):
        thread_type = " -thread_type frame"
    else:
        thread_type = ""

    # First PASS
    if (encode_type == "3"):
        fastfirstpass = ""
    else:
        fastfirstpass = ask_fastfirstpass()
        if (fastfirstpass == "y"):
            fastfirstpass = " -fastfirstpass 1"
        elif (fastfirstpass == "n"):
            fastfirstpass = " -fastfirstpass 0"
        else:
            fastfirstpass = ""

    # Refs Frames ( max: 16 )
    refs = ask_refs()
    verif_z1 = re.compile(crf_regex, flags=0).search(refs)
    while not (refs) or refs.isdigit() is False\
            or verif_z1 is not None or int(refs) > 16:
        expert_mode_error()
        refs = ask_refs()
        verif_z1 = re.compile(crf_regex, flags=0).search(refs)
    refs = " -refs {0}".format(refs)

    # Mixed Refs
    mixed = ask_mixed_refs()
    if (mixed == "n"):
        mixed = " -mixed-refs 0"
    elif (mixed == "y"):
        mixed = " -mixed-refs 1"
    else:
        mixed = ""

    # MAX B-Frames ( max: 16 )
    bf = ask_max_bframes()
    while not bf or bf.isdigit() is False or int(bf) > 16:
        expert_mode_error()
        bf = ask_max_bframes()
    bf = " -bf {0}".format(bf)

    # Pyramidal
    pyramid = ask_pyramidal()
    pyramid_resp = ["1", "2", "3"]
    pyramid_values = ["", "none", "normal", "strict"]
    if (pyramid in pyramid_resp):
        pyramid = " -b-pyramid {0}".format(pyramid_values[int(pyramid)])
    else:
        pyramid = ""

    # Weight B-Frames
    weightb = ask_weight_bframes()
    if (weightb == "n"):
        weightb = " -weightb 0"
    elif (weightb == "y"):
        weightb = " -weightb 1"
    else:
        weightb = ""

    # Weight P-Frames
    weightp = ask_weight_pframes()
    weightp_resp = ["1", "2", "3"]
    weightp_values = ["", "none", "simple", "smart"]
    if (weightp in weightp_resp):
        weightp = " -weightp {0}".format(weightp_values[int(weightp)])
    else:
        weightp = ""

    # 8x8 Transform
    dct = ask_8x8_transform()
    if (dct == "n"):
        dct = " -8x8dct 0"
    elif (dct == "y"):
        dct = " -8x8dct 1"
    else:
        dct = ""

    # Cabac
    cabac = ask_cabac()
    if (cabac == "n"):
        cabac = " -coder vlc"
    elif (cabac == "y"):
        cabac = " -coder ac"
    else:
        cabac = ""

    # Adaptive B-Frames
    b_strat = ask_bstrategy()
    b_strategy_resp = ["1", "2", "3"]
    if (b_strat in b_strategy_resp):
        b_strategy = " -b_strategy {0}"\
                     .format(b_strategy_resp.index(b_strat))
    else:
        b_strategy = ""

    # Direct Mode
    direct = ask_direct_mode()
    direct_resp = ["1", "2", "3", "4"]
    direct_values = ["", "none", "spatial", "temporal", "auto"]
    if (direct in direct_resp):
        direct = " -direct-pred {0}".format(direct_values[int(direct)])
    else:
        direct = ""

    # Motion Estimation
    me_method = ask_me_method()
    me_resp = ["1", "2", "3", "4", "5"]
    me_values = ["", "dia", "hex", "umh", "esa", "tesa"]
    if (me_method_ in me_resp):
        me_method = " -me_method {0}".format(me_values[int(me_method)])
    else:
        me_method = ""

    # Subpixel ( max: 11 )
    subq = ask_subpixel()
    while not (subq) or subq.isdigit() is False or int(subq) > 11:
        expert_mode_error()
        subq = ask_subpixel()
    subq = " -subq {0}".format(subq)

    # Estimation Range ( max: 64 )
    me_range = ask_motion_range()
    while not (me_range) or me_range.isdigit() is False\
            or int(me_range) > 64:
        expert_mode_error()
        me_range = ask_motion_range()
    me_range = " -me_range {0}".format(me_range)

    # Partitions
    parts = ask_partitions()
    parts_resp = ["1", "2", "3", "4", "5", "6", "7"]
    p_values = ["", "all", "p8x8", "p4x4", "none", "b8x8", "i8x8", "i4x4"]
    if (parts in parts_resp):
        partitions = " -partitions {0}".format(p_values[int(parts)])
    else:
        partitions = ""

    # Trellis Mode
    trellis = ask_trellis()
    trellis_resp = ["1", "2", "3"]
    if (trellis in trellis_resp):
        trellis = " -trellis {0}".format(trellis_resp.index(trellis))
    else:
        trellis = ""

    # Quantization Mode
    aq_mod = ask_aq_mode()
    aq_mod_resp = ["1", "2", "3"]
    if aq_mod in aq_mod_resp:
        aq_mode = " -aq-mode {0}".format(aq_mod_resp.index(aq_mod))
    else:
        aq_mode = ""

    # Quantization Strength ( max 2.9 )
    aq = ask_aq_strength()
    aq_mod_regex = re.compile(aq_regex, flags=0).search(aq)
    while not aq or aq_mod_regex is None:
        expert_mode_error()
        aq = ask_aq_strength()
        aq_mod_regex = re.compile(aq_regex, flags=0).search(aq)
    aq = " -aq-strength {0}".format(aq)

    # Psychovisual Optimization
    psy = ask_psy_optimization()
    if (psy) == "n":
        psy = " -psy 0"
    elif (psy) == "y":
        psy = " -psy 1"
    else:
        psy = ""

    # Rate Distortion
    psy1 = ask_rate_distortion()
    # psy1_regex = r"^[0-2]{1}[.][0-9]{2}$"
    # psya_regex = re.compile(psy1_regex, flags=0).search(psy1)
    if not (psy1):
        psyrd = ""
    else:

        # Psy RD (
        psy2 = ask_psy_rd()

        if not (psy2):
            psyrd = ""
        else:
            psyrd = " -psy-rd {0}:{1}".format(psy1, psy2)

    # Deblock
    deblock = ask_deblock()
    if not (deblock):
        deblock = ""
    else:
        deblock = " -deblock {0}".format(deblock)

    # Frames Lookahead
    lookahead = ask_lookahead()
    if not (lookahead):
        lookahead = ""
    else:
        lookahead = " -rc-lookahead {0}".format(lookahead)

    # BluRay Compatibility
    bluray = ask_bluray_compatibility()
    if (bluray == "y"):
        bluray = " -bluray-compat 1"
    elif (bluray == "n"):
        bluray = " -bluray-compat 0"
    else:
        bluray = ""

    # Fast Skip
    fastpskip = ask_fast_skip()
    if (fastpskip == "y"):
        fastpskip = " -fast-pskip 1"
    elif (fastpskip == "n"):
        fastpskip = " -fast-pskip 0"
    else:
        fastpskip = ""

    # Keyframe Interval
    g = ask_keyframe_interval()
    if not (g):
        g = ""
    else:
        g = " -g {0}".format(g)

    # Minimal Key Interval
    keyint_min = ask_key_min_interval()
    if not (keyint_min):
        keyint_min = ""
    else:
        keyint_min = " -keyint_min {0}".format(keyint_min)

    # Scene Cut
    scenecut = ask_scenecut()
    if not (scenecut):
        scenecut = ""
    else:
        scenecut = " -sc_threshold {0}".format(scenecut)

    # Chroma Motion
    cmp = ask_chroma_motion()
    if (cmp == "n"):
        cmp = " -cmp sad"
    elif (cmp == "y"):
        cmp = " -cmp chroma"
    else:
        cmp = ""

    # Expert Mode Values
    param = "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}{14}"\
            "{15}{16}{17}{18}{19}{20}{21}{22}{23}{24}{25}{26}"\
            "{27}{28}{29}{30}"\
            .format(preset, tune, threads, thread_type, fastfirstpass,
                    refs, mixed, bf, pyramid, weightb, weightp, dct,
                    cabac, b_strategy, direct, me_method, subq, me_range,
                    partitions, trellis, aq, psy, psyrd, deblock,
                    lookahead, bluray, fastpskip, g, keyint_min,
                    scenecut, cmp, aq_mod)

    # First Pass Values
    pass1 = "{0}{1}{2}{3}{4}".format(preset, tune, threads,
                                     thread_type, fastfirstpass)

    return (param, pass1)
