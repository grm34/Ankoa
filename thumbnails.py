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
import time
import glob
import Image
import shutil
import commands
import optparse
import ImageDraw
import ImageFont
from user.settings import option
from django.utils.encoding import (smart_str, smart_unicode)
from app.main.events import (thumbnails_help, global_error,
                             bad_source, bad_thumbs, thumbnails_process,
                             thumbnails_success)

(folder, thumb, tag, team, announce, tmdb_api_key, tag_thumb) = option()


def snapshot(path, nb_lgn, nb_col):
    mplayer = 'mplayer -identify -frames 0 {0} 2>/dev/null| grep ID_'
    infos = commands.getoutput(mplayer.format(path))

    longueur = int(re.findall('ID_LENGTH=([0-9]*)', infos)[0])-300
    os.mkdir(os.path.expanduser(thumb)+'rtemp')
    interval = int(longueur/(int(nb_lgn)*int(nb_col)+1))
    width = int(re.findall('ID_VIDEO_WIDTH=([0-9]*)', infos)[0])

    for i in range(300, longueur-interval, interval):
        mplayer2 = 'mplayer -nosound -ss {0} -frames 4 -vf scale'\
                   ' -vo png:z=0 {1}'.format(str(i), path)
        empty = commands.getoutput(mplayer2)

        shutil.move('00000004.png', os.path.expanduser(thumb) +
                    'rtemp/' + str(i).zfill(5) + '.png')
        image = Image.open(os.path.expanduser(thumb) +
                           'rtemp/' + str(i).zfill(5) + '.png')
        draw = ImageDraw.Draw(image)

        if (width <= 720):
            xfont = 20
        elif (width > 720 and width <= 1280):
            xfont = 35
        else:
            xfont = 50

        font = ImageFont.truetype(
            os.path.expanduser("app/skin/") + 'police.ttf', xfont)

        draw.text(
            (10, 10), time.strftime('%H:%M:%S', time.gmtime(i)), font=font)

        image.save(
            os.path.expanduser(thumb) + 'rtemp/' + str(i).zfill(5) + '.png')

    for i in range(1, 4):
        os.remove('0000000{0}.png'.format(str(i)))

    return (infos, longueur)


def trait_path(path):
    path = path.replace(' ', '\\ ').replace('[', '\\[').replace(']', '\\]')\
               .replace('(', '\\(').replace(')', '\\)')
    return path


def index_th(infos, nb_col, nb_lgn):
    width = int(re.findall('ID_VIDEO_WIDTH=([0-9]*)', infos)[0])
    height = int(re.findall('ID_VIDEO_HEIGHT=([0-9]*)', infos)[0])
    nb_col, nb_lgn = int(nb_col), int(nb_lgn)

    if (width <= 720):
        [x, y, a, b, c, d] = [0, 120, 25, 45, 115, 5]
    elif (width > 720 and width <= 1280):
        [x, y, a, b, c, d] = [0, 225, 25, 45, 235, 8]
    else:
        [x, y, a, b, c, d] = [0, 330, 30, 60, 330, 10]

    img_idx = Image.new("RGB", (a+width*nb_col, b+height*nb_lgn+c), "#FFFFFF")
    pre = glob.glob(os.path.expanduser(thumb)+'rtemp/'+'*.png')
    pre.sort()

    for i in pre:
        im = Image.open(i)
        im_t = im.resize((width, height), Image.ANTIALIAS)
        img_idx.paste(im_t, (10+(width+d)*x, 10+y))
        if (x == nb_col-1):
            y += d+height
            x = 0
        else:
            x += 1

    img_idx.save(os.path.expanduser(thumb)+'index.png', "PNG")


def img_infos(infos, duree, path):
    width = re.findall('ID_VIDEO_WIDTH=([0-9]*)', infos)[0]
    height = re.findall('ID_VIDEO_HEIGHT=([0-9]*)', infos)[0]
    path = path.replace("\\", "")
    taille = os.stat(path)[6]
    image = Image.open(os.path.expanduser(thumb)+'index.png')
    draw = ImageDraw.Draw(image)
    nom = path.split("/")
    title = nom[-1]

    if (int(width) <= 720):
        [e, f, g, h, i, j, k] = [10, 20, 35, 55, 75, 95, 20]

    elif (int(width) > 720 and int(width) <= 1280):
        [e, f, g, h, i, j, k] = [15, 30, 60, 100, 140, 180, 35]

    else:
        [e, f, g, h, i, j, k] = [20, 40, 85, 145, 205, 265, 50]

    font = ImageFont.truetype(
        os.path.expanduser("app/skin/") + 'police.ttf', k)
    draw.text((e, e), "" + tag_thumb + "", font=font, fill="#000000")
    draw.text((f, g), "TiTLE : " + title[:-4], font=font, fill="#000000")
    draw.text((f, h), "SiZE..............: " +
              str(int(float(taille)/1048576)) + " Mo",
              font=font, fill="#000000")
    draw.text((f, i), "DURATiON..........: " +
              str(int(float(duree)/60+5)) + " Min",
              font=font, fill="#000000")
    draw.text((f, j), "RESOLUTiON........: " +
              width + "x" + height, font=font, fill="#000000")

    image.save(os.path.expanduser(thumb) + 'index.png', "PNG")
    shutil.move(os.path.expanduser(thumb) + 'index.png',
                os.path.expanduser(thumb) + title[:-3] + 'png')

    if (width > 800):
        resize = ("convert -quality 0 -resize 3470000@ {0}{1}png {0}{1}png"
                  .format(thumb, title[:-3]))
        os.system(resize)


def main(argv):

    # HELP
    usage = thumbnails_help()
    parser = optparse.OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    if (len(args) != 3):
        parser.print_help()
        parser.exit(1)

    # RUN
    if os.path.isfile(sys.argv[1]) is True:
        if (os.path.isdir(os.path.expanduser(thumb) + 'rtemp')):
            shutil.rmtree(os.path.expanduser(thumb) + 'rtemp')
        try:
            thumbnails_process()
            path = trait_path(argv[0])
            info, longueur = snapshot(path, argv[1], argv[2])
            index_th(info, argv[2], argv[1])
            img_infos(info, longueur, path)
            thumbnails_success()

        # Thubnails Error
        except (IOError, IndexError) as e:
            bad_thumbs(e)
            sys.exit()

        if (os.path.isdir(os.path.expanduser(thumb) + 'rtemp')):
            shutil.rmtree(os.path.expanduser(thumb) + 'rtemp')

    # Source not found
    else:
        bad_source()

if (__name__ == "__main__"):
    main(sys.argv[1:])
