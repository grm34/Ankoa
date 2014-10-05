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

import re
import os
import sys
import optparse
import readline
from django.utils.encoding import (smart_str, smart_unicode)
from app.skin.style import banner
from app.main.events import (setup_help, setup_success, setup_error,
                             update_success, update_error, setup_bad_source,
                             setup_bad_dest, setup_bad_team, setup_bad_tk,
                             setup_bad_api, global_error, already_up2date)
from app.main.inputs import (ask_source_path, ask_dest_path, ask_user_team,
                             ask_tk_announce, ask_tmdb_key)
from app.main.param import (bad_chars, regex)

deleted = bad_chars()
(hb_regex, crf_regex, delay_regex, fp_regex, aq_regex, url_regex) = regex()


def main():

    # HELP
    usage = setup_help()
    parser = optparse.OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    if ((len(args) != 1) and
            (sys.argv[1].lower() != "install"
                or sys.argv[1].lower() != "update")):
        parser.print_help()
        parser.exit(1)

    # VERIFICATION
    if os.path.exists("app/") is False\
            and os.path.isfile("app/nfo/base.nfo") is False\
            and os.path.isfile("user/settings.py") is False\
            and os.path.isfile("nfogen.sh") is False:

        # Files not found
        setup_error()
        sys.exit()

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
        banner()

        # Specify Source Path
        source = ask_source_path()
        while not source or os.path.exists(source) is False:
            setup_bad_source()
            source = ask_source_path()

        # Specify Destination Path
        result = ask_dest_path()
        while not result or os.path.exists(result) is False:
            setup_bad_dest()
            result = ask_dest_path()
        readline.parse_and_bind("tab: ")

        # Specify Team Name
        team = ask_user_team()
        while not team:
            setup_bad_team()
            team = ask_user_team()

        # Clean # Team Name
        for d_char in deleted:
            if d_char in team.strip():
                team = smart_str(team).strip().replace(' ', '.')\
                                              .replace(d_char, '')
            else:
                team = smart_str(team).strip().replace(' ', '.')

        # Specify Tracker URL announce
        tk = ask_tk_announce()
        tk_regex = re.compile(url_regex, flags=0).search(tk.strip())
        while not tk or tk_regex is None:
            setup_bad_tk()
            tk = ask_tk_announce()
            tk_regex = re.compile(url_regex, flags=0).search(tk.strip())
        tk = tk.strip()

        # Specify TMDB API KEY
        api = ask_tmdb_key()
        key_regex = r"^[a-zA-Z0-9_]*$"
        api_regex = re.compile(key_regex, flags=0).search(api.strip())
        while not api or api_regex is None:
            setup_bad_api()
            api = ask_tmdb_key()
        api = api.strip()

        try:

            # Authorize & copy NFO
            os.system("chmod +x * app/* user/* app/modules/* app/skin/*")
            os.system("cp app/nfo/base.nfo user/nfo_base.nfo")

            # SAVE personal settings
            temp = sys.stdout
            sys.stdout = open('user/settings.txt', 'w')
            print ("{0}\n{1}\n{2}\n{3}\n{4}".format(source, result,
                                                    team, tk, api))
            sys.stdout.close()
            sys.stdout = temp

            # WRITE personal settings
            f = file('user/settings.py', 'r')
            chaine = f.read()
            f.close()
            if "XXX001" in chaine and "XXX002" in chaine:
                data = chaine.replace("XXX001", source.strip())\
                             .replace("XXX002", result.strip())\
                             .replace("XXX003", team.strip()
                                                    .replace(' ', '.'))\
                             .replace("XXX004", tk.strip())\
                             .replace("XXX005", api.strip())
                f = file('user/settings.py', 'w')
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

                # Install successful
                setup_success()

            # Already installed or corrupted
            else:
                setup_error()
                sys.exit()

        # Install Error
        except OSError as e:
            global_error(e)
            sys.exit()

    # UPDATE
    if (sys.argv[1] == "update"):

        try:

            # AUTHORIZE
            os.system("chmod +x * app/* user/* app/modules/* app/skin/*")

            # READ personal settings
            with open('user/settings.txt') as save:
                opts = save.read().split("\n")

            # WRITE personal settings
            f = file('user/settings.py', 'r')
            chaine = f.read()
            f.close()
            if "XXX001" in chaine and "XXX002" in chaine:
                data = chaine.replace("XXX001", opts[0].strip())\
                             .replace("XXX002", opts[1].strip())\
                             .replace("XXX003", opts[2].strip())\
                             .replace("XXX004", opts[3].strip())\
                             .replace("XXX005", opts[4].strip())
                f = file('user/settings.py', 'w')
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

                # Update successful
                update_success()

            # Already up to date
            else:
                already_up2date()
                sys.exit()

        # Setup Error
        except (IOError, IndexError):
            update_error()
            sys.exit()

if (__name__ == "__main__"):
    main()
