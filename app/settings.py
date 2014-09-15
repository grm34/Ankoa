#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#------------------  AnKoA  -----------------------#
#     Made with love by grm34 (FRIPOUILLEJACK)     #
#     ........fripouillejack@gmail.com .......     #
# Greetz: thibs, Rockweb, c0da, Hydrog3n, Speedy76 #
#--------------------------------------------------#
"""
    folder........: source path (ex: /home/toto/torrents/)
    thumb.........: result path (ex: /home/toto/encodes/)
    tag...........: your team name (ex: KULTURA)
    team..........: MEDIAINFO 'Proudly Present' Tag (ex: TEAM KULTURA)
    announce......: your favorite tracker url announce
    tmdb_api_key..: API Key from https://www.themoviedb.org/documentation/api
    tag_thumb.....: Thumbnails tag (ex: <KULTURA PROUDLY PRESENT>)
"""

def option():

    folder = "XXX001"
    thumb = "XXX002"
    tag = "XXX003"
    team = "TEAM XXX003"
    announce = "XXX004"
    tmdb_api_key = "XXX005"
    tag_thumb = "<XXX003 PROUDLY PRESENTS>"

    values = (folder, thumb, tag, team, announce, tmdb_api_key, tag_thumb)
    return (values)
