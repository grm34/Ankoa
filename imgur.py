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
import socket
import urllib
import base64
import urllib2
import optparse
import BeautifulSoup
from urllib2 import (urlopen, URLError, HTTPError)
from app.main.events import (imgur_help, imgur_print_url, imgur_upload_error,
                             imgur_timeout_error, imgur_source_error,
                             imgur_process)


def main():

    # HELP
    usage = imgur_help()
    parser = optparse.OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    if (len(args) < 1 or len(args) > 2):
        parser.print_help()
        parser.exit(1)

    # UPLOAD IMG FILE
    if os.path.isfile(sys.argv[1]) is True:
        try:
            imgur_process()
            img_file = open(sys.argv[1], "rb")
            img = base64.b64encode(img_file.read())
            url = 'http://api.imgur.com/2/upload'
            key = {'key': '02b62fd8f1d5e78321e62bb42ced459e', 'image': img}
            data = urllib.urlencode(key)
            req = urllib2.Request(url, data)
            resp = BeautifulSoup.BeautifulSoup(urlopen(req, None, 5.0))
            thumb_link = str(resp.find('original')).replace('<original>', '')\
                                                   .replace('</original>', '')

            # WRITE LINK on PREZ
            if (len(args) == 2 and args[1] == "add"):
                f = file("{0}.txt".format(sys.argv[1][:-4]), 'r')
                chaine = f.read()
                f.close()
                data = chaine.replace("thumbnails_link", thumb_link)
                f = file("{0}.txt".format(sys.argv[1][:-4]), 'w')
                f.write(data)
                f.close

            imgur_print_url(thumb_link)

        # Upload Error
        except (HTTPError, ValueError, IOError, TypeError, URLError) as e:
            imgur_upload_error(e)
        except socket.timeout:
            imgur_timeout_error()
            sys.exit()

    # Thumbnails not found
    else:
        imgur_source_error()

if (__name__ == "__main__"):
    main()
