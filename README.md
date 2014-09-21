AnkoA v3.2.0
=====

**FFMPEG Command Line Easy Encoding Tools ...** [Video Demo](https://www.youtube.com/watch?v=RvEIvgnXdBg&feature=youtu.be)

![AnkoA](http://i.imgur.com/BlG3BNs.png)


## Description :

* FFMPEG easy encoding
* Thumbnails Generator
* NFO Generator
* Genprez Upload
* Auto make .torrent


## How to install AnkoA ?

Take a tour on the [wiki](https://github.com/grm34/AnkoA/wiki/AnkoA-Wiki) !

Chan IRC : **irc.bakaserv.net/6667 #AnkoA**


## Usage :

* Easy encoding tool :
`./ankoa.py`

* Thumbnails generator :
`./thumbnails source.video 5 2`

* Upload thumbnails on imgur :
`./imgur.py thumbnails.png`

* Genprez :
`./genprez.py LANGUAGE QUALITY CODECS SUBS SIZE ID_IMDB`

* NFO generator :
`./nfogen.sh source.video SOURCE SUBS SUBFORCED URL`
 
* Thumbs+nfo+torrent :
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

***
## Version :

Take a tour on the [changelog](https://github.com/grm34/AnkoA/wiki/changelog) !

#### Thanks for assistance and contributions :

* [@thibs](https://github.com/thibs7777777)
* [@Rockweb](https://github.com/Rockweb)
* [@c0ding](https://github.com/c0ding)
* [@Hydrog3n](https://github.com/Hydrog3n)
* [@speedy76](https://github.com/speedy76)

***
### Links :

* [AnkoA wiki](https://github.com/grm34/AnkoA/wiki/AnkoA-Wiki)
* [AnkoA changelog](https://github.com/grm34/AnkoA/wiki/Changelog)
* [Compile Multimedia Environment](https://github.com/grm34/AnkoA/wiki/Compile-Multimedia-Environment)
* [Video demonstration](https://www.youtube.com/watch?v=RvEIvgnXdBg&feature=youtu.be)

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
    
	Filename:    Source:    Comment:    Both:    Blank:    Total:

	nfo.php           32          39       21        20       112
	ankoa.py        1159          60       25       160      1404
	genprez.py       271          62        7        35       375
	imgur.py          40          43        0         6        89
	make.py           34          43        0        11        88
	setup.py          42          46        0        13       101
	thumbnails.py    167          43       18        35       263
	bitrate.py        36          43        0         9        88
	settings.py       10          55        0         5        70
	style.py          14          67        5         6        92
	nfogen.sh         15          41        1         4        61

	[Total] :       1820         542       77       304      2743
	
***
### Preview (older version) :

![Preview](http://i.imgur.com/kGjj63X.png)

    Don't be afraid, as you can see on the preview, x264 Expert Mode is on...
    When you select off, x264 params will be controlled by the preset & tune.
    In this case, all expert questions will be skipped !
    This option is only for advanced encoders...

***
