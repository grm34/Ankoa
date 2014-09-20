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

import sys
import json
import optparse
import urllib2
from json import loads
from urllib2 import (Request, urlopen, URLError, HTTPError, unquote)
from pprint import pprint
sys.path.append("app/")
from settings import option
from style import color

(folder, thumb, tag, team, announce, tmdb_api_key, tag_thumb) = option()
(BLUE, RED, YELLOW, GREEN, END) = color()


def main():

    # HELP
    usage = "./genprez.py LANGUAGE QUALITY CODECS SUBS SIZE ID_IMDB"
    parser = optparse.OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    if (len(args) != 6):
        parser.print_help()
        parser.exit(1)

    # VALUES
    lang = sys.argv[1]
    qualite = sys.argv[2]
    format = sys.argv[3]
    sub = sys.argv[4]
    size = sys.argv[5]
    imdb = sys.argv[6]

    # CONNECT IMDB
    searchIMDB = "http://deanclatworthy.com/imdb/?id=tt{0}"\
                 .format(imdb)
    try:
        data_IMDB = loads(urlopen(searchIMDB).read())
    except(HTTPError, ValueError, URLError):
        data_IMDB = ""
        pass

    # CONNECT TMDB
    searchTMDB = "http://api.themoviedb.org/3/movie/tt{0}?api_"\
                 "key={1}&language=fr".format(imdb, tmdb_api_key)
    dataTMDB = urllib2.Request(searchTMDB,
                               headers={"Accept": "application/json"})
    try:
        data_TMDB = loads(urllib2.urlopen(dataTMDB).read())
    except(HTTPError, ValueError, URLError):
        data_TMDB = ""
        pass

    # CONNECT OMDB
    searchOMDB = "http://www.omdbapi.com/?i=tt{0}".format(imdb)
    try:
        data_OMDB = loads(urlopen(searchOMDB).read())
    except(HTTPError, ValueError, URLError):
        data_OMDB = ""
        pass

    # CONNECT MyAPI
    searchAPI = "http://www.myapifilms.com/imdb?idIMDB=tt{0}&format="\
                "JSON&aka=0&business=0&seasons=0&seasonYear=0&techni"\
                "cal=0&lang=en-us&actors=F&biography=0&trailer=1&uni"\
                "queName=0&filmography=0&bornDied=0&starSign=0&actor"\
                "Actress=1&actorTrivia=0&movieTrivia=0".format(imdb)
    try:
        data_API = loads(urlopen(searchAPI).read())
    except(HTTPError, ValueError, URLError):
        data_API = ""
        pass

    # Cover
    cover_TMDB = "poster_path"
    cover_OMDB = "Poster"
    cover_API = "urlPoster"

    if (cover_TMDB in data_TMDB):
        poster = "[img]https://d3gtl9l2a4fn1j.cloudfront.net/t/p/"\
                 "original{0}[/img]".format(data_TMDB['poster_path'])
    elif (cover_OMDB in data_OMDB):
        poster = "[img]{0}[/img]".format(data_OMDB['Poster'])
    elif (cover_API in data_API):
        poster = "[img]{0}[/img]".format(data_API['urlPoster'])
    else:
        poster = "[img]N/A[/img]"

    # Overview
    overview_TMDB = "overview"
    overview_OMDB = "Plot"
    overview_API = "plot"

    if (overview_TMDB in data_TMDB and "None" not in data_TMDB['overview']):
        overview = "[i]{0}[/i]".format(data_TMDB['overview'])
    elif (overview_OMDB in data_OMDB):
        overview = "[i]{0}[/i]".format(data_OMDB['Plot'])
    elif (overview_API in data_API):
        overview = "[i]{0}[/i]".format(data_API['plot'])
    else:
        overview = "[i]N/A[/i]"

    # Title
    title_IMDB = "title"
    title_TMDB = "original_title"
    title_OMDB = "Title"
    title_API = "title"

    if (title_IMDB in data_IMDB):
        dir = "{0}".format(data_IMDB['title'])
        title = "[b][u]Title[/u] : [/b] [i]{0}[/i]".format(dir)
    elif (title_TMDB in data_TMDB):
        dir = "{0}".format(data_TMDB['original_title'])
        title = "[b][u]Title[/u] : [/b] [i]{0}[/i]".format(dir)
    elif (title_OMDB in data_OMDB):
        dir = "{0}".format(data_OMDB['Title'])
        title = "[b][u]Title[/u] : [/b] [i]{0}[/i]".format(dir)
    elif (title_API in data_API):
        dir = "{0}".format(data_API['title'])
        title = "[b][u]Title[/u] : [/b] [i]{0}[/i]".format(dir)
    else:
        dir = "N/A"
        title = "[b][u]Title[/u] : [/b] [i]N/A[/i]"

    # Year
    year_IMDB = "year"
    year_TMDB = "release_date"
    year_OMDB = "Year"
    year_API = "year"

    if (year_IMDB in data_IMDB):
        year = "[b][u]Production Year[/u] : [/b] [i{0}[/i]"\
               .format(data_IMDB['year'])
    elif (year_OMDB in data_OMDB):
        year = "[b][u]Production Year[/u] : [/b] [i]{0}[/i]"\
               .format(data_OMDB['Year'])
    elif (year_TMDB in data_TMDB):
        year = "[b][u]Production Year[/u] : [/b] [i]{0}[/i]"\
               .format(data_TMDB['release_date'])
    elif (year_API in data_API):
        year = "[b][u]Production Year[/u] : [/b] [i]{0}[/i]"\
               .format(data_API['year'])
    else:
        year = "[b][u]Production Year[/u] : [/b] [i]N/A[/i]"

    # Nationality
    country_IMDB = "country"
    country_TMDB = "production_countries"
    country_API = "countries"
    country_OMDB = "Country"

    if (country_IMDB in data_IMDB):
        country = "[b][u]Nationality[/u] : [/b] [i]{0}[/i]"\
                  .format(data_IMDB['country'])
    elif (country_API in data_API):
        countryList = ""
        for item in data_API['countries']:
            countryList += "{0}, ".format(item)
        country = "[b][u]Nationality[/u] : [/b] [i]{0}[/i]".format(countryList)
    elif (country_TMDB in data_TMDB):
        countryList = ""
        for item in data_TMDB['production_countries']:
            countryList += "{0}, ".format(item['name'])
        country = "[b][u]Nationality[/u] : [/b] [i]{0}[/i]".format(countryList)
    elif (country_OMDB in data_OMDB):
        country = "[b][u]Nationality[/u] : [/b] [i]{0}[/i]"\
                  .format(data_OMDB['Country'])
    else:
        country = "[b][u]Nationality[/u] : [/b] [i]N/A[/i]"

    # Genres
    genre_IMDB = "genres"
    genre_TMDB = "genres"
    genre_OMDB = "Genre"
    genre_API = "genres"

    if (genre_IMDB in data_IMDB):
        genres = "[b][u]Genre(s) :[/u][/b] [i]{0}[/i]"\
                 .format(data_IMDB['genres'])
    elif (genre_TMDB in data_TMDB):
        genresList = ""
        for item in data_TMDB['genres']:
            genresList += "{0}, ".format(item['name'])
        genres = "[b][u]Genre(s) :[/u][/b] [i]{0}[/i]".format(genresList)
    elif (genre_OMDB in data_OMDB):
        genres = "[b][u]Genre(s) :[/u][/b] [i]{0}[/i]"\
                 .format(data_OMDB['Genre'])
    elif (genre_API in data_API):
        genresList = ""
        for item in data_API['genres']:
            genresList += "{0}, ".format(item)
        genres = "[b][u]Genre(s) :[/u][/b] [i]{0}[/i]".format(genresList)
    else:
        genres = "[b][u]Genre(s) :[/u][/b] [i]N/A[/i]"

    # Directors
    director_TMDB = "production_companies"
    director_OMDB = "Director"
    director_API = "directors"

    if (director_OMDB in data_OMDB):
        directors = "[b][u]Director(s)[/u] : [/b] [i]{0}[/i]"\
                    .format(data_OMDB['Director'])
    elif (director_API in data_API):
        directorsList = ""
        for item in data_API['directors']:
            directorsList += "{0}, ".format(item['name'])
        directors = "[b][u]Director(s)[/u] : [/b] [i]{0}[/i]"\
                    .format(directorsList)
    elif (director_TMDB in data_TMDB):
        directorsList = ""
        for item in data_TMDB['production_companies']:
            directorsList += "{0}, ".format(item['name'])
        directors = "[b][u]Director(s)[/u] : [/b] [i]{0}[/i]"\
                    .format(directorsList)
    else:
        directors = "[b][u]Director(s)[/u] : [/b] [i]N/A[/i]"

    # Runtime
    runtime_IMDB = "runtime"
    runtime_TMDB = "runtime"
    runtime_OMDB = "Runtime"
    runtime_API = "runtime"

    if (runtime_OMDB in data_OMDB and "N/A" != data_OMDB['Runtime']):
        runtime = "[b][u]Duration[/u] : [color=#980000][i]{0}"\
                  "[/i][/color][/b]".format(data_OMDB['Runtime'])
    elif (runtime_API in data_API):
        runtimeList = ""
        for item in data_API['runtime']:
            runtimeList += "{0}, ".format(item)
        runtime = "[b][u]Duration[/u] : [color=#980000]"\
                  "[i]{0}[/i][/color][/b]".format(runtimeList)
    elif (runtime_IMDB in data_IMDB):
        runtime = "[b][u]Duration[/u] : [color=#980000]"\
                  "[i]{0}[/i][/color][/b]".format(data_IMDB['runtime'])
    elif (runtime_TMDB in data_TMDB and "0" != data_TMDB['runtime']):
        runtime = "[b][u]Duration[/u] : [color=#980000]"\
                  "[i]{0}[/i][/color][/b]".format(data_TMDB['runtime'])
    else:
        runtime = "[b][u]Duration[/u] : [color=#980000]"\
                  "[i]N/A[/i][/color][/b]"

    # Actors
    actors_OMDB = "Actors"
    actors_API = "actors"

    if (actors_API in data_API):
        actorsList = ""
        for item in data_API['actors']:
            actorsList += "{0}, ".format(item['actorName'])
        actors = "[spoil=Casting][i]{0}[/i][/spoil]".format(actorsList)
    elif (actors_OMDB in data_OMDB):
        actors = "[spoil=Casting][i]{0}[/i][/spoil]"\
                 .format(data_OMDB['Actors'])
    else:
        actors = "[spoil=Casting][i]N/A[/i][/spoil]"

    # Rating
    rating_IMDB = "rating"
    rating_TMDB = "vote_average"
    rating_OMDB = "imdbRating"
    rating_API = "rating"

    if (rating_IMDB in data_IMDB):
        rating = "[b][u]IMDB Rating[/u] : [/b] [i]{0}[/i]"\
                 .format(data_IMDB['rating'])
    elif (rating_OMDB in data_OMDB):
        rating = "[b][u]IMDB Rating[/u] : [/b] [i]{0}[/i]"\
                 .format(data_OMDB['imdbRating'])
    elif (rating_TMDB in data_TMDB):
        rating = "[b][u]IMDB Rating[/u] : [/b] [i]{0}[/i]"\
                 .format(data_TMDB['vote_average'])
    elif (rating_API in data_API):
        rating = "[b][u]IMDB Rating[/u] : [/b] [i]{0}[/i]"\
                 .format(data_API['rating'])
    else:
        rating = "[b][u]IMDB Rating[/u] : [/b] [i]N/A[/i]"

    # DATAS
    imdbLink = "[b][u]IMDB Link[/u] :[/b] [i]"\
               "http://www.imdb.com/title/tt{0}[/i]".format(imdb)
    prezQualite = "[b][u]Quality[/u] :[/b] [i]{0}[/i]".format(qualite)
    prezFormat = "[b][u]Codecs[/u] : [color=#980000]"\
                 "[i]{0}[/i][/color][/b]".format(format)
    prezLang = "[b][u]Language(s)[/u] : [/b] [i]{0}[/i]".format(lang)
    prezSub = "[b][u]Subtitles[/u] : [/b] [i]{0}[/i][/size]".format(sub)
    prezSize = "[size=6][color=#980000][b]{0}[/b][/color][/size]".format(size)
    font = "[center][size=4]\n"
    name = dir.replace(' ', '.').replace('/', '').replace('(', '')\
              .replace(')', '').replace('"', '').replace(':', '')\
              .replace("'", "").replace("[", "").replace("]", "")\
              .replace(";", "").replace(",", "")

    # GENPREZ
    prez = "{0}\n{1}\n\n[img]http://fripouillejack.free.fr/synop.png[/img]"\
           "\n\n{2}\n\n".format(font, poster, overview)
    prez += "[img]http://fripouillejack.free.fr/movie.png[/img]"\
            "\n\n{0}\n\n{1}\n\n{2}\n\n{3}\n\n{4}\n\n{5}\n\n{6}\n\n{7}\n\n{8}"\
            "\n\n".format(title, year, country, genres, directors, runtime,
                          actors, rating, imdbLink)
    prez += "[img]http://fripouillejack.free.fr/thumbs.png[/img]\n\n"
    prez += "[spoil=Click Here][img]thumbnails_link[/img][/spoil]\n\n"
    prez += "[img]http://fripouillejack.free.fr/upload.png[/img]"\
            "\n\n{0}\n\n{1}\n\n{2}\n\n{3}\n\n{4}[/center]"\
            .format(prezQualite, prezFormat, prezLang, prezSub, prezSize)

    if (title_TMDB not in data_TMDB and title_IMDB not in data_IMDB
            and title_OMDB not in data_OMDB and title_API not in data_API):
        print ("\n{0} -> {1}Genprez ERROR : {2}Movie not found, please try "
               "again !\n{3}".format(GREEN, BLUE, RED, END))
    else:
        # WRITE
        temp = sys.stdout
        sys.stdout = open('{0}{1}_prez.txt'.format(thumb, name), 'w')
        print prez.encode('utf-8')
        sys.stdout.close()
        sys.stdout = temp

if (__name__ == "__main__"):
    main()
