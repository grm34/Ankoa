#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#------------------  AnKoA  -----------------------#
#     Made with love by grm34 (FRIPOUILLEJACK)     #
#     ........fripouillejack@gmail.com .......     #
# Greetz: thibs, Rockweb, c0da, Hydrog3n, Speedy76 #
#--------------------------------------------------#

from style import color

(BLUE, RED, YELLOW, GREEN, END) = color()

def calcul():
    HH = raw_input(GREEN+"CALCULATOR HOURS : "+END)
    MM = raw_input(GREEN+"CALCULATOR MINUTES : "+END)
    SS = raw_input(GREEN+"CALCULATOR SECONDS : "+END)
    audiobit = raw_input(GREEN+"CALCULATOR AUDIO BITRATE : "+END)
    rls_size = raw_input(GREEN+"CALCULATOR SIZE > \n"+YELLOW+\
                         "350 - 550 - 700 - 1.37 - 2.05 - 2.74 - 4.37 "\
                         "- 6.56"+GREEN+" : "+END)

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
        "wcalc [{"+calsize+"-[{"+audiobit+"/8}/1024*[{"+HH+\
        "*3600}+{"+MM+"*60}+"+SS+"]]}/[{"+HH+"*3600}+{"+MM+\
        "*60}+"+SS+"]]*8*1024"
    )