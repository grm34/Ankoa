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

import os
import sys
import readline
import subprocess
from user.settings import option
from modules.audio import *
from modules.extract import *
from modules.mkvmerge import *
from modules.ratio import *
from modules.scan import *
from modules.source import *
from modules.subs import *
from modules.video import *
from modules.x264 import *
from main.events import *
from main.inputs import *
from main.main import *

(folder, thumb, tag, team, announce, tmdb_api_key, tag_thumb) = option()


def ANKOA_SYSTEM():

    # Auto Complete
    def completer(text, state):
        return (
            [entry.replace(' ', '\ ') for entry in os.listdir(
                folder + os.path.dirname(
                    readline.get_line_buffer())
                ) if entry.startswith(text)][state])

    # Set some values
    [source, title, year, stag, string, codec, encode_type, crf,
     bit, level, idvideo, fps, interlace, interlace2, audiolang,
     audio_config, sub_config, reso, param, pass1, mark, nfoimdb,
     nfosource, titlesub, subforced, prezquality, name, ask_cmds,
     subtype, audiotype, extend, sync, titlesub, charset, idsub,
     forced, sync2, titlesub2, charset2, idsub2, subsource] = ["", ] * 41

    # Run Auto Complete
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)

    # Select Source
    source = select_source(folder)

    # Stop Auto Complete
    readline.parse_and_bind("tab: ")

    # Release Title
    title = release_title(deleted)

    # Release Year
    year = release_year()

    # Special Tag
    stag = release_tag()

    # Scan Source
    source_scan(source, title, year)

    # REMUX / CRF / 2PASS ?
    encode_type = ask_2pass_crf()

    # MUXING MODE
    if (encode_type == "1"):
        (mkvmerge, mkvextract, source_mkv,
         tools) = MUXING_MODE(encode_type, source, title, year, stag, folder)
        ready = ask_remux_start()
        while (ready == "n"):
            os.system("./ankoa.py")
            sys.exit()
        try:
            muxing_process()
            subprocess.check_output(mkvextract, shell=True)
            subprocess.check_output(mkvmerge, shell=True)
            muxing_success()
            os.system(tools)
            ankoa_success()
            del_source_mkv = "rm {0}".format(source_mkv)
            os.system(del_source_mkv)
            sys.exit()

        # REMUX ERROR
        except OSError as e:
            global_error(e)
            sys.exit()
        except subprocess.CalledProcessError as e:
            global_error(e)
            sys.exit()

    # FFMPEG CRF value
    elif (encode_type == "3"):
        crf = ffmpeg_crf()

    # FFMPEG 2PASS bitrate
    else:
        calculator = ask_bitrate_calculator()
        bit = ffmpeg_2pass(calculator)

    # Video Format
    (format, form, hd_size) = video_format()

    # Video Codec
    (codec, xcod) = video_codec()

    # Video Container ( mp4 or mkv )
    (string, extend) = video_container()

    # Scan Source Tracks
    ffmpeg_scan_tracks(source, title, year)

    # Select Video Track ID
    idvideo = select_video_ID()

    # Change Video FPS
    fps = video_fps()

    # Deinterlace Video ( yadif filter )
    (interlace, interlace2) = deinterlace(encode_type)

    # Select Audio Type ( FRENCH | ENGLiSH | OTHER | MULTi | NONE )
    audiotype = ask_audio_type()

    # Audio Configuration
    (audio_config, audiocodec, lang, audiolang, audionum,
     audionum2) = AUDIO_CONFIGURATION(audiotype, encode_type)

    # Release Title
    (mark, prezquality) = RELEASE_FINAL_TITLE(audiocodec, lang, form,
                                              xcod, tag, extend)

    # SUBTITLES ?
    subsource = ask_subs_from()

    # When yes > specify Subtitles type ( ISO | MKV | M2TS | SOURCE | NONE )
    if (subsource == "1" or subsource == "3" or subsource == "4"
            or subsource == "5" or subsource == "6"):
        subtype = ask_subs_type()

        # SUBTITLES from SOURCE
        if (subsource == "1"):
            (forced, stforced, subforced, idsub, idsub2, titlesub,
             titlesub2) = SUBTITLES_FROM_SOURCE(audiotype, subtype)
        else:

            # SUBTITLES from FILE
            if (subsource == "3"):
                if (subtype == "3"):
                    (titlesub, titlesub2) = manual_title_subs()
                else:
                    (titlesub, titlesub2) = auto_title_sub(subtype)

            # SUBTITLES EXTRACTIONS
            else:
                (extract, titlesub,
                 titlesub2) = SUBTITLES_EXTRACTIONS(subsource, subtype,
                                                    source, title)
                if (subsource != "3"):
                    try:

                        # RUN EXTRACTION(s)
                        extracting()
                        subprocess.check_output(extract, shell=True)
                        subextract_message()

                    # EXTRACTION ERROR
                    except OSError as e:
                        global_error(e)
                        sys.exit()
                    except subprocess.CalledProcessError as e:
                        global_error(e)
                        sys.exit()

            # Specify Files Locations
            (idsub, idsub2, charset,
             charset2, sync, sync2) = SUBTITLES_LOCATIONS(subtype)

            # Subforced Config
            (forced, stforced) = subforced_config_EXT(subtype)
            subforced = subforced_nfo(subtype, stforced)

            # MKVMERGE Command Line
            sub_remux = MKVMERGE(subtype, audiotype, thumb, title, year, stag,
                                 mark, extend, sync, titlesub, charset, idsub,
                                 forced, sync2, titlesub2, charset2, idsub2,
                                 subsource)
    # NO SUBTITLES ( NFO )
    else:
        titlesub = "N/A"
        subforced = "N/A"

    # Scan Aspect Ratio & Autocrop
    scan_autocrop(source, title, year)

    # Screenshots verification
    screenshots_verif(source)

    # Manual Crop
    crop = manual_crop()

    # Custom Resolution
    perso = ask_custom_reso()
    if (perso == "y"):
        reso = custom(crop)

    # Standard Resolution
    else:
        reso = STANDARD_RESOLUTIONS(format, hd_size, crop)

    # x264 Format Profile
    level = format_profile()

    # x264 Preset
    preset = x264_preset()

    # x264 Tune
    tune = x264_tune()

    # ADVANCED x264 MODE
    x264 = ask_advanced_mode()
    if (x264 == "y"):
        (param, pass1) = advanced_mode(encode_type)

    # Default Threads Values
    else:
        (param, pass1) = default_threads(preset, tune)

    # Release Source
    nfosource = release_source(deleted)

    # Release IMDB ID
    nfoimdb = ask_rls_imdb()

    # Find Release Infos
    (name, nfoimdb) = find_release_title(nfoimdb)

    # Return Global Values
    return (
        source, title, year, stag, string, codec, encode_type, crf,
        bit, level, idvideo, fps, interlace, interlace2, audiolang,
        audio_config, sub_config, reso, param, pass1, mark, nfoimdb,
        nfosource, titlesub, subforced, prezquality, name, subtype,
        audiotype, extend, sync, titlesub, charset, idsub, forced,
        sync2, titlesub2, charset2, idsub2, subsource)
