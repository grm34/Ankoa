#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#-------------------- [ AnKoA ] -------------------#
#     Made with love by grm34 (FRIPOUILLEJACK)     #
#--------------------------------------------------#
"""
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
    modify and/ or redistribute the software under the terms of the CeCILL-C
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
import shutil
import glob
import Image
import ImageDraw
import ImageFont
import re
import time
import optparse
sys.path.append("app/")
from settings import option
from style import color

(folder, thumb, tag, team, announce, tmdb_api_key, tag_thumb) = option()

(BLUE, RED, YELLOW, GREEN, END) = color()

def snapshot(path, nb_lgn, nb_col):
    buff=os.popen('mplayer -identify -frames 0 '+path+\
                  ' 2>/dev/null| grep ID_')
    infos=buff.read()
    buff.close()

    longueur = int(re.findall('ID_LENGTH=([0-9]*)', infos)[0])-300
    os.mkdir(os.path.expanduser(thumb)+'rtemp')
    interval = int(longueur/(int(nb_lgn)*int(nb_col)+1))
    width = int(re.findall('ID_VIDEO_WIDTH=([0-9]*)', infos)[0])

    for i in range(300, longueur-interval, interval):
        os.system('mplayer -nosound -ss '+str(i)+\
                  ' -frames 4 -vf scale -vo png:z=0 '+path)
        try:
            shutil.move('00000004.png', os.path.expanduser(thumb)+\
                        'rtemp/'+str(i).zfill(5)+'.png')
            image = Image.open(os.path.expanduser(thumb)+\
                               'rtemp/'+str(i).zfill(5)+'.png')
            draw = ImageDraw.Draw(image)

            if (width <= 720):
                font = ImageFont.truetype(os.path.expanduser("app/")+\
                                          'police.ttf', 20)
            elif (width > 720 and width <= 1280):
                font = ImageFont.truetype(os.path.expanduser("app/")+\
                                          'police.ttf', 35)
            else:
                font = ImageFont.truetype(os.path.expanduser("app/")+\
                                          'police.ttf', 50)

            draw.text((10, 10),
                      time.strftime('%H:%M:%S', time.gmtime(i)),
                      font=font)

            image.save(os.path.expanduser(thumb)+\
                       'rtemp/'+str(i).zfill(5)+'.png')

        except (IOError, IndexError):
            print (GREEN+"\n ->"+BLUE+" BAD THUMBS : "+\
                   RED+str(e)+"\n"+END)
            sys.exit()

    for i in range(1, 4):
        os.remove('0000000'+str(i)+'.png')

    return (infos, longueur)

def trait_path(path):
    path = path.replace(' ', '\\ ').replace('[', '\\[')\
               .replace(']', '\\]').replace('(', '\\(')\
               .replace(')', '\\)')
    return (path)

def index_th(infos, nb_col, nb_lgn):
    width = int(re.findall('ID_VIDEO_WIDTH=([0-9]*)', infos)[0])
    height = int(re.findall('ID_VIDEO_HEIGHT=([0-9]*)', infos)[0])
    nb_col, nb_lgn = int(nb_col), int(nb_lgn)

    if (width <= 720):
        x = 0
        y = 120
        img_idx = Image.new("RGB", (25+width*nb_col, 45+height*nb_lgn+115),
                            "#FFFFFF")
    elif (width > 720 and width <= 1280):
        x = 0
        y = 225
        img_idx = Image.new("RGB", (25+width*nb_col, 45+height*nb_lgn+235),
                            "#FFFFFF")
    else:
        x = 0
        y = 330
        img_idx = Image.new("RGB", (30+width*nb_col, 60+height*nb_lgn+330),
                            "#FFFFFF")

    pre = glob.glob(os.path.expanduser(thumb)+'rtemp/'+'*.png')
    pre.sort()

    for i in pre:
        im=Image.open(i)
        im_t = im.resize((width, height), Image.ANTIALIAS)

        if (width <= 720):
            img_idx.paste(im_t, (10+(width+5)*x, 10+y))
            if (x == nb_col-1):
                y += 5+height
                x = 0
            else:
                x += 1
        elif (width > 720 and width <= 1280):
            img_idx.paste(im_t, (10+(width+8)*x, 10+y))
            if (x == nb_col-1):
                y += 8+height
                x = 0
            else:
                x += 1
        else:
            img_idx.paste(im_t, (10+(width+10)*x, 10+y))
            if (x == nb_col-1):
                y += 10+height
                x = 0
            else:
                x+=1

    img_idx.save(os.path.expanduser(thumb)+'index.png' , "PNG")

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
        font = ImageFont.truetype(os.path.expanduser("app/")+\
                                  'police.ttf', 20)
        draw.text((10, 10), ""+tag+"", font=font, fill="#000000")
        draw.text((20, 35), "TiTLE : " + title[:-4],
                  font=font, fill="#000000")
        draw.text((20, 55), "SiZE..............: " +\
                  str(int(float(taille)/1048576)) + " Mo",
                  font=font, fill="#000000")
        draw.text((20, 75), "DURATiON..........: " +\
                  str(int(float(duree)/60+5)) + " Min",
                  font=font, fill="#000000")
        draw.text((20, 95), "RESOLUTiON........: " +\
                  width + "x" + height, font=font, fill="#000000")

    elif (int(width) > 720 and int(width) <= 1280):
        font = ImageFont.truetype(os.path.expanduser("app/")+\
                                  'police.ttf', 35)
        draw.text((15, 15), ""+tag+"", font=font, fill="#000000")
        draw.text((30, 60), "TiTLE : " + title[:-4],
                  font=font, fill="#000000")
        draw.text((30, 100), "SiZE..............: " +\
                  str(int(float(taille)/1048576)) + " Mo",
                  font=font, fill="#000000")
        draw.text((30, 140), "DURATiON..........: " +\
                  str(int(float(duree)/60+5)) + " Min",
                  font=font, fill="#000000")
        draw.text((30, 180), "RESOLUTiON........: " +\
                  width + "x" + height, font=font, fill="#000000")
    else:
        font = ImageFont.truetype(os.path.expanduser("app/")+\
                                  'police.ttf', 50)
        draw.text((20, 20), ""+tag+"", font=font, fill="#000000")
        draw.text((40, 85), "TiTLE : " + title[:-4],
                  font=font, fill="#000000")
        draw.text((40, 145), "SiZE..............: " +\
                  str(int(float(taille)/1048576)) + " Mo",
                  font=font, fill="#000000")
        draw.text((40, 205), "DURATiON..........: " +\
                  str(int(float(duree)/60+5)) + " Min",
                  font=font, fill="#000000")
        draw.text((40, 265), "RESOLUTiON........: " +\
        width + "x" + height, font=font, fill="#000000")

    image.save(os.path.expanduser(thumb)+'index.png', "PNG")
    shutil.move(os.path.expanduser(thumb)+'index.png',
                os.path.expanduser(thumb)+title[:-3]+'png')

    if (width > 800):
        resize = ("convert -quality 0 -resize 3470000@ "+thumb+\
                  title[:-3]+"png "+thumb+title[:-3]+"png")
        os.system(resize)

def main(argv):
    usage = "./thumbnails.py video 5 2"

    parser = optparse.OptionParser(usage = usage)
    (options, args) = parser.parse_args()
    if (len(args) != 3):
        parser.print_help()
        parser.exit(1)

    if (os.path.isdir(os.path.expanduser(thumb)+'rtemp')):
        shutil.rmtree(os.path.expanduser(thumb)+'rtemp')
    try:
        path = trait_path(argv[0])
        info, longueur = snapshot(path, argv[1], argv[2])
        index_th(info, argv[2], argv[1])
        img_infos(info, longueur, path)

    except (IOError, IndexError) as e:
        print (GREEN+"\n ->"+BLUE+" BAD THUMBS : "+\
               RED+str(e)+"\n"+END)
        sys.exit()

    if (os.path.isdir(os.path.expanduser(thumb)+'rtemp')):
        shutil.rmtree(os.path.expanduser(thumb)+'rtemp')

if (__name__ == "__main__"):
    main(sys.argv[1:])