#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#------------------  AnKoA  -----------------------#
#     Made with love by grm34 (FRIPOUILLEJACK)     #
#     ........fripouillejack@gmail.com .......     #
# Greetz: thibs, Rockweb, c0da, Hydrog3n, Speedy76 #
#--------------------------------------------------#

import sys
import optparse
import urllib
import urllib2
import base64
import BeautifulSoup
from urllib2 import (urlopen, URLError, HTTPError)
sys.path.append("app/")
from style import color

(BLUE, RED, YELLOW, GREEN, END) = color()

def main():
    usage = "./imgur.py /path/to/image.png"
    parser = optparse.OptionParser(usage = usage)
    (options, args) = parser.parse_args()
    if (len(args) != 1 or args[0] == ""):
        parser.print_help()
        parser.exit(1)

    try:
        file = open(sys.argv[1], "rb")
        img = base64.b64encode(file.read())
        url = 'http://api.imgur.com/2/upload'
        key = {'key':'02b62fd8f1d5e78321e62bb42ced459e', 'image':img}
        data = urllib.urlencode(key)
        req = urllib2.Request(url, data)
        resp = BeautifulSoup.BeautifulSoup(urlopen(req))
        link = str(resp.find('original')).replace('<original>', '')\
                                         .replace('</original>', '')

        print (GREEN + "\nThumbnails url > " + BLUE + link + "\n" + END)

    except (HTTPError, ValueError, IOError) as e:
        print (RED + "\nThumbnails Upload Error > " + \
               BLUE + str(e) + "\n" + END)

if (__name__ == "__main__"):
    main()
