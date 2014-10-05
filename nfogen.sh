#!/bin/bash
#
# [AnKoA] Made with love by grm34 (FRIPOUILLEJACK)
#
# Copyright PARDO Jérémy (Sept 2014)
# Contact: jerem.pardo@gmail.com
#
# This software is a computer program whose purpose is to help command
# line encoders. Intuitive command line interface with many tools:
#
# * FFMPEG easy encoding
# * Thumbnails Generator
# * NFO Generator
# * Genprez Upload
# * Auto make .torrent
#
# This software is governed by the CeCILL-C license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/or redistribute the software under the terms of the CeCILL-C
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL-C license and that you accept its terms.

# HELP
HELP=$(
/usr/bin/python <<'EOF'
from app.main.events import nfogen_help
usage = nfogen_help()
print usage
EOF
)
function help {
    echo -e "${HELP}\n\n"
    echo -e "Options:\n  -h, --help  show this help message and exit"
    exit 0
}

# COLORS
RED='\e[0;31m'
BLUE='\e[0;36m'
GREEN='\e[0;32m'
YELLOW='\e[0;33m'
END='\e[0m'

# VALUES
VIDEO=${1}
SOURCE=${2}
SUBS=${3}
SUBFORCED=${4}
URL=${5}
EXT=${1##*.}
TITLE=`basename "${VIDEO}" ".${EXT}"`

# NFOGEN
function nfogen {

    if ([ -f "${VIDEO}" ] && [ -n "$SOURCE" ] && [ -n "$SUBS" ] \
&& [ -n "$SUBFORCED" ] && [ -n "$URL" ]); then

        echo -e "${RED} > ${BLUE}Creating NFO...${END}"
        php -e app/nfo/nfo.php "${VIDEO}" "${TITLE}" "${SOURCE}" "\
${SUBS}" "${SUBFORCED}" "${URL}" >> XXX002$TITLE.nfo

        echo -e "${RED} > ${GREEN}NFO created !${END}"

    elif [ -f "${VIDEO}" ]; then
        help;
    else

        echo -e "${END} > ${RED}NFO ERROR : ${GREEN}Bad source, specify \
valid video source !${END}"

    fi
}

# EXECUTE
case $1 in -h | --help)
        help;;
    *)
        nfogen
esac
