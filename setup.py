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
import optparse
import readline
sys.path.append("app/")
from style import (banner, color)

(BLUE, RED, YELLOW, GREEN, END) = color()


def main():

    # HELP
    usage = "python setup.py [install] | [update]"
    parser = optparse.OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    if ((len(args) != 1) and
            (sys.argv[1] != "install" or sys.argv[1] != "update")):
        parser.print_help()
        parser.exit(1)

    # INSTALL
    if (sys.argv[1] == "install"):

        # Auto complete
        def completer(text, state):
            return (
                [entry + "/" for entry in os.listdir(
                    os.path.dirname(
                        readline.get_line_buffer())
                    ) if entry.startswith(text)][state])

        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)

        # Install form
        banner()
        source = raw_input("{0}ENTER SOURCE PATH {1}(ex: /home/user/torrent"
                           "s/){0} : {2}".format(GREEN, YELLOW, END))
        while not source or os.path.exists(source) is False:
            print ("\n{0} -> {1}ERROR : {2}Bad SOURCE PATH, please try"
                   " again !{3}\n".format(GREEN, BLUE, RED, END))
            source = raw_input("{0}ENTER SOURCE PATH {1}(ex: /home/user/torre"
                               "nts/){0} : {2}".format(GREEN, YELLOW, END))
        result = raw_input("{0}ENTER DESTINATION PATH {1}(ex: /home/user/en"
                           "codes/){0} : {2}".format(GREEN, YELLOW, END))
        while not result or os.path.exists(result) is False:
            print ("\n{0} -> {1}ERROR : {2}Bad DESTINATION PATH, please try"
                   " again !{3}\n".format(GREEN, BLUE, RED, END))
            result = raw_input("{0}ENTER DESTINATION PATH {1}(ex: /home/user/"
                               "encodes/){0} : {2}"
                               .format(GREEN, YELLOW, END))
        readline.parse_and_bind("tab: ")
        team = raw_input("{0}ENTER PERSONAL TEAM NAME {1}(ex: KULTURA){0} :"
                         " {2}".format(GREEN, YELLOW, END))
        while not team:
            print ("\n{0} -> {1}ERROR : {2}Please, specify team name "
                   "!{3}\n".format(GREEN, BLUE, RED, END))
            team = raw_input("{0}ENTER PERSONAL TEAM NAME {1}(ex: KULTURA){0}"
                             " : {2}".format(GREEN, YELLOW, END))
        tk = raw_input("{0}ENTER URL TRACKER ANNOUNCE {1}(ex: http://tk.com"
                       ":80/announce){0} : {2}".format(GREEN, YELLOW, END))
        while not tk:
            print ("\n{0} -> {1}ERROR : {2}Please, specify tracker url announ"
                   "ce !{3}\n".format(GREEN, BLUE, RED, END))
            tk = raw_input("{0}ENTER URL TRACKER ANNOUNCE {1}(ex: http://tk.c"
                           "om:80/announce){0} : {2}"
                           .format(GREEN, YELLOW, END))
        api = raw_input("{0}ENTER PERSONAL TMDB API KEY {1}(from: https://w"
                        "ww.themoviedb.org/documentation/api){0} : {2}"
                        .format(GREEN, YELLOW, END))
        while not api:
            print ("\n{0} -> {1}ERROR : {2}Please, specify TMDB API KEY"
                   " !{3}\n".format(GREEN, BLUE, RED, END))
            api = raw_input("{0}ENTER PERSONAL TMDB API KEY {1}(from: https:/"
                            "/www.themoviedb.org/documentation/api){0} : {2}"
                            .format(GREEN, YELLOW, END))

        if (source != "" or result != "" or team != "" or
                tk != "" or api != ""):

            # AUTHORIZE
            try:
                os.system("chmod +x * && chmod +x app/*")
                os.system("cp app/base.nfo app/nfo_base.nfo")
            except OSError as e:
                print ("{0} -> {1}ERROR : {2}{4}{3}\n"
                       .format(GREEN, BLUE, RED, END, str(e)))
                sys.exit()

            # SAVE personal settings
            temp = sys.stdout
            sys.stdout = open('app/save.txt', 'w')
            print ("{0}\n{1}\n{2}\n{3}\n{4}".format(source, result,
                                                    team, tk, api))
            sys.stdout.close()
            sys.stdout = temp

            # WRITE personal settings
            f = file('app/settings.py', 'r')
            chaine = f.read()
            f.close()
            data = chaine.replace("XXX001", source.strip())\
                         .replace("XXX002", result.strip())\
                         .replace("XXX003", team.strip().replace(' ', '.'))\
                         .replace("XXX004", tk.strip())\
                         .replace("XXX005", api.strip())
            f = file('app/settings.py', 'w')
            f.write(data)
            f.close

            # WRITE nfogen settings
            ff = file('nfogen.sh', 'r')
            chaine = ff.read()
            ff.close()
            data = chaine.replace("XXX002", result.strip())
            ff = file('nfogen.sh', 'w')
            ff.write(data)
            ff.close

            print ("\n{0} AnkoA {1}-> {2}Installation successful !\n{3}"
                   .format(BLUE, RED, GREEN, END))

        else:
            print ("\n{0} AnkoA {1}-> {2}Invalid settings,"
                   " please try again !\n{3}"
                   .format(BLUE, GREEN, RED, END))

    # UPDATE
    if (sys.argv[1] == "update"):

        # AUTHORIZE
        try:
            os.system("chmod +x * && chmod +x app/*")
        except OSError as e:
            print ("{0} -> {1}ERROR : {2}{4}{3}\n"
                   .format(GREEN, BLUE, RED, END, str(e)))
            sys.exit()

        try:
            # READ personal settings
            with open('app/save.txt') as save:
                opts = save.read().split("\n")

            # WRITE personal settings
            f = file('app/settings.py', 'r')
            chaine = f.read()
            f.close()
            data = chaine.replace("XXX001", opts[0].strip())\
                         .replace("XXX002", opts[1].strip())\
                         .replace("XXX003", opts[2].strip())\
                         .replace("XXX004", opts[3].strip())\
                         .replace("XXX005", opts[4].strip())
            f = file('app/settings.py', 'w')
            f.write(data)
            f.close

            # WRITE nfogen settings
            ff = file('nfogen.sh', 'r')
            chaine = ff.read()
            ff.close()
            data = chaine.replace("XXX002", opts[1].strip())
            ff = file('nfogen.sh', 'w')
            ff.write(data)
            ff.close

            print ("\n{0} AnkoA {1}-> {2}Update successful !\n{3}"
                   .format(BLUE, RED, GREEN, END))

        except (IOError, IndexError):
            print ("\n{0} AnkoA {1}-> {2}Update error, fix it"
                   " with a clean install !\n{3}"
                   .format(BLUE, GREEN, RED, END))

if (__name__ == "__main__"):
    main()
