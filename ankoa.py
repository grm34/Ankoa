#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#------------------  AnKoA  -----------------------#
#     Made with love by grm34 (FRIPOUILLEJACK)     #
#     ........fripouillejack@gmail.com .......     #
# Greetz: thibs, Rockweb, c0da, Hydrog3n, Speedy76 #
#--------------------------------------------------#

import os
import sys
import readline
import optparse
import json
import urllib2
import subprocess
from json import loads
from urllib2 import (Request, urlopen, URLError, HTTPError, unquote)
from subprocess import (CalledProcessError, check_output)
from pprint import pprint
sys.path.append("app/")
from style import (banner, next, color)
from bitrate import (calcul, calc)
from settings import option

(folder, thumb, tag, team, announce, tmdb_api_key, tag_thumb) = option()

(BLUE, RED, YELLOW, GREEN, END) = color()

#___ Run ___#
def ffmpeg():
    if (encode_type == "2"):    #-->  CRF
        return (
            "cd "+thumb+" && ffmpeg -i "+source+" -metadata title='"+\
            title+"."+year+"' -metadata proudly.presented.by='"+team+\
            "' -map 0:"+idvideo+interlace+fps+" -metadata:s:v:0 title= "\
            "-metadata:s:v:0 language= -f "+string+reso+" -c:v:0 "+codec+\
            " -crf "+crf+" -level "+level+param+audio_config+sub_config+\
            " -passlogfile "+title+".log "+title+"."+year+stag+mark+sub_remux
        )

    else:                       #-->  2PASS
        return (
            "cd "+thumb+" && ffmpeg -i "+source+" -pass 1 -map 0:"+\
            idvideo+interlace2+fps+" -f "+string+reso+" -c:v:0 "+\
            codec+" -b:v:0 "+bit+"k -level "+level+pass1+" -an -sn "\
            "-passlogfile "+title+".log "+title+"."+year+stag+mark+\
            " && ffmpeg -y -i "+source+" -pass 2 -metadata title='"+title+\
            "."+year+"' -metadata proudly.presented.by='"+team+"' -map 0:"+\
            idvideo+interlace+fps+" -metadata:s:v:0 title= -metadata:s:v:0 "\
            "language= -f "+string+reso+" -c:v:0 "+codec+" -b:v:0 "+bit+"k "\
            "-level "+level+param+audio_config+sub_config+" -passlogfile "+\
            title+".log "+title+"."+year+stag+mark+sub_remux
        )

def data():                     #--> Tools
    if (len(nfoimdb) == 7):
        prezz = "&& ./genprez.py "+audiolang+" "+prezquality+" "+titlesub+\
                " "+prezsize+" "+nfoimdb+" && mv "+thumb+name+\
                "*.txt "+thumb+title+"."+year+stag+mark+".txt "
        zipp = "cd "+thumb+" && zip -r "+title+".zip -m "+title+\
               "."+year+stag+"*.torrent "+title+"."+year+stag+\
               "*.nfo "+title+"."+year+stag+"*.txt "+title+\
               "*.log "+title+"."+year+stag+"*.png"
    else:
        prezz = ""
        zipp = "cd "+thumb+" && zip -r "+title+".zip -m "+title+\
               "."+year+stag+"*.torrent "+title+"."+year+stag+"*.nfo "+\
               title+"*.log "+title+"."+year+stag+"*.png"

    return (
        "./thumbnails.py "+thumb+title+"."+year+stag+mark+" 5 2 "+prezz+\
        "&& ./nfogen.sh "+thumb+title+"."+year+stag+mark+" "+nfosource+\
        " "+titlesub+" "+subforced+" http://www.imdb.com/title/tt"+nfoimdb+\
        " && rm -f "+thumb+title+"*.mbtree && cd "+thumb+" && mktorrent -a "+\
        announce+" -p -t 8 -l "+pieces+" "+title+"."+year+stag+mark+" "+zipp
    )

def main():

    #___ Auto completion ___#
    def completer(text,state):
        return (
            [entry for entry in os.listdir(
                folder+os.path.dirname(readline.get_line_buffer()))
                if entry.startswith(text)][state]
        )

    #___ Source Infos ___#
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)
    prefix = raw_input(GREEN+"RELEASE SOURCE > \n"+END)
    readline.parse_and_bind("tab: ")
    source = folder+prefix
    title = raw_input(GREEN+"RELEASE TITLE "+YELLOW+\
                      "(ex: Hudson.Hawk)"+GREEN+" : "+END)
    year = raw_input(GREEN+"RELEASE PRODUCTION YEAR : "+END)
    special = raw_input(GREEN+"SPECIAL TAG "+YELLOW+\
                        "(ex: EXTENDED.CUT)"+GREEN+" : "+END)
    scan = [
        "HandBrakeCLI -t 0 --scan -i "+source,\
        "mediainfo -f --Inform='General;%Duration/String3%' "+source,\
        "mediainfo -f --Inform='General;%FileSize/String4%' "+source,\
        "mediainfo -f --Inform='Video;%BitRate/String%' "+source,\
        "mediainfo -f --Inform='Video;%FrameRate/String%' "+source,\
        "mediainfo -f --Inform='Video;%Width/String%' "+source,\
        "mediainfo -f --Inform='Video;%Height/String%' "+source,\
        "mediainfo -f --Inform='Video;%DisplayAspectRatio/"\
            "String%' "+source,\
        "mediainfo -f --Inform='Audio;%CodecID% - ' "+source,\
        "mediainfo -f --Inform='Audio;%Language/String% - ' "+source,\
        "mediainfo -f --Inform='Audio;%BitRate/String% - ' "+source,\
        "mediainfo -f --Inform='Audio;%SamplingRate/String% - ' "+source,\
        "mediainfo -f --Inform='Audio;%Channel(s)/String% - ' "+source,\
        "mediainfo -f --Inform='Text;%CodecID% - ' "+source,\
        "mediainfo -f --Inform='Text;%Language/String% - ' "+source
    ]
    type = raw_input(GREEN+"SCAN INFOS SOURCE > \n"+YELLOW+\
                     "HANDBRAKE "+GREEN+"[1]"+YELLOW+" - MEDIAINFO "+GREEN+\
                     "[2] : "+END)
    try:
        if (type == "1"):
            subprocess.check_output(scan[0], shell=True)
        else:
            subprocess.check_output(scan[1], shell=True)
            for x in range(1, 15):
                os.system(scan[x])
                x = x + 1
    except (OSError, CalledProcessError):
        print (GREEN+"\n -> "+BLUE+"ERROR : "+RED+"Bad source selection"\
               ", please try again !\n"+END)
        sys.exit()

    #___ Video Params ___#
    codec_type = raw_input(GREEN+"VIDEO CODEC > \n"+YELLOW+"x264 "+GREEN+\
                           "[1]"+YELLOW+" - x265 "+GREEN+"[2] : "+END)
    if (codec_type == "2"):
        codec = "libx265"
    else:
        codec = "libx264"

    encode_type = raw_input(GREEN+"ENCODING MODE > \n"+YELLOW+\
                            "DUALPASS "+GREEN+"[1]"+YELLOW+\
                            " - CRF "+GREEN+"[2] : "+END)
    if (encode_type == "2"):
        bit = ""
        crf = raw_input(GREEN+"CRF LEVEL "+YELLOW+"(ex: 19)"+GREEN+" : "+END)
    else:
        crf = ""
        calculator = raw_input(GREEN+"BITRATE CALCULATOR "+YELLOW+\
                               "(y/n)"+GREEN+" : "+END)
        if (calculator == "y"):
            next = "y"
            while (next != "n"):
                HH, MM, SS, audiobit, rls_size, calsize = calcul()
                run_calc = calc(HH, MM, SS, audiobit, rls_size, calsize)
                os.system(run_calc)
                next = raw_input(GREEN+"TRY AGAIN "+YELLOW+\
                                 "(y/n)"+GREEN+" : "+END)
            bit = raw_input(GREEN+"VIDEO BITRATE Kbps : "+END)
        else:
            bit = raw_input(GREEN+"VIDEO BITRATE Kbps : "+END)

    format = raw_input(GREEN+"RELEASE FORMAT > \n"+YELLOW+"HDTV "+GREEN+\
                       "[1]"+YELLOW+" - PDTV "+GREEN+"[2]"+YELLOW+\
                       " - BDRip "+GREEN+"[3]\n"+YELLOW+"DVDRip "+GREEN+\
                       "[4]"+YELLOW+" - BRRip "+GREEN+"[5]"+YELLOW+\
                       " - 720p "+GREEN+"[6] : "+END)
    if (format == "2"):
        hr = raw_input(GREEN+"PDTV HIGH RESOLUTION "+YELLOW+\
                       "(y/n)"+GREEN+" : "+END)
        if (hr == "y"):
            format = "0"+format

    rlstype = raw_input(GREEN+"RELEASE CONTAINER > \n"+YELLOW+\
                        "MPEG4 "+GREEN+"[1]"+YELLOW+" - MATROSKA "+GREEN+\
                        "[2] : "+END)
    if (rlstype == "1"):
        string = "mp4"
    else:
        string = "matroska"

    scan2 = raw_input(GREEN+"FFMPEG SCAN TRACKS "+YELLOW+\
                      "(y/n)"+GREEN+" : "+END)
    ffmpeg = "ffmpeg -i "+source
    if (scan2 == "y"):
        os.system(ffmpeg)

    idvideo = raw_input(GREEN+"VIDEO TRACK FFMPEG ID "+YELLOW+\
                        "(ex: 0)"+GREEN+" : "+END)
    modif_fps = raw_input(GREEN+"CHANGE VIDEO FRAMERATE "+YELLOW+\
                          "(y/n)"+GREEN+" : "+END)
    if (modif_fps == "y"):
        set_fps = raw_input(GREEN+"VIDEO FRAMERATE "+YELLOW+\
                            "(ex: 23.98)"+GREEN+" : "+END)
        fps = "-r "+set_fps+" "
    else:
        fps = ""

    deinterlace = raw_input(GREEN+"DEINTERLACE VIDEO "+YELLOW+\
                            "(y/n)"+GREEN+" : "+END)
    if (deinterlace == "y"):
        interlace = " -filter:v yadif=deint=0 "
        if (encode_type == "2"):
            interlace2 = ""
        else:
            interlace2 = " -filter:v yadif=deint=1 "
    else:
        interlace = ""
        interlace2 = ""

    #___ Audio Infos ___#
    audiotype = raw_input(GREEN+"RELEASE AUDIO TYPE > \n"+YELLOW+\
                          "FRENCH "+GREEN+"[1]"+YELLOW+" - ENGLiSH "+GREEN+\
                          "[2]\n"+YELLOW+"OTHER "+GREEN+"[3]"+YELLOW+" - "\
                          "MULTi "+GREEN+"[4]"+YELLOW+" - NONE "+GREEN+\
                          "[5] : "+END)
    if (audiotype == "1" or audiotype == "2" or audiotype == "3"):
        audionum = raw_input(GREEN+"AUDIO TRACK FFMPEG ID "+YELLOW+\
                             "(ex: 1)"+GREEN+" : "+END)
        if (audiotype == "3"):
            audiolang = raw_input(GREEN+"AUDIO TRACK TITLE "+YELLOW+\
                                  "(ex: Espagnol)"+GREEN+" : "+END)
        audiocodec = raw_input(GREEN+"AUDIO TRACK CODEC > \n"+YELLOW+\
                               "MP3 "+GREEN+"[1]"+YELLOW+" - AC3 "+GREEN+\
                               "[2]"+YELLOW+" - DTS/COPY "+GREEN+"[3] : "+END)
        if (audiocodec == "2"):
            abitrate = raw_input(GREEN+"AUDIO TRACK BITRATE Kbps "+YELLOW+\
                                 "(ex: 448)"+GREEN+" : "+END)
            surround = raw_input(GREEN+"AUDIO TRACK CHANNELS "+YELLOW+\
                                 "(ex: 2)"+GREEN+" : "+END)
    elif (audiotype == "4"):
        audionum = raw_input(GREEN+"AUDIO TRACK 01 FFMPEG ID "+YELLOW+\
                             "(ex: 1)"+GREEN+" : "+END)
        audiolang = raw_input(GREEN+"AUDIO TRACK 01 TITLE "+YELLOW+\
                              "(ex: English)"+GREEN+" : "+END)
        audiocodec = raw_input(GREEN+"AUDIO TRACK 01 CODEC > \n"+YELLOW+\
                               "MP3 "+GREEN+"[1]"+YELLOW+" - AC3 "+GREEN+\
                               "[2]"+YELLOW+" - DTS/COPY "+GREEN+"[3] : "+END)
        if (audiocodec == "2"):
            abitrate = raw_input(GREEN+"AUDIO TRACK 01 BITRATE Kbps "+YELLOW+\
                                 "(ex: 448)"+GREEN+" : "+END)
            surround = raw_input(GREEN+"AUDIO TRACK 01 CHANNELS "+YELLOW+\
                                 "(ex: 2)"+GREEN+" : "+END)
        audionum2 = raw_input(GREEN+"AUDIO TRACK 02 FFMPEG ID "+YELLOW+\
                              "(ex: 0)"+GREEN+" : "+END)
        audiolang2 = raw_input(GREEN+"AUDIO TRACK 02 TITLE "+YELLOW+\
                               "(ex: English)"+GREEN+" : "+END)
        audiocodec2 = raw_input(GREEN+"AUDIO TRACK 02 CODEC > \n"+YELLOW+\
                                "MP3 "+GREEN+"[1]"+YELLOW+" - AC3 "+GREEN+\
                                "[2]"+YELLOW+" - DTS/COPY "+GREEN+\
                                "[3] : "+END)
        if (audiocodec2 == "2"):
            abitrate2 = raw_input(GREEN+"AUDIO TRACK 02 BITRATE "\
                                  "Kbps "+YELLOW+"(ex: 448)"+GREEN+" : "+END)
            surround2 = raw_input(GREEN+"AUDIO TRACK 02 CHANNELS"\
                                  " "+YELLOW+"(ex: 2)"+GREEN+" : "+END)
    else:
        audiocodec = ""
    if (audiotype == "1" or audiotype == "2"
            or audiotype == "3" or audiotype == "4"):
        audiox_ = raw_input(GREEN+"CHANGE SAMPLING RATE "+YELLOW+\
                            "(y/n)"+GREEN+" : "+END)
        if (audiox_ == "y"):
            if (audiotype == "4"):
                ar1_ = raw_input(GREEN+"AUDIO TRACK 01 SAMPLING "\
                                 "RATE "+YELLOW+"(ex: 48)"+GREEN+" : "+END)
                if not (ar1_):
                    ar1 = " -ar:a:0 48k"
                else:
                    ar1 = " -ar:a:0 "+ar1_+"k"
                ar2 = raw_input(GREEN+"AUDIO TRACK 02 SAMPLING RATE "+YELLOW+\
                                "(ex: 48)"+GREEN+" : "+END)
                if not (ar2_):
                    ar2 = " -ar:a:1 48k"
                else:
                    ar2 = " -ar:a:1 "+ar2_+"k"
                audiox = ar1
                audiox2 = ar2
            else:
                ar_ = raw_input(GREEN+"AUDIO TRACK 01 SAMPLING RATE "+YELLOW+\
                                "(ex: 48)"+GREEN+" : "+END)
                if not (ar_):
                    ar = " -ar:a:0 48k"
                else:
                    ar = " -ar:a:0 "+ar_+"k"
                audiox = ar
                audiox2 = ""
        else:
            audiox = " -ar:a:0 48k"
            audiox2 = " -ar:a:1 48k"

    #___ Audio Params ___#
    if (audiocodec == "1"):
        config = "-c:a:0 mp3 -b:a:0 128k -ac:a:0 2"+audiox
    elif (audiocodec == "2"):
        config = "-c:a:0 ac3 -b:a:0 "+abitrate+"k -ac:a:0 "+surround+audiox
    else:
        config = "-c:a:0 copy"

    if (audiotype == "4"):
        if (audiocodec2 == "1"):
            config2 = "-c:a:1 mp3 -b:a:1 128k -ac:a:1 2"+audiox2
        elif (audiocodec2 == "2"):
            config2 = "-c:a:1 ac3 -b:a:1 "+abitrate2+\
                      "k -ac:a:1 "+surround2+audiox2
        else:
            config2 = "-c:a:1 copy"

    if (audiotype == "1"):
        lang = "FRENCH"
        audiolang = "FRENCH"
    elif (audiotype == "2"):
        lang = "VOSTFR"
        audiolang = "ENGLiSH"
    elif (audiotype == "3"):
        lang = "VOSTFR"
    elif (audiotype == "4"):
        lang = "MULTi"
    else:
        lang = "NOAUDIO"
        audiolang = "NOAUDIO"

    if (audiotype == "4"):
        audio_config = " -map 0:"+audionum+" -metadata:s:a:0 title='"+\
                       audiolang+"' -metadata:s:a:0 language= "+config+\
                       " -map 0:"+audionum2+" -metadata:s:a:1 title='"+\
                       audiolang2+"' -metadata:s:a:1 language= "+config2

    elif (audiotype == "1" or audiotype == "2" or audiotype == "3"):
        audio_config = " -map 0:"+audionum+" -metadata:s:a:0 title='"+\
                       audiolang+"' -metadata:s:a:0 language= "+config
    else:
        audio_config = ""

    #___ Release Tag ___#
    if (special == ""):
        stag = ""
    else:
        stag = "."+special

    if (format == "1"):
        form = "HDTV"
    elif (format == "2"):
        form = "PDTV"
    elif (format == "02"):
        form = "HR.PDTV"
    elif (format == "3"):
        form = "BDRip"
    elif (format == "4"):
        form = "DVDRip"
    elif (format == "6"):
        form = "720p.BluRay"
    else:
        form = "BRRip"

    if (rlstype == "1"):
        extend = ".mp4"
    else:
        extend = ".mkv"
    if (codec_type == "2"):
        x = "x265"
    else:
        x = "x264"

    if (audiocodec == "1"):
        mark = "."+lang+"."+form+"."+x+"-"+tag+extend
        prezquality = form+" "+x
    elif (audiocodec == "3"):
        mark = "."+lang+"."+form+".DTS"+"."+x+"-"+tag+extend
        prezquality = form+" DTS."+x
    else:
        mark = "."+lang+"."+form+".AC3"+"."+x+"-"+tag+extend
        prezquality = form+" AC3."+x

    #___ Mkvmerge ___#
    def remux_ext():
        if (subtype == "3"):
            if (audiotype == "4"):  #--> FILE - Audio MULTi / SRT MULTi
                return (
                    " && mv "+thumb+title+"."+year+stag+mark+" "+thumb+\
                    title+extend+" && mkvmerge -o "+thumb+title+"."+year+\
                    stag+mark+" --compression -1:none --default-track 0:yes "\
                    "--forced-track 0:no --default-track 1:yes "\
                    "--forced-track 1:no --default-track 2:no "\
                    "--forced-track 2:no "+thumb+title+extend+\
                    " --default-track '0:yes' --forced-track '0:no'"\
                    " --language '0:und' "+sync+"--track-name '0:"+titlesub+\
                    "'"+charset+" "+idsub+" --default-track '0:no' "+forced+\
                    "--language '0:und' "+sync2+"--track-name '0:"+titlesub2+\
                    "'"+charset2+" "+idsub2+" && rm -f "+thumb+title+extend
                )

            else:                   #--> FILE - Audio FR-VO / SRT MULTi
                return (
                    " && mv "+thumb+title+"."+year+stag+mark+" "+thumb+\
                    title+extend+" && mkvmerge -o "+thumb+title+"."+year+\
                    stag+mark+" --compression -1:none --default-track 0:yes "\
                    "--forced-track 0:no --default-track 1:yes "\
                    "--forced-track 1:no "+thumb+title+extend+\
                    " --default-track '0:yes' --forced-track '0:no' "\
                    "--language '0:und' "+sync+"--track-name '0:"+titlesub+\
                    "'"+charset+" "+idsub+" --default-track '0:no' "+forced+\
                    "--language '0:und' "+sync2+"--track-name '0:"+titlesub2+\
                    "'"+charset2+" "+idsub2+" && rm -f "+thumb+title+extend
                )

        else:
            if (audiotype == "4"):  #--> FILE - Audio MULTi / SRT FR-VO
                return (
                    " && mv "+thumb+title+"."+year+stag+mark+" "+thumb+title+\
                    extend+" && mkvmerge -o "+thumb+title+"."+year+stag+mark+\
                    " --compression -1:none --default-track 0:yes "\
                    "--forced-track 0:no --default-track 1:yes "\
                    "--forced-track 1:no --default-track 2:no --forced-track"\
                    " 2:no "+thumb+title+extend+" --default-track '0:yes' "+\
                    forced+"--language '0:und' "+sync+"--track-name '0:"+\
                    titlesub+"'"+charset+" "+idsub+" && rm -f "+thumb+\
                    title+extend
                )

            else:                   #--> FILE - Audio FR-VO / SRT FR-VO
                return (
                    " && mv "+thumb+title+"."+year+stag+mark+" "+thumb+title+\
                    extend+" && mkvmerge -o "+thumb+title+"."+year+stag+mark+\
                    " --compression -1:none --default-track 0:yes "\
                    "--forced-track 0:no --default-track 1:yes "\
                    "--forced-track 1:no "+thumb+title+extend+" "\
                    "--default-track '0:yes' "+forced+"--language '0:und' "+\
                    sync+"--track-name '0:"+titlesub+"'"+charset+" "+idsub+\
                    " && rm -f "+thumb+title+extend
                )

    def remux_int():
        if (subtype == "3"):
            if (audiotype == "4"):  #--> SOURCE - Audio MULTi / SRT MULTi
                return (
                    " && mv "+thumb+title+"."+year+stag+mark+" "+thumb+title+\
                    extend+" && mkvmerge -o "+thumb+title+"."+year+stag+mark+\
                    " --compression -1:none --default-track 0:yes "\
                    "--forced-track 0:no --default-track 1:yes "\
                    "--forced-track 1:no --default-track 2:no "\
                    "--forced-track 2:no --default-track 3:yes "\
                    "--forced-track 3:no --default-track 4:no "+\
                    forced+thumb+title+extend+" && rm -f "+thumb+title+extend
                )

            else:                   #--> SOURCE - Audio FR/VO / SRT MULTi
                return (
                    " && mv "+thumb+title+"."+year+stag+mark+" "+thumb+title+\
                    extend+" && mkvmerge -o "+thumb+title+"."+year+stag+mark+\
                    " --compression -1:none --default-track 0:yes "\
                    "--forced-track 0:no --default-track 1:yes "\
                    "--forced-track 1:no --default-track 2:yes "\
                    "--forced-track 2:no --default-track 3:no "+forced+\
                    thumb+title+extend+" && rm -f "+thumb+title+extend
                )
        else:
            if (audiotype == "4"):  #--> SOURCE - Audio MULTi / SRT FR/VO
                return (
                    " && mv "+thumb+title+"."+year+stag+mark+" "+thumb+title+\
                    extend+" && mkvmerge -o "+thumb+title+"."+year+stag+mark+\
                    " --compression -1:none --default-track 0:yes "\
                    "--forced-track 0:no --default-track 1:yes "\
                    "--forced-track 1:no --default-track 2:no "\
                    "--forced-track 2:no --default-track 3:yes "+forced+\
                    thumb+title+extend+" && rm -f "+thumb+title+extend
                )

            else:                   #--> SOURCE - Audio FR/VO / SRT FR/VO
                return (
                    " && mv "+thumb+title+"."+year+stag+mark+" "+thumb+title+\
                    extend+" && mkvmerge -o "+thumb+title+"."+year+stag+mark+\
                    " --compression -1:none --default-track 0:yes "\
                    "--forced-track 0:no --default-track 1:yes "\
                    "--forced-track 1:no --default-track 2:yes "+forced+\
                    thumb+title+extend+" && rm -f "+thumb+title+extend
                )

    #___ Subtitles Params ___#
    def infos_subs_in():
        if (subtype == "3"):
            if (subsource == "4"):
                idsub = raw_input(GREEN+"SUBTITLES TRACK 01 ISO ID "+YELLOW+\
                                  "(ex: 1)"+GREEN+" : "+END)
                idsub2 = raw_input(GREEN+"SUBTITLES TRACK 02 ISO ID "+YELLOW+\
                                   "(ex: 2)"+GREEN+" : "+END)
            else:
                idsub = raw_input(GREEN+"SUBTITLES TRACK 01 FFMPEG ID "+\
                                  YELLOW+"(ex: 1)"+GREEN+" : "+END)
                idsub2 = raw_input(GREEN+"SUBTITLES TRACK 02 FFMPEG ID "+\
                                   YELLOW+"(ex: 2)"+GREEN+" : "+END)
            titlesub = raw_input(GREEN+"SUBTITLES TRACK 01 TITLE "+YELLOW+\
                                 "(ex: Full.French)"+GREEN+" : "+END)
            titlesub2 = raw_input(GREEN+"SUBTITLES TRACK 02 TITLE "+YELLOW+\
                                  "(ex: French.Forced)"+GREEN+" : "+END)

        else:
            if (subsource == "4"):
                idsub = raw_input(GREEN+"SUBTITLES TRACK ISO ID "+YELLOW+\
                                  "(ex: 1)"+GREEN+" : "+END)
            else:
                idsub = raw_input(GREEN+"SUBTITLES TRACK FFMPEG ID "+YELLOW+\
                                  "(ex: 1)"+GREEN+" : "+END)
            if (subtype == "1"):
                titlesub = "FULL.FRENCH"
            elif (subtype == "2"):
                titlesub = "FRENCH.FORCED"
            idsub2 = ""
            titlesub2 = ""

        infos_subs_in = (idsub, titlesub, idsub2, titlesub2)
        return (infos_subs_in)

    def infos_subs_out():
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)

        if (subtype == "3"):
            ub = raw_input(GREEN+"SUBTITLES TRACK 01 SOURCE > \n"+END)
            ub2 = raw_input(GREEN+"SUBTITLES TRACK 02 SOURCE > \n"+END)
            readline.parse_and_bind("tab: ")
            idsub = folder+ub
            idsub2 = folder+ub2
            if (subsource == "3"):
                titlesub = raw_input(GREEN+"SUBTITLES TRACK 01 TITLE  "+\
                                     YELLOW+"(ex: Full.French)"+GREEN+\
                                     " : "+END)
                titlesub2 = raw_input(GREEN+"SUBTITLES TRACK 02 TITLE  "+\
                                      YELLOW+"(ex: French.Forced)"+GREEN+\
                                      " : "+END)
        else:
            ub = raw_input(GREEN+"SUBTITLES TRACK SOURCE > \n"+END)
            readline.parse_and_bind("tab: ")
            idsub = folder+ub
            if (subtype == "1"):
                titlesub = "FULL.FRENCH"
            elif (subtype == "2"):
                titlesub = "FRENCH.FORCED"
            idsub2 = ""
            titlesub2 = ""

        if (subtype == "3"):
            idcharset = raw_input(GREEN+"SUBTITLES 01 CHARSET ANSI "+YELLOW+\
                                  "(y/n)"+GREEN+" : "+END)
            idcharset2 = raw_input(GREEN+"SUBTITLES 02 CHARSET ANSI "+YELLOW+\
                                   "(y/n)"+GREEN+" : "+END)
        else:
            idcharset = raw_input(GREEN+"SUBTITLES CHARSET ANSI "+YELLOW+\
                                  "(y/n)"+GREEN+" : "+END)

        if (idcharset == "y"):
            charset = " --sub-charset '0:cp1252'"
        else:
            charset = ""

        if (subtype == "3"):
            if idcharset2 == "y":
                charset2 = " --sub-charset '0:cp1252'"
        else:
            charset2 = ""

        subsync = raw_input(GREEN+"SUBTITLES DELAY "+YELLOW+\
                            "(y/n)"+GREEN+" : "+END)
        if (subsync == "y"):
            if (subtype == "3"):
                subdelay1 = raw_input(GREEN+"SUBTITLES 01 DELAY "+YELLOW+\
                                      "(ex: -200)"+GREEN+" : "+END)
                subdelay2 = raw_input(GREEN+"SUBTITLES 02 DELAY "+YELLOW+\
                                      "(ex: -200)"+GREEN+" : "+END)
                sync = "--sync 0:"+subdelay1+" "
                sync2 = "--sync 0:"+subdelay2+" "
            else:
                subdelay = raw_input(GREEN+"SUBTITLES DELAY "+YELLOW+\
                                     "(ex: -200)"+GREEN+" : "+END)
                sync = "--sync 0:"+subdelay+" "
                sync2 = ""
        else:
            sync = ""
            sync2 = ""

        infos_subs_out = (idsub, titlesub, idsub2, titlesub2,
                          charset, charset2, sync, sync2)
        return (infos_subs_out)

    #___ Subtitles Extract ___#
    def iso_extract():
        if (subtype == "3"):    #-->  EXTRACT ISO MULTi Subs
            return (
                "sudo mount -o loop -t iso9660 "+source+" /media/ && cd "+\
                thumb+" && mencoder -dvd-device /media/ dvd://1 -vobsubout "+\
                title+"1 -vobsuboutindex 0 -sid "+idsub+\
                " -o /dev/null -nosound "\
                "-ovc frameno && mencoder -dvd-device /media/ dvd://1"\
                " -vobsubout "+title+"2 -vobsuboutindex 0 -sid "+idsub2+\
                " -o /dev/null -nosound -ovc frameno && sudo umount -f"\
                " /media*"
            )

        else:                   #-->  EXTRACT ISO FR/VO Subs
            return (
                "sudo mount -o loop -t iso9660 "+source+" /media/ && cd "+\
                thumb+" && mencoder -dvd-device /media/ dvd://1 -vobsubout "+\
                title+" -vobsuboutindex 0 -sid "+idsub+\
                " -o /dev/null -nosound "\
                "-ovc frameno && sudo umount -f /media*"
            )

    def m2ts_extract():
        if (subtype == "3"):    #-->  EXTRACT M2TS MULTi Subs
            return (
                "cd "+thumb+" && ffmpeg -i "+source+" -vn -an -map 0:"+idsub+\
                " -scodec copy "+title+"1.mkv && ffmpeg -i "+source+\
                " -vn -an -map 0:"+idsub2+" -scodec copy "+title+\
                "2.mkv && mkvextract tracks "+title+"1.mkv 0:"\
                +title+"1.pgs && mkvextract tracks "+title+"2.mkv 0:"+title+\
                "2.pgs && mv "+title+"1.pgs "+title+"1.sup && mv "+title+\
                "2.pgs "+title+"2.sup && rm -f "+title+"1.mkv && "\
                "rm -f "+title+"2.mkv"
            )

        else:                   #-->  EXTRACT M2TS FR/VO Subs
            return (
                "cd "+thumb+" && ffmpeg -i "+source+" -vn -an -map 0:"+idsub+\
                " -scodec copy "+title+".mkv && mkvextract tracks "+title+\
                ".mkv 0:"+title+".pgs && mv "+title+".pgs "+title+\
                ".sup && rm -f "+title+".mkv"
            )

    def mkv_format():
        if (subtype == "3"):
            ext = raw_input(GREEN+"SUBTITLES 01 FORMAT > \n"+YELLOW+"PGS "+\
                            GREEN+"[1]"+YELLOW+" - VOBSUB "+GREEN+"[2]"+\
                            YELLOW+" - ASS "+GREEN+"[3]"+YELLOW+" - SRT "+\
                            GREEN+"[4] : "+END)
            ext2 = raw_input(GREEN+"SUBTITLES 02 FORMAT > \n"+YELLOW+\
                             "PGS "+GREEN+"[1]"+YELLOW+" - VOBSUB "+GREEN+\
                             "[2]"+YELLOW+" - ASS "+GREEN+"[3]"+YELLOW+\
                             " - SRT "+GREEN+"[4] : "+END)
        else:
            ext = raw_input(GREEN+"SUBTITLES FORMAT > \n"+YELLOW+\
                            "PGS "+GREEN+"[1]"+YELLOW+" - VOBSUB "+GREEN+\
                            "[2]"+YELLOW+" - ASS "+GREEN+"[3]"+YELLOW+\
                            " - SRT "+GREEN+"[4] : "+END)
            ext2 = ""

        if (ext == "1"):
            ext = ".pgs"
        elif (ext == "2"):
            ext = ".vobsub"
        elif (ext == "3"):
            ext = ".ass"
        else:
            ext = ".srt"
        if (ext2 == "1"):
            ext2 = ".pgs"
        elif (ext2 == "2"):
            ext2 = ".vobsub"
        elif (ext2 == "3"):
            ext2 = ".ass"
        elif (ext2 == "4"):
            ext2 = ".srt"
        else:
            ext2 == ""

        subext = (ext, ext2)
        return (subext)

    def mkv_extract():
        if (subtype == "3"):
            if (ext == "1"):
                if (ext2 == "1"):   #-->  MULTi PGS from MKV
                    return (
                        "cd "+thumb+" && mkvextract tracks "+\
                        source+" "+idsub+":"+title+\
                        "1"+ext+" && mkvextract tracks "+source+" "+idsub2+\
                        ":"+title+"2"+ext2+" && mv "+title+"1"+ext+\
                        " "+title+"1.sup && mv "+title+"2"+ext2+\
                        " "+title+"2.sup"
                    )

            else:                   #-->  MULTi SRT/ASS/VOBSUB from MKV
                return (
                    "cd "+thumb+" && mkvextract tracks "+\
                    source+" "+idsub+":"+title+"1"+ext+\
                    " && mkvextract tracks "+source+" "+idsub2+\
                    ":"+title+"2"+ext2
                )
        else:
            if (ext == "1"):        #-->  FR/VO PGS from MKV
                return (
                    "cd "+thumb+" && mkvextract tracks "+\
                    source+" "+idsub+":"+title+ext+\
                    " && mv "+title+"1"+ext+" "+title+"1.sup"
                )

            else:                   #-->  FR/VO SRT/ASS/VOBSUB from MKV
                return (
                    "cd "+thumb+" && mkvextract tracks "+\
                    source+" "+idsub+":"+title+ext)

    def internal_subs():
        if (subtype == "3"):        #-->  CONFIG MULTI Subs from SOURCE
            sub_config = " -map 0:"+idsub+" -metadata:s:s:0 title='"+\
                         titlesub+"' -metadata:s:s:0 language= -c:s:0 srt "\
                         "-map 0:"+idsub2+" -metadata:s:s:1 title='"+\
                         titlesub2+"' -metadata:s:s:1 language= -c:s:1 srt"

        else:                       #-->  CONFIG FR/VO Subs from SOURCE
            sub_config = " -map 0:"+idsub+" -metadata:s:s:0 title='"+\
                         titlesub+"' -metadata:s:s:0 language= -c:s:0 srt"
        return (sub_config)

    subsource = raw_input(GREEN+"SUBTITLES FROM > \n"+YELLOW+"SOURCE "+GREEN+\
                          "[1]"+YELLOW+" - NONE "+GREEN+"[2]"+YELLOW+\
                          " - FILE "+GREEN+"[3]\n"+YELLOW+"ISO/IMG "+GREEN+\
                          "[4]"+YELLOW+" - MKV "+GREEN+"[5]"+YELLOW+\
                          " - M2TS "+GREEN+"[6] : "+END)

    if (subsource == "1" or subsource == "3" or subsource == "4"
            or subsource == "5" or subsource == "6"):
        subtype = raw_input(GREEN+"SUBTITLES TYPE > \n"+YELLOW+"FR "+GREEN+\
                            "[1]"+YELLOW+" - FORCED "+GREEN+"[2]"+YELLOW+\
                            " - MULTi "+GREEN+"[3] : "+END)
        if (subsource == "1"):
            if (audiotype == "4"):
                if (subtype == "1"):
                    forced = "--forced-track 3:no "
                elif (subtype == "2"):
                    forced = "--forced-track 3:yes "
                else:
                    stforced = raw_input(GREEN+"USE FORCED TRACK "+YELLOW+\
                                         "(y/n)"+GREEN+" : "+END)
                    if (stforced == "y"):
                        forced = "--forced-track 4:yes "
                    else:
                        forced = "--forced-track 4:no "
            else:
                if (subtype == "1"):
                    forced = "--forced-track 2:no "
                elif (subtype == "2"):
                    forced = "--forced-track 2:yes "
                else:
                    stforced = raw_input(GREEN+"USE FORCED TRACK "+YELLOW+\
                                         "(y/n)"+GREEN+" : "+END)
                    if (stforced == "y"):
                        forced = "--forced-track 3:yes "
                    else:
                        forced = "--forced-track 3:no "
        elif (subsource == "3" or subsource == "4"
                or subsource == "5" or subsource == "6"):
            if (subtype == "1"):
                forced = "--forced-track '0:no' "
            elif (subtype == "2"):
                forced = "--forced-track '0:yes' "
            else:
                stforced = raw_input(GREEN+"USE FORCED TRACK "+YELLOW+\
                                     "(y/n)"+GREEN+" : "+END)
                if (stforced == "y"):
                    forced = "--forced-track '0:yes' "
                else:
                    forced = "--forced-track '0:no' "
        if (subtype == "3"):
            if (stforced == "y"):
                subforced = "YES"
            else:
                subforced = "N/A"
        elif (subtype == "2"):
            subforced = "YES"
        else:
            subforced = "N/A"

        #___ Subtitles Process ___#
        def subextract_message():
            print (
                RED+"\n ->"+GREEN+" EXTRACTION DONE, CHECK RESULT FOLDER "\
                "& RUN OCR IF NEEDED !"+RED+"\n ->"+GREEN+\
                " WARNING > PUT FINAL SRT IN SOURCE "\
                "FOLDER FOR NEXT STEP !\n"+END
            )
        if (subsource == "1"):              #-->  SOURCE
            (idsub, titlesub, idsub2, titlesub2) = infos_subs_in()
            sub_config = internal_subs()
            sub_remux = remux_int()

        elif (subsource == "4"):            #-->  ISO
            (idsub, titlesub, idsub2, titlesub2) = infos_subs_in()
            extract_iso = iso_extract()
            os.system(extract_iso)
            subextract_message()

            (
                idsub, titlesub, idsub2, titlesub2,
                charset, charset2, sync, sync2
            ) = infos_subs_out()

            sub_config = ""
            sub_remux = remux_ext()

        elif (subsource == "5"):            #-->  MKV
            (idsub, titlesub, idsub2, titlesub2) = infos_subs_in()
            (ext, ext2) = mkv_format()
            extract_mkv = mkv_extract()
            os.system(extract_mkv)
            subextract_message()

            (
                idsub, titlesub, idsub2, titlesub2,
                charset, charset2, sync, sync2
            ) = infos_subs_out()

            sub_config = ""
            sub_remux = remux_ext()

        elif (subsource == "6"):            #-->  M2TS
            (idsub, titlesub, idsub2, titlesub2) = infos_subs_in()
            extract_m2ts = m2ts_extract()
            os.system(extract_m2ts)
            subextract_message()

            (
                idsub, titlesub, idsub2, titlesub2,
                charset, charset2, sync, sync2
            ) = infos_subs_out()

            sub_config = ""
            sub_remux = remux_ext()

        else:                               #-->  FILE
            (
                idsub, titlesub, idsub2, titlesub2,
                charset, charset2, sync, sync2
            ) = infos_subs_out()

            sub_config = ""
            sub_remux = remux_ext()

    else:
        sub_config = ""
        sub_remux = ""
        titlesub = "N/A"
        subforced = "N/A"

     #___ Aspect Ratio ___#
    def custom():
        W = raw_input(GREEN+"RESOLUTION WIDTH : "+END)
        H = raw_input(GREEN+"RESOLUTION HEIGHT : "+END)
        reso = " -s "+W+"x"+H+crop
        return (reso)

    def DVD():
        ask_sar = raw_input(GREEN+"USE SAMPLE ASPECT RATIO "+YELLOW+\
                            "(y/n)"+GREEN+" : "+END)
        if (ask_sar == "y"):
            sar = raw_input(GREEN+"SOURCE ASPECT RATIO > \n"+YELLOW+\
                            "PAL 16:9 "+GREEN+"[1]"+YELLOW+" - PAL 4:3 "+\
                            GREEN+"[2]\n"+YELLOW+"NTSC 16:9 "+GREEN+\
                            "[3]"+YELLOW+" - NTSC 4:3 "+GREEN+"[4] : "+END)
            if (sar == "1"):
                reso = " -sar 64:45"+crop
            elif (sar == "2"):
                reso = " -sar 16:15"+crop
            elif (sar == "3"):
                reso = " -sar 32:27"+crop
            elif (sar == "4"):
                reso = " -sar 8:9"+crop
            else:
                reso = custom()
        else:
            reso = custom()
        return (reso)

    def BLURAY():
        perso = raw_input(GREEN+"CUSTOM RESOLUTION "+YELLOW+\
                          "(y/n)"+GREEN+" : "+END)
        if (perso == "y"):
            reso = custom()
        else:
            ratio = raw_input(GREEN+"RELEASE ASPECT RATIO > \n"+YELLOW+\
                              "1.33 - 1.66 - 1.78 - 1.85 - 2.35 - 2.40"+\
                              GREEN+" : "+END)
            if (ratio == "2.40"):
                reso = " -s 720x300"+crop
            elif (ratio == "2.35"):
                reso = " -s 720x306"+crop
            elif (ratio == "1.85"):
                reso = " -s 720x390"+crop
            elif (ratio == "1.78"):
                reso = " -s 720x404"+crop
            elif (ratio == "1.66"):
                reso = " -s 720x432"+crop
            elif (ratio == "1.33"):
                reso = " -s 720x540"+crop
            else:
                reso = custom()
        return (reso)

    scan = raw_input(GREEN+"SCAN AUTOCROP SOURCE "+YELLOW+\
                     "(y/n)"+GREEN+" : "+END)
    if (scan == "y"):
        os.system("HandBrakeCLI -t 0 --scan -i"+source)

    ask_screen = raw_input(GREEN+"SCREENSHOT VERIFICATION "+YELLOW+\
                           "(y/n)"+GREEN+" : "+END)
    if (ask_screen == "y"):
        os.system("./xthumb.py "+source+" 5 2")

    man_crop = raw_input(GREEN+"MANUAL SOURCE CROP "+YELLOW+\
                         "(y/n)"+GREEN+" : "+END)
    if (man_crop == "y"):
        w_crop = raw_input(GREEN+"SOURCE CROP WIDTH "+YELLOW+\
                           "(ex: 1920)"+GREEN+" : "+END)
        h_crop = raw_input(GREEN+"SOURCE CROP HEIGHT "+YELLOW+\
                           "(ex: 800)"+GREEN+" : "+END)
        x_crop = raw_input(GREEN+"PIXELS CROP LEFT/RIGHT "+YELLOW+\
                           "(ex: 0)"+GREEN+" : "+END)
        y_crop = raw_input(GREEN+"PIXELS CROP TOP/BOTTOM "+YELLOW+\
                           "(ex: 140)"+GREEN+" : "+END)
        crop = " -filter:v crop="+w_crop+":"+h_crop+\
               ":"+x_crop+":"+y_crop+""
    else:
        crop = ""
    if (format == "4"):
        reso = DVD()
    elif (format == "6"):
        reso = custom()
    else:
        reso = BLURAY()

    #___ x264/x265 Params ___#
    level = raw_input(GREEN+"VIDEO FORMAT PROFILE "+YELLOW+\
                      "(ex: 3.1)"+GREEN+" : "+END)
    preset = raw_input(GREEN+"CUSTOM PRESET X264/X265 > \n"+YELLOW+\
                       "FAST "+GREEN+"[1]"+YELLOW+" - SLOW "+GREEN+\
                       "[2]"+YELLOW+" - SLOWER "+GREEN+"[3]\n"+YELLOW+\
                       "VERYSLOW "+GREEN+"[4]"+YELLOW+" - PLACEBO "+GREEN+\
                       "[5]"+YELLOW+" - NONE "+GREEN+"[6] : "+END)

    if (preset == "1"):
        prest = " -preset fast"
    elif (preset == "2"):
        preset = " -preset slow"
    elif (preset == "3"):
        preset = " -preset slower"
    elif (preset == "4"):
        preset = " -preset veryslow"
    elif (preset == "5"):
        preset = " -preset placebo"
    else:
        preset = ""

    tuned = raw_input(GREEN+"X264/X265 TUNE > \n"+YELLOW+"FILM "+GREEN+\
                      "[1]"+YELLOW+" - ANIMATION "+GREEN+"[2]"+YELLOW+\
                      " - GRAIN "+GREEN+"[3]\n"+YELLOW+"STILLIMAGE "+GREEN+\
                      "[4]"+YELLOW+" - PSNR "+GREEN+"[5]"+YELLOW+\
                      " - SSIM "+GREEN+"[6]\n"+YELLOW+"FASTDECODE "+GREEN+\
                      "[7]"+YELLOW+" - "+GREEN+"[8]"+YELLOW+\
                      " - NONE "+GREEN+"[9] : "+END)

    if (tuned == "1"):
        tune = " -tune film"
    elif (tuned == "2"):
        tune = " -tune animation"
    elif (tuned == "3"):
        tune = " -tune grain"
    elif (tuned == "4"):
        tune = " -tune stillimage"
    elif (tuned == "5"):
        tune = " -tune psnr"
    elif (tuned == "6"):
        tune = " -tune ssim"
    elif (tuned == "7"):
        tune = " -tune fastdecode"
    elif (tuned == "8"):
        tune = " -tune zerolatency"
    else:
        tune = ""

    #___ x264 Expert Mode ___#
    x264 = raw_input(GREEN+"X264/X265 EXPERT MODE "+YELLOW+\
                     "(y/n)"+GREEN+" : "+END)
    if (x264 == "y"):
        threads_ = raw_input(GREEN+"PROCESSOR THREADS "+YELLOW+\
                             "(ex: 8)"+GREEN+" : "+END)
        if not (threads_):
            threads = " -threads 0"
        else:
            threads = " -threads "+threads_

        thread_type_ = raw_input(GREEN+"THREAD TYPE > \n"+YELLOW+\
                                 "SLICE "+GREEN+"[1]"+YELLOW+\
                                 " - FRAME "+GREEN+"[2] : "+END)
        if (thread_type_ == "1"):
            thread_type = " -thread_type slice"
        elif (thread_type_ == "2"):
            thread_type = " -thread_type frame"
        else:
            thread_type = ""
        if (encode_type == "2"):
            fastfirstpass = ""
        else:
            fastfirstpass_ =  raw_input(GREEN+"FAST FIRST PASS "+YELLOW+\
                                        "(y/n)"+GREEN+" : "+END)
            if (fastfirstpass_ == "y"):
                fastfirstpass = " -fastfirstpass 1"
            elif (fastfirstpass_ == "n"):
                fastfirstpass = " -fastfirstpass 0"
            else:
                fastfirstpass = ""

        refs_ = raw_input(GREEN+"REFERENCE FRAMES "+YELLOW+\
                          "(ex: 8)"+GREEN+" : "+END)
        if not (refs_):
            refs = ""
        else:
            refs = " -refs "+refs_

        mixed_ = raw_input(GREEN+"MIXED REFERENCES "+YELLOW+\
                           "(y/n)"+GREEN+" : "+END)
        if (mixed_ == "n"):
            mixed = " -mixed-refs 0"
        elif (mixed_ == "y"):
            mixed = " -mixed-refs 1"
        else:
            mixed = ""

        bf_ = raw_input(GREEN+"MAXIMUM B-FRAMES "+YELLOW+\
                        "(ex: 16)"+GREEN+" : "+END)
        if not (bf_):
            bf = ""
        else:
            bf = " -bf "+bf_

        pyramid_ = raw_input(GREEN+"PYRAMIDAL METHOD > \n"+YELLOW+\
                             "NONE "+GREEN+"[1]"+YELLOW+" - NORMAL "+GREEN+\
                             "[2]"+YELLOW+" - STRICT "+GREEN+"[3] : "+END)
        if (pyramid_ == "1"):
            pyramid = " -b-pyramid none"
        elif (pyramid_ == "2"):
            pyramid = " -b-pyramid normal"
        elif (pyramid_ == "3"):
            pyramid = " -b-pyramid strict"
        else:
            pyramid = ""

        weightb_ = raw_input(GREEN+"WEIGHTED B-FRAMES "+YELLOW+\
                             "(y/n)"+GREEN+" : "+END)
        if (weightb_ == "n"):
            weightb = " -weightb 0"
        elif (weightb_ == "y"):
            weightb = " -weightb 1"
        else:
            weightb = ""

        weightp_ = raw_input(GREEN+"WEIGHTED P-FRAMES > \n"+YELLOW+\
                             "NONE "+GREEN+"[1]"+YELLOW+" - SIMPLE "+GREEN+\
                             "[2]"+YELLOW+" - SMART "+GREEN+"[3] : "+END)
        if (weightp_ == "1"):
            weightp = " -weightp none"
        elif (weightp_ == "2"):
            weightp = " -weightp simple"
        elif (weightp_ == "3"):
            weightp = " -weightp smart"
        else:
            weightp = ""

        dct_ = raw_input(GREEN+"ENABLE 8x8 TRANSFORM "+YELLOW+\
                         "(y/n)"+GREEN+" : "+END)
        if (dct_ == "n"):
            dct = " -8x8dct 0"
        elif (dct_ == "y"):
            dct = " -8x8dct 1"
        else:
            dct = ""

        cabac_ = raw_input(GREEN+"ENABLE CABAC "+YELLOW+\
                           "(y/n)"+GREEN+" : "+END)
        if (cabac_ == "n"):
            cabac = " -coder vlc"
        elif (cabac_ == "y"):
            cabac = " -coder ac"
        else:
            cabac = ""

        b_strategy_ = raw_input(GREEN+"ADAPTIVE B-FRAMES > \n"+YELLOW+\
                                "VERYFAST "+GREEN+"[1]"+YELLOW+\
                                " - FAST "+GREEN+"[2]"+YELLOW+\
                                " - SLOWER "+GREEN+"[3] : "+END)
        if (b_strategy_ == "1"):
            b_strategy = " -b_strategy 0"
        elif (b_strategy_ == "2"):
            b_strategy = " -b_strategy 1"
        elif (b_strategy_ == "3"):
            b_strategy = " -b_strategy 2"
        else:
            b_strategy = ""

        direct_ = raw_input(GREEN+"ADAPTIVE DIRECT MODE > \n"+YELLOW+\
                            "NONE "+GREEN+"[1]"+YELLOW+" - SPATIAL "+GREEN+\
                            "[2]\n"+YELLOW+"TEMPORAL "+GREEN+"[3]"+YELLOW+\
                            " - AUTO "+GREEN+"[4] : "+END)
        if (direct_ == "1"):
            direct = " -direct-pred none"
        elif (direct_ == "2"):
            direct = " -direct-pred spatial"
        elif (direct_ == "3"):
            direct = " -direct-pred temporal"
        elif (direct_ == "4"):
            direct = " -direct-pred auto"
        else:
            direct = ""

        me_method_ = raw_input(GREEN+"MOTION ESTIMATION METHOD > \n"+YELLOW+\
                               "DIA "+GREEN+"[1]"+YELLOW+" - HEX "+GREEN+\
                               "[2]\n"+YELLOW+"UMH "+GREEN+"[3]"+YELLOW+\
                               " - ESA "+GREEN+"[4]"+YELLOW+\
                               " - TESA "+GREEN+"[5] : "+END)
        if (me_method_ == "1"):
            me_method = " -me_method dia"
        elif (me_method_ == "2"):
            me_method = " -me_method hex"
        elif (me_method_ == "3"):
            me_method = " -me_method umh"
        elif (me_method_ == "4"):
            me_method = " -me_method esa"
        elif (me_method_ == "5"):
            me_method = " -me_method tesa"
        else:
            me_method = ""

        subq_ = raw_input(GREEN+"SUBPIXEL MOTION ESTIMATION "+YELLOW+\
                          "(ex: 11)"+GREEN+" : "+END)
        if not (subq_):
            subq = ""
        else:
            subq = " -subq "+subq_

        me_range_ = raw_input(GREEN+"MOTION ESTIMATION RANGE "+YELLOW+\
                              "(ex: 16)"+GREEN+" : "+END)
        if not (me_range_):
            me_range = ""
        else:
            me_range = " -me_range "+me_range_

        partitions_ = raw_input(GREEN+"PARTITIONS TYPE > \n"+YELLOW+\
                                "ALL "+GREEN+"[1]"+YELLOW+" - p8x8 "+GREEN+\
                                "[2]"+YELLOW+" - p4x4 "+GREEN+\
                                "[3]\n"+YELLOW+"NONE "+GREEN+"[4]"+YELLOW+\
                                " - b8x8 "+GREEN+"[5]"+YELLOW+\
                                " - i8x8 "+GREEN+"[6]"+YELLOW+\
                                " - i4x4 "+GREEN+"[7] : "+END)
        if (partitions_ == "1"):
            partitions = " -partitions all"
        elif (partitions_ == "2"):
            partitions = " -partitions p8x8"
        elif (partitions_ == "3"):
            partitions = " -partitions p4x4"
        elif (partitions_ == "4"):
            partitions = " -partitions none"
        elif (partitions_ == "5"):
            partitions = " -partitions b8x8"
        elif (partitions_ == "6"):
            partitions = " -partitions i8x8"
        elif (partitions_ == "7"):
            partitions = " -partitions i4x4"
        else:
            partitions = ""

        trellis_ = raw_input(GREEN+"TRELLIS MODE > \n"+YELLOW+\
                             "OFF "+GREEN+"[1]"+YELLOW+\
                             " - DEFAULT "+GREEN+"[2]"+YELLOW+\
                             " - ALL "+GREEN+"[3] : "+END)
        if (trellis_ == "1"):
            trellis = " -trellis 0"
        elif (trellis_ == "2"):
            trellis = " -trellis 1"
        elif (trellis_ == "3"):
            trellis = " -trellis 2"
        else:
            trellis = ""

        aq_ = raw_input(GREEN+"ADAPTIVE QUANTIZATION "+YELLOW+\
                        "(ex: 1.5)"+GREEN+" : "+END)
        if not (aq_):
            aq = ""
        else:
            aq = " -aq-strength "+aq_

        psy_ = raw_input(GREEN+"PSYCHOVISUAL OPTIMIZATION "+YELLOW+\
                         "(y/n)"+GREEN+" : "+END)
        if (psy_) == "n":
            psy = " -psy 0"
        elif (psy_) == "y":
            psy = " -psy 1"
        else:
            psy = ""

        psyrd1 = raw_input(GREEN+"RATE DISTORTION [psy-rd] "+YELLOW+\
                           "(ex: 1.00)"+GREEN+" : "+END)
        if not (psyrd1):
            psyrd = ""
        else:
            psyrd2 = raw_input(GREEN+"PSYCHOVISUAL TRELLIS [psy-rd] "+\
                               YELLOW+"(ex: 0.15)"+GREEN+" : "+END)
            if not (psyrd2):
                psyrd = ""
            else:
                psyrd = " -psy-rd "+psyrd1+":"+psyrd2

        deblock_ = raw_input(GREEN+"DEBLOCKING "+YELLOW+\
                             "(ex: -1:-1)"+GREEN+" : "+END)
        if not (deblock_):
            deblock = ""
        else:
            deblock = " -deblock "+deblock_

        lookahead_ = raw_input(GREEN+"FRAMES LOOKAHEAD "+YELLOW+\
                     "(ex: 60)"+GREEN+" : "+END)
        if not (lookahead_):
            lookahead = ""
        else:
            lookahead = " -rc-lookahead "+lookahead_

        bluray_ = raw_input(GREEN+"BLURAY COMPATIBILITY "+YELLOW+\
                            "(y/n)"+GREEN+" : "+END)
        if (bluray_ == "y"):
            bluray = " -bluray-compat 1"
        elif (bluray_ == "n"):
            bluray = " -bluray-compat 0"
        else:
            bluray = ""

        fastpskip_ = raw_input(GREEN+"FAST SKIP on P-FRAMES "+YELLOW+\
                               "(y/n)"+GREEN+" : "+END)
        if (fastpskip_ == "y"):
            fastpskip = " -fast-pskip 1"
        elif (fastpskip_ == "n"):
            fastpskip = " -fast-pskip 0"
        else:
            fastpskip = ""

        g_ = raw_input(GREEN+"KEYFRAME INTERVAL "+YELLOW+\
                       "(ex: 250)"+GREEN+" : "+END)
        if not (g_):
            g = ""
        else:
            g = " -g "+g_

        keyint_min_ = raw_input(GREEN+"MINIMAL KEY INTERVAL "+YELLOW+\
                                "(ex: 25)"+GREEN+" : "+END)
        if not (keyint_min_):
            keyint_min = ""
        else:
            keyint_min = " -keyint_min "+keyint_min_

        scenecut_ =  raw_input(GREEN+"SCENECUT DETECTION "+YELLOW+\
                               "(ex: 40)"+GREEN+" : "+END)
        if not (scenecut_):
            scenecut = ""
        else:
            scenecut = " -sc_threshold "+scenecut_

        cmp_ = raw_input(GREEN+"CHROMA MOTION ESTIMATION "+YELLOW+\
                         "(y/n)"+GREEN+" : "+END)
        if (cmp_ == "n"):
            cmp = " -cmp sad"
        elif (cmp_ == "y"):
            cmp = " -cmp chroma"
        else:
            cmp = ""

        param = preset+tune+threads+thread_type+fastfirstpass+refs+mixed+\
                bf+pyramid+weightb+weightp+dct+cabac+b_strategy+direct+\
                me_method+subq+me_range+partitions+trellis+aq+psy+psyrd+\
                deblock+lookahead+bluray+fastpskip+g+keyint_min+scenecut+cmp

        pass1 = preset+tune+threads+thread_type+fastfirstpass

    else:
        param = preset+tune+" -threads 0"
        pass1 = preset+tune+" -threads 0"

    #___ Prez / Torrent  ___#
    nfosource = raw_input(GREEN+"RELEASE SOURCE "+YELLOW+\
                          "(ex: 1080p.HDZ)"+GREEN+" : "+END)
    nfoimdb = raw_input(GREEN+"RELEASE IMDB ID "+YELLOW+\
                        "(ex: 6686697)"+GREEN+" : "+END)

    if (nfoimdb == ""):
        name = ""
    else:
        searchIMDB = "http://deanclatworthy.com/imdb/?id=tt"+nfoimdb
        try:
            data1 = loads(urlopen(searchIMDB).read())
        except (HTTPError, ValueError):
            data1 = ""
            pass

        searchTMDB = "http://api.themoviedb.org/3/movie/tt"+nfoimdb+\
                     "?api_key="+tmdb_api_key+"&language=fr"
        dataTMDB = urllib2.Request(\
                   searchTMDB, headers={"Accept" : "application/json"})
        try:
            data2 = loads(urllib2.urlopen(dataTMDB).read())
        except (HTTPError, ValueError):
            data2 = ""
            pass

        searchOMDB = "http://www.omdbapi.com/?i=tt%s"+nfoimdb
        try:
            data3 = loads(urlopen(searchOMDB).read())
        except (HTTPError, ValueError):
            data3 = ""
            pass

        tit1 = "title"
        tit2 = "original_title"
        tit3 = "Title"

        if (tit1 in data1):
            dir = "%s" % data1['title']
            name = dir.replace(' ', '.').replace('/', '')\
                      .replace('(', '').replace(')', '')\
                      .replace('"', '').replace(':', '')\
                      .replace("'", "").replace("[", "")\
                      .replace("]", "").replace(";", "")\
                      .replace(",", "")
        else:
            if (tit2 in data2):
                dir = "%s" % data2['original_title']
                name = dir.replace(' ', '.').replace('/', '')\
                          .replace('(', '').replace(')', '')\
                          .replace('"', '').replace(':', '')\
                          .replace("'", "").replace("[", "")\
                          .replace("]", "").replace(";", "")\
                          .replace(",", "")
            else:
                if (tit3 in data3):
                    dir = "%s" % data3['Title']
                    name = dir.replace(' ', '.').replace('/', '')\
                              .replace('(', '').replace(')', '')\
                              .replace('"', '').replace(':', '')\
                              .replace("'", "").replace("[", "")\
                              .replace("]", "").replace(";", "")\
                              .replace(",", "")
                else:
                    name = ""
                    nfoimdb = ""

    tsize = raw_input(GREEN+"RELEASE SIZE > \n"+YELLOW+\
                      "SD - 350 - 550 - 700 - 1.37 - 2.05 - 2.74 - 4.37 "\
                      "- 6.56 - HD"+GREEN+" : "+END)

    tsize = tsize.lower()
    if (tsize == "350"):
        pieces = "18"
        prezsize = "350Mo"
    elif (tsize == "550"):
        pieces = "18"
        prezsize = "550Mo"
    elif (tsize == "700"):
        pieces = "19"
        prezsize = "700Mo"
    elif (tsize == "1.37"):
        pieces = "20"
        prezsize = "1.37Go"
    elif (tsize == "2.05"):
        pieces = "20"
        prezsize = "2.05Go"
    elif (tsize == "2.74"):
        pieces = "21"
        prezsize = "2.74Go"
    elif (tsize == "4.37"):
        pieces = "22"
        prezsize = "4.37Go"
    elif (tsize == "6.56"):
        pieces = "22"
        prezsize = "6.56Go"
    elif (tsize == "hd"):
        pieces = "22"
        prezsize = "..Go"
    else:
        pieces = "20"
        prezsize = "..Go"

    pprint = raw_input(GREEN+"PRINT FFMPEG FINAL COMMAND "+YELLOW+\
                       "(y/n)"+GREEN+" : "+END)

    #___ Return Global Values ___#
    info_main = (
        source, thumb, team, announce, title, year, stag, string, codec,
        encode_type, crf, bit, level, idvideo, fps, interlace, interlace2,
        audiolang, audio_config, sub_config, sub_remux, reso, param, pass1,
        mark, nfoimdb, nfosource, titlesub, subforced, prezquality,
        prezsize, pieces, name, pprint
    )

    return (info_main)

#---> PROCESS <---#

banner()

(
    source, thumb, team, announce, title, year, stag, string, codec,
    encode_type, crf, bit, level, idvideo, fps, interlace, interlace2,
    audiolang, audio_config, sub_config, sub_remux, reso, param, pass1,
    mark, nfoimdb, nfosource, titlesub, subforced, prezquality, prezsize,
    pieces, name, pprint
) = main()

run_ffmpeg = [
    ffmpeg(),"","","","","","","","","","","","","","","","","","",""
]

run_data = [
    data(),"","","","","","","","","","","","","","","","","","",""
]

n = 1

if (pprint == "y"):
    print (ffmpeg())

again = raw_input(GREEN+"NEXT ENCODE "+YELLOW+"(y/n)"+GREEN+" : "+END)
while (again != "n"):
    next()

    (
        source, thumb, team, announce, title, year, stag, string, codec,
        encode_type, crf, bit, level, idvideo, fps, interlace, interlace2,
        audiolang, audio_config, sub_config, sub_remux, reso, param, pass1,
        mark, nfoimdb, nfosource, titlesub, subforced, prezquality, prezsize,
        pieces, name, pprint, pending
    ) = main()

    run_ffmpeg[n] = ffmpeg()
    run_data[n] = data()
    n = n + 1

    if (n != 20):
        again = raw_input(GREEN+"NEXT ENCODE "+YELLOW+\
                          "(y/n)"+GREEN+" : "+END)
    else:
        break

for i in range (n):
    os.system(run_ffmpeg[i])
    os.system(run_data[i])
    i = i + 1

print (RED+"\n ->"+GREEN+" ALL JOBS DONE, CONGRATULATIONS !"+END)
print (RED+" ->"+GREEN+" NFO, THUMBNAILS, (PREZ) & TORRENT CREATED !\n"+END)

sys.exit()

if (__name__ == "__main__"):
    main()
