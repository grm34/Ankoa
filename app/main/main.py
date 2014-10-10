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
from user.settings import option
from app.modules.audio import *
from app.modules.extract import *
from app.modules.mkvmerge import *
from app.modules.ratio import *
from app.modules.scan import *
from app.modules.source import *
from app.modules.subs import *
from app.modules.video import *
from app.modules.x264 import *
from app.main.events import *
from app.main.inputs import *
from make import ankoa_tools

(folder, thumb, tag, team, announce, tmdb_api_key, tag_thumb) = option()


def MUXING_MODE(encode_type, source, title, year, stag, folder):

    # Set some values
    extend = ".mkv"
    [audiolang, xcod2] = ["", ] * 2

    # Global infos
    (format, form, hd_size) = video_format()
    ffmpeg_scan_tracks(source, title, year)
    idvideo = select_video_ID()

    # Audio infos
    audiotype = ask_audio_type()
    (audio_config, audiocodec, lang, audiolang, audionum,
     audionum2) = AUDIO_CONFIGURATION(audiotype, encode_type)
    xcod_val = ["x264", "x265"]
    xcod2_val = ["AC3", "DTS", "AAC"]
    for item in xcod_val:
        if item in source:
            xcod = item
        else:
            xcod = "x264"
    for item2 in xcod2_val:
        if item2 in source:
            xcod2 = item2

    # Remux Title
    (mark, prezquality) = RELEASE_FINAL_TITLE(audiocodec, lang, form,
                                              xcod, tag, extend)

    # Subtitles infos
    subtype = ask_subs_type()
    while not subtype or subtype.isdigit() is False\
            or int(subtype) < 1 or int(subtype) > 3:
        bad_subs_type()
        subtype = ask_subs_type()
    if (subtype == "3"):
        (titlesub, titlesub2) = manual_title_subs()
    else:
        (titlesub, titlesub2) = auto_title_sub(subtype)
    subsource = "3"
    (idsub, idsub2, charset, charset2, sync,
     sync2) = SUBTITLES_LOCATIONS(subtype)
    (forced, stforced) = subforced_config_EXT(subtype)
    subforced = subforced_nfo(subtype, stforced)

    # Source infos
    nfosource = release_source(deleted)
    nfoimdb = ask_rls_imdb()
    (name, nfoimdb) = find_release_title(nfoimdb)

    # Mkvextract Tracks
    idvid = "{0}:{0}".format(idvideo)
    [audio_1, audio_2] = ["", ] * 2
    if audionum:
        audio_1 = " {0}:{0}".format(audionum)
    if audionum2:
        audio_2 = " {0}:{0}".format(audionum2)
    mkvextract = "cd {0} && mkdir tmp_mkv && cd tmp_mkv && mkvextract tracks"\
                 " {1} {2}{3}{4} && mkvmerge -o {5}.{6}{7}{8} {10} {11} {12}"\
                 " && mv {5}.{6}{7}{8} {9} && cd .. && rm -r tmp_mkv"\
                 .format(thumb, source, idvid, audio_1, audio_2, title, year,
                         stag, mark, folder, idvideo, audionum, audionum2)
    source_mkv = "{0}{1}.{2}{3}{4}".format(folder, title, year, stag, mark)

    # Final remux cmds
    mkvmerge = MKVMERGE(subtype, audiotype, thumb, title, year, stag, mark,
                        extend, sync, titlesub, charset, idsub, forced, sync2,
                        titlesub2, charset2, idsub2, subsource)
    temp = "{0}{1}{2}".format(thumb, title, extend)
    mkvmerge = mkvmerge.split('&&', 2)[1].strip().replace(temp, source_mkv)
    tools = ankoa_tools(thumb, title, year, stag, mark, audiolang, prezquality,
                        titlesub, subforced, nfosource, nfoimdb, name)

    # Check Mkvmerge cmd
    print_mkvmerge = ask_print_mkvmerge()
    if (print_mkvmerge == "y"):
        print mkvmerge

    return (mkvmerge, mkvextract, source_mkv, tools)


def AUDIO_CONFIGURATION(audiotype, encode_type):

    # Set some values
    [audionum, audionum2, audiolang, audiolang2, abitrate,
     abitrate2, surround, surround2, audiocodec, audiocodec2,
     audio_config] = ["", ] * 11

    # Infos > Single Audio Track
    if (audiotype == "1" or audiotype == "2" or audiotype == "3"):

        # Audio Track 00 ( ID, title, codec)
        audionum = select_audio_ID()
        if (audiotype == "3"):
            audiolang = audio_track_title(deleted)

        # When ENCODE MODE > AC3 infos
        if (encode_type != "1"):
            audiocodec = audio_track_codec(codec_resp)
            if (audiocodec == "2"):
                abitrate = audio_track_bitrate()
                surround = audio_track_channels()

    # Infos > Multi Audio Tracks
    if (audiotype == "4"):

        # Audio Track 01 ( ID, title, codec)
        audionum = select_audio_ID_01()
        audiolang = audio_track_title_01(deleted)

        # When ENCODE MODE  > AC3 infos
        if (encode_type != "1"):
            audiocodec = audio_track_codec_01(codec_resp)
            if (audiocodec == "2"):
                abitrate = audio_track_bitrate_01()
                surround = audio_track_channels_01()

        # Audio Track 02 ( ID, title, codec)
        audionum2 = select_audio_ID_02()
        audiolang2 = audio_track_title_02(deleted)

        # When ENCODE MODE > AC3 infos
        if (encode_type != "1"):
            audiocodec2 = audio_track_codec_02(codec_resp)
            if (audiocodec2 == "2"):
                abitrate2 = audio_track_bitrate_02()
                surround2 = audio_track_channels_02()

    # Title & NFO Languages
    (lang, audiolang) = audio_language_values(audiotype, audiolang)

    # Audio Config > when ENCODE MODE
    if (encode_type != "1"):

        # When AUDIO in USE
        if (audiotype == "1" or audiotype == "2"
                or audiotype == "3" or audiotype == "4"):
            audiox = ask_modif_sampling_rate()
            if (audiox == "y"):

                # Audio Sampling Rate
                if (audiotype == "4"):                  # Multi Tracks
                    audiox = audio_track_sampling_rate_01(sampling_val)
                    audiox2 = audio_track_sampling_rate_02(sampling_val)
                else:                               # Single Track
                    (audiox, audiox2) = audio_track_sampling_rate(sampling_val)
            else:                               # Default Sampling Rate
                (audiox, audiox2) = default_sampling_rate()

            # Track 01 Codecs cmd
            if (audiocodec == "1"):                  # Codec MP3
                config = audio_codec_MP3_01(audiox)
            elif (audiocodec == "2"):               # Codec AC3
                config = audio_codec_AC3_01(abitrate, surround, audiox)
            else:                                  # Codec DTS
                config = audio_codec_DTS_01()

            # Track 02 Codecs cmd
            if (audiotype == "4"):
                if (audiocodec2 == "1"):               # Codec MP3
                    config2 = audio_codec_MP3_02(audiox2)
                elif (audiocodec2 == "2"):            # Codec AC3
                    config2 = audio_codec_AC3_02(abitrate2, surround2, audiox2)
                else:                                # Codec DTS
                    config2 = audio_codec_DTS_02()

        # FFMPEG Audio cmd > MULTi Audio Tracks
        if (audiotype == "4"):
            audio_config = audio_multi_config(audionum, audiolang, config,
                                              audionum2, audiolang2, config2)

        # FFMPEG Audio cmd > Single Audio Track
        elif (audiotype == "1" or audiotype == "2" or audiotype == "3"):
            audio_config = audio_solo_config(audionum, audiolang, config)

    return (audio_config, audiocodec, lang, audiolang, audionum, audionum2)


def RELEASE_FINAL_TITLE(audiocodec, lang, form, xcod, tag, extend):

    if (audiocodec == "3"):                       # Codec DTS
        xcod2 = "DTS"
    elif (audiocodec == "2"):                    # Codec AC3
        xcod2 = "AC3"
    else:                                       # Codec MP3
        xcod2 = ""
    (mark, prezquality) = rls_title_codec(lang, form, xcod, tag, extend, xcod2)
    return (mark, prezquality)


def SUBTITLES_LOCATIONS(subtype):

    # Auto Complete
    def completer(text, state):
        return (
            [entry.replace(' ', '\ ') for entry in os.listdir(
                folder + os.path.dirname(
                    readline.get_line_buffer())
                ) if entry.startswith(text)][state])

    # Set some values
    [idsub, idsub2, charset, charset2, sync,
     sync2, idcharset, idcharset2] = ["", ] * 8

    # MULTI TRACKS
    if (subtype == "3"):

        # Run Auto Complete
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)

        # Ask for Tracks Location
        (idsub, idsub2) = subs_file_multi()

        # Stop Auto Complete
        readline.parse_and_bind("tab: ")

        # Subcharset + Delay
        idcharset = ask_subcharset01()
        idcharset2 = ask_subcharset02()
        (charset, charset2) = subcharset_ANSI(idcharset, idcharset2)
        (sync, sync2) = subdelay_multi()

    # SINGLE TRACK
    else:

        # Run Auto Complete
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)

        # Ask for Track Location
        (idsub, idsub2) = subs_file_solo()

        # Stop Auto Complete
        readline.parse_and_bind("tab: ")

        # Subcharset + Delay
        idcharset = ask_subcharset00()
        (charset, charset2) = subcharset_ANSI(idcharset, idcharset2)
        (sync, sync2) = subdelay_solo()

    return (idsub, idsub2, charset, charset2, sync, sync2)


def SUBTITLES_EXTRACTIONS(subsource, subtype, source, title):

    # EXTRACT from ISO or IMG
    if (subsource == "4"):

        # Multi Tracks > ID + Titles + extract cmd
        if (subtype == "3"):
            (idsub, idsub2) = subs_multi_handbrake_ID()
            (titlesub, titlesub2) = manual_title_subs()
            extract = iso_multi(source, thumb, title,
                                idsub, idsub2)

        # Single Track > ID + Titles + extract cmd
        else:
            (idsub, idsub2) = subs_solo_handbrake_ID()
            (titlesub, titlesub2) = auto_title_sub(subtype)
            extract = iso_solo(source, thumb, title, idsub)

    # EXTRACT from M2TS
    if (subsource == "6"):

        # Multi Tracks > ID + Titles + extract cmd
        if (subtype == "3"):
            (idsub, idsub2) = subs_multi_ffmpeg_ID()
            (titlesub, titlesub2) = manual_title_subs()
            extract = m2ts_multi(thumb, source, idsub,
                                 title, idsub2)

        # Single Track > ID + Titles + extract cmd
        else:
            (idsub, idsub2) = subs_solo_ffmpeg_ID()
            (titlesub, titlesub2) = auto_title_sub(subtype)
            extract = m2ts_solo(thumb, source, idsub, title)

    # EXTRACT from MKV
    if (subsource == "5"):

        # Multi Tracks > ID + Titles + Format ( srt, ass, vobsub ? )
        if (subtype == "3"):
            (idsub, idsub2) = subs_multi_ffmpeg_ID()
            (titlesub, titlesub2) = manual_title_subs()
            (ext, ext2) = subtitles_format(subtype)

            # When PGS - extract cmd
            if (ext == "1" and ext2 == "1"):
                extract = mkv_multi_pgs(thumb, source, idsub,
                                        title, ext, idsub2, ext2)

            # When SRT or ASS or VOBSUB - extract cmd
            else:
                extract = mkv_multi_srt(thumb, source, idsub,
                                        title, ext, idsub2, ext2)

        # Single Track > ID + Titles + Format ( srt, ass, vobsub ? )
        else:
            (idsub, idsub2) = subs_solo_ffmpeg_ID()
            (titlesub, titlesub2) = auto_title_sub(subtype)
            (ext, ext2) = subtitles_format(subtype)

            # When PGS - extract cmd
            if (ext == "1" and ext2 == "1"):
                extract = mkv_solo_pgs(thumb, source, idsub,
                                       title, ext)

            # When SRT or ASS or VOBSUB - extract cmd
            else:
                extract = mkv_solo_srt(thumb, source, idsub,
                                       title, ext)

    return (extract, titlesub, titlesub2)


def SUBTITLES_FROM_SOURCE(audiotype, subtype):

    # Subforced config (INT)
    (forced, stforced) = subforced_config_INT(audiotype, subtype)
    subforced = subforced_nfo(subtype, stforced)

    # Multi Tracks > ID + Titles + ffmpeg cmd
    if (subtype == "3"):
        (idsub, idsub2) = subs_multi_ffmpeg_ID()
        (titlesub, titlesub2) = manual_title_subs()
        sub_config = ffmpeg_multi_subs(idsub, titlesub,
                                       idsub2, titlesub2)

    # Single Track > ID + Titles + ffmpeg cmd
    else:
        (idsub, idsub2) = subs_solo_ffmpeg_ID()
        (titlesub, titlesub2) = auto_title_sub(subtype)
        sub_config = ffmpeg_solo_subs(idsub, titlesub)

    return (forced, stforced, subforced, idsub, idsub2, titlesub, titlesub2)


def MKVMERGE(subtype, audiotype, thumb, title, year, stag, mark,
             extend, sync, titlesub, charset, idsub, forced, sync2,
             titlesub2, charset2, idsub2, subsource):

    # When SUBTITLES from SOURCE ( INT )
    if (subsource == "1"):

        # When MULTI SUBTITLES
        if (subtype == "3"):
            if (audiotype == "4"):                  # When MULTi Audio
                mkvmerge = INT_mA_mS(thumb, title, year, stag, mark,
                                     extend, forced)
            # When Single Audio
            elif (audiotype == "1" or audiotype == "2" or audiotype == "3"):
                mkvmerge = INT_sA_mS(thumb, title, year, stag, mark,
                                     extend, forced)
            else:                           # When NOAUDIO
                mkvmerge = INT_NA_mS(thumb, title, year, stag,
                                     mark, extend, forced)

        # When SINGLE SUBTITLES
        else:
            if (audiotype == "4"):                  # When MULTi Audio
                mkvmerge = INT_mA_sS(thumb, title, year, stag,
                                     mark, extend, forced)
            # When Single Audio
            elif (audiotype == "1" or audiotype == "2" or audiotype == "3"):
                mkvmerge = INT_sA_sS(thumb, title, year, stag,
                                     mark, extend, forced)
            else:                           # When NOAUDIO
                mkvmerge = INT_NA_sS(thumb, title, year, stag, mark,
                                     extend, forced)

    # When SUBTITLES from FILE ( EXT )
    elif (subsource == "3" or subsource == "4" or subsource == "5"
            or subsource == "6"):

        # When MULTI SUBTITLES
        if (subtype == "3"):
            if (audiotype == "4"):                  # When MULTi Audio
                mkvmerge = EXT_mA_mS(thumb, title, year, stag, mark,
                                     extend, sync, titlesub, charset,
                                     idsub, forced, sync2, titlesub2,
                                     charset2, idsub2)
            # When Single Audio
            elif (audiotype == "1" or audiotype == "2" or audiotype == "3"):
                mkvmerge = EXT_sA_mS(thumb, title, year, stag, mark,
                                     extend, sync, titlesub, charset,
                                     idsub, forced, sync2, titlesub2,
                                     charset2, idsub2)
            else:                           # When NOAUDIO
                mkvmerge = EXT_NA_mS(thumb, title, year, stag, mark, extend,
                                     sync, titlesub, charset, idsub, forced,
                                     sync2, titlesub2, charset2, idsub2)

        # When SINGLE SUBTITLES
        else:
            if (audiotype == "4"):               # When MULTi Audio
                mkvmerge = EXT_mA_sS(thumb, title, year, stag, mark,
                                     extend, forced, sync, titlesub,
                                     charset, idsub)
            # When Single Audio
            elif (audiotype == "1" or audiotype == "2" or audiotype == "3"):
                mkvmerge = EXT_sA_sS(thumb, title, year, stag, mark,
                                     extend, forced, sync, titlesub,
                                     charset, idsub)
            else:                           # When NOAUDIO
                mkvmerge = EXT_NA_sS(thumb, title, year, stag, mark, extend,
                                     forced, sync, titlesub, charset, idsub)

    # When NO SUBTITLES ( INT )
    else:
        if (audiotype == "4"):               # When MULTi Audio
            mkvmerge = INT_mA_NA(thumb, title, year, stag, mark, extend)
        # When Single Audio
        elif (audiotype == "1" or audiotype == "2" or audiotype == "3"):
            mkvmerge = INT_sA_NA(thumb, title, year, stag, mark, extend)
        else:                           # When NOAUDIO ( and NOSUBS )
            mkvmerge = ""

    return mkvmerge


def STANDARD_RESOLUTIONS(format, hd_size, crop):

    # When DVDRip
    if (format == "4"):
        reso = DVD(crop)

    # When HDTV
    elif (format == "1"):
        if (hd_size == "1"):
            reso = standard_720p(crop)
        elif (hd_size == "2"):
            reso = standard_1080p(crop)
        else:
            reso = standard_SD()

    # When BluRay
    elif (format == "6"):
        if (hd_size == "1"):
            reso = standard_720p(crop)
        else:
            reso = standard_1080p(crop)

    # When BRRip/BDRip/PDTV
    else:
        reso = standard_SD(crop)

    return reso
