AnkoA v3.2.2
=====

**FFMPEG Command Line Easy Encoding Tools ...** [**Video Demo**](https://www.youtube.com/watch?v=RvEIvgnXdBg&feature=youtu.be)

![AnkoA](http://i.imgur.com/BlG3BNs.png)

## Description :

* FFMPEG easy encoding
* Thumbnails Generator
* NFO Generator
* Genprez Upload
* Auto make .torrent

## How to install AnkoA ?

Take a tour on the [**wiki**](https://github.com/grm34/AnkoA/wiki)

Chan IRC : **irc.bakaserv.net/6667 #AnkoA**

## Usage :

* **Easy encoding tool :**
`./ankoa.py`

* **Thumbnails generator :**
`./thumbnails.py source.video 5 2`

* **Upload thumbnails on imgur :**
`./imgur.py thumbnails.png`

* **Genprez :**
`./genprez.py LANGUAGE QUALITY CODECS SUBS SIZE ID_IMDB`

* **NFO generator :**
`./nfogen.sh source.video SOURCE SUBS SUBFORCED URL`

* **Thumbs+nfo+torrent :**
`./make.py source.video SOURCE SUBS SUBFORCED URL`

### Values :

    SOURCE..............: release source     →  1080p.THENiGHTMAREiNHD
    SUBS................: subtitles source   →  FULL.FRENCH.Z1
    SUBFORCED...........: forced subtitles   →  FRENCH.FORCED or N/A
    LANGUAGE............: release language   →  ENGLiSH
    FORMAT..............: release format     →  720p.BluRay
    CODECS..............: release codecs     →  AC3.x264
    SiZE................: release size       →  1.37Go
    iD_iMDB.............: release iMDB iD    →  1121931 (without 'tt')
    URL.................: release infos url  →  http://www.imdb.com/title/tt0315733

## Version :

Take a tour on the [**changelog**](https://github.com/grm34/AnkoA/wiki/changelog)

#### Thanks for assistance and contributions :

* [@thibs](https://github.com/thibs7777777)
* [@Rockweb](https://github.com/Rockweb)
* [@c0ding](https://github.com/c0ding)
* [@Hydrog3n](https://github.com/Hydrog3n)
* [@speedy76](https://github.com/speedy76)

#### Links :

* [AnkoA wiki](https://github.com/grm34/AnkoA/wiki)
* [Install or update AnkoA](https://github.com/grm34/AnkoA/wiki/Install-or-update-AnkoA)
* [Compile Multimedia Environment](https://github.com/grm34/AnkoA/wiki/Compile-Multimedia-Environment)
* [AnkoA global usage](https://github.com/grm34/AnkoA/wiki/AnkoA-global-usage)
* [How to crop with AnkoA](https://github.com/grm34/AnkoA/wiki/How-to-crop-with-AnkoA)
* [How to use subtitles with AnkoA](https://github.com/grm34/AnkoA/wiki/How-to-use-subtitles-with-AnkoA)
* [AnkoA changelog](https://github.com/grm34/AnkoA/wiki/Changelog)
* [Video demonstration](https://www.youtube.com/watch?v=RvEIvgnXdBg&feature=youtu.be)
* [NFO example](https://github.com/grm34/AnkoA/wiki/NFO-Example)

***
### License :

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

***
### Project stats :

    Filename:         Source:    Comment:    Both:    Blank:    Total:

    nfo.php                32          39       21        20       112
    ankoa.py              100          49        2        24       175
    genprez.py            284          62        7        35       388
    imgur.py               53          45        0         9       107
    make.py                37          46        0        10        93
    setup.py              142          61        0        29       232
    thumbnails.py         181          45       18        35       279
    bitrate.py             36          43        0         9        88
    settings.py            10          55        0         5        70
    style.py               14          66        5         6        91
    system.py            1348         219       43       221      1806
    nfogen.sh              15          41        1         4        61

    [Total] :            2252         771       97       407      3527

***
