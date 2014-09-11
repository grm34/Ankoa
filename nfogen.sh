#!/bin/bash
#
#------------------  AnKoA  -----------------------#
#     Made with love by grm34 (FRIPOUILLEJACK)     #
#     ........fripouillejack@gmail.com .......     #
# Greetz: thibs, Rockweb, c0da, Hydrog3n, Speedy76 #
#--------------------------------------------------#

FINAL=${1}
SOURCE=${2}
SOURCESRT=${3}
FORCED=${4}
IMDB=${5}
EXT=${1##*.}
FILE_NAME=`basename "${FINAL}" ".${EXT}"`

if [ -f "${FINAL}" ]; then
    php -e app/nfo.php "${FINAL}" "${FILE_NAME}" "${SOURCE}" "${SOURCESRT}" "${IMDB}" "${FORCED}" >> XXX002$FILE_NAME.nfo
else
    echo "NFO Error : bad source !"
fi
