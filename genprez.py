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

import sys
import json
import socket
import urllib2
import optparse
from json import loads
from django.utils.encoding import (smart_str, smart_unicode)
from urllib2 import (Request, urlopen, URLError, HTTPError, unquote)
from app.main.events import (genprez_help, genprez_success,
                             genprez_error, genprez_process)
from user.settings import option

(folder, thumb, tag, team, announce, tmdb_api_key, tag_thumb) = option()


def api_connexion(imdb):

    # CONNECT IMDB
    searchIMDB = "http://deanclatworthy.com/imdb/?id=tt{0}"\
                 .format(imdb)
    try:
        data_IMDB = loads(urlopen(searchIMDB, None, 5.0).read())
    except(HTTPError, ValueError, URLError):
        data_IMDB = ""
        pass
    except socket.timeout:
        data_IMDB = ""
        pass

    # CONNECT TMDB
    searchTMDB = "http://api.themoviedb.org/3/movie/tt{0}?api_"\
                 "key={1}&language=fr".format(imdb, tmdb_api_key)
    dataTMDB = urllib2.Request(searchTMDB,
                               headers={"Accept": "application/json"})
    try:
        data_TMDB = loads(urllib2.urlopen(dataTMDB, None, 5.0).read())
    except(HTTPError, ValueError, URLError):
        data_TMDB = ""
        pass
    except socket.timeout:
        data_TMDB = ""
        pass

    # CONNECT OMDB
    searchOMDB = "http://www.omdbapi.com/?i=tt{0}".format(imdb)
    try:
        data_OMDB = loads(urlopen(searchOMDB, None, 5.0).read())
    except(HTTPError, ValueError, URLError):
        data_OMDB = ""
        pass
    except socket.timeout:
        data_OMDB = ""
        pass

    # CONNECT MyAPI
    searchAPI = "http://www.myapifilms.com/imdb?idIMDB=tt{0}&format="\
                "JSON&aka=0&business=0&seasons=0&seasonYear=0&techni"\
                "cal=0&lang=en-us&actors=F&biography=0&trailer=1&uni"\
                "queName=0&filmography=0&bornDied=0&starSign=0&actor"\
                "Actress=1&actorTrivia=0&movieTrivia=0".format(imdb)
    try:
        data_API = loads(urlopen(searchAPI, None, 5.0).read())
    except(HTTPError, ValueError, URLError):
        data_API = ""
        pass
    except socket.timeout:
        data_API = ""
        pass

    return (data_IMDB, data_TMDB, data_OMDB, data_API)


def main():

    # HELP
    usage = genprez_help()
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

    genprez_process()
    (data_IMDB, data_TMDB, data_OMDB, data_API) = api_connexion(imdb)

    # Set some values
    [countryList, genresList, directorsList,
     runtimeList, actorsList] = ["", ] * 5

    # Cover
    [cover_TMDB, cover_OMDB,
     cover_API] = ["poster_path", "Poster", "urlPoster"]

    if (cover_TMDB in data_TMDB):
        poster = "[img]https://d3gtl9l2a4fn1j.cloudfront.net/t/p/"\
                 "original{0}[/img]"\
                 .format(smart_str(data_TMDB['poster_path']))
    elif (cover_OMDB in data_OMDB):
        poster = "[img]{0}[/img]".format(smart_str(data_OMDB['Poster']))
    elif (cover_API in data_API):
        poster = "[img]{0}[/img]".format(smart_str(data_API['urlPoster']))
    else:
        poster = "[img]N/A[/img]"

    # Overview
    [overview_TMDB, overview_OMDB, overview_API] = ["overview", "Plot", "plot"]

    if (overview_TMDB in data_TMDB and "None" not in data_TMDB['overview']):
        overview = "[i]{0}[/i]".format(smart_str(data_TMDB['overview']))
    elif (overview_OMDB in data_OMDB):
        overview = "[i]{0}[/i]".format(smart_str(data_OMDB['Plot']))
    elif (overview_API in data_API):
        overview = "[i]{0}[/i]".format(smart_str(data_API['plot']))
    else:
        overview = "[i]N/A[/i]"

    # Title
    [title_IMDB, title_TMDB, title_OMDB,
     title_API] = ["title", "original_title", "Title", "title"]

    if (title_IMDB in data_IMDB):
        dir = "{0}".format(smart_str(data_IMDB['title']))
        title = "[b][u]Title[/u] : [/b] [i]{0}[/i]".format(dir)
    elif (title_TMDB in data_TMDB):
        dir = "{0}".format(smart_str(data_TMDB['original_title']))
        title = "[b][u]Title[/u] : [/b] [i]{0}[/i]".format(dir)
    elif (title_OMDB in data_OMDB):
        dir = "{0}".format(smart_str(data_OMDB['Title']))
        title = "[b][u]Title[/u] : [/b] [i]{0}[/i]".format(dir)
    elif (title_API in data_API):
        dir = "{0}".format(smart_str(data_API['title']))
        title = "[b][u]Title[/u] : [/b] [i]{0}[/i]".format(dir)
    else:
        dir = "N/A"
        title = "[b][u]Title[/u] : [/b] [i]N/A[/i]"

    # Year
    [year_IMDB, year_API] = ["year", ] * 2
    [year_TMDB, year_OMDB] = ["release_date", "Year"]

    if (year_IMDB in data_IMDB):
        year = "[b][u]Production Year[/u] : [/b] [i{0}[/i]"\
               .format(smart_str(data_IMDB['year']))
    elif (year_OMDB in data_OMDB):
        year = "[b][u]Production Year[/u] : [/b] [i]{0}[/i]"\
               .format(smart_str(data_OMDB['Year']))
    elif (year_TMDB in data_TMDB):
        year = "[b][u]Production Year[/u] : [/b] [i]{0}[/i]"\
               .format(smart_str(data_TMDB['release_date']))
    elif (year_API in data_API):
        year = "[b][u]Production Year[/u] : [/b] [i]{0}[/i]"\
               .format(smart_str(data_API['year']))
    else:
        year = "[b][u]Production Year[/u] : [/b] [i]N/A[/i]"

    # Nationality
    [country_IMDB, country_TMDB, country_API,
     country_OMDB] = ["country", "production_countries",
                      "countries", "Country"]

    if (country_IMDB in data_IMDB):
        country = "[b][u]Nationality[/u] : [/b] [i]{0}[/i]"\
                  .format(smart_str(data_IMDB['country']))
    elif (country_API in data_API):
        for item in data_API['countries']:
            countryList += "{0}, ".format(smart_str(item))
        country = "[b][u]Nationality[/u] : [/b] [i]{0}[/i]"\
                  .format(countryList)
    elif (country_TMDB in data_TMDB):
        for item in data_TMDB['production_countries']:
            countryList += "{0}, ".format(smart_str(item['name']))
        country = "[b][u]Nationality[/u] : [/b] [i]{0}[/i]"\
                  .format(countryList)
    elif (country_OMDB in data_OMDB):
        country = "[b][u]Nationality[/u] : [/b] [i]{0}[/i]"\
                  .format(smart_str(data_OMDB['Country']))
    else:
        country = "[b][u]Nationality[/u] : [/b] [i]N/A[/i]"

    # Genres
    [genre_IMDB, genre_TMDB, genre_API] = ["genres", ] * 3
    genre_OMDB = "Genre"

    if (genre_IMDB in data_IMDB):
        genres = "[b][u]Genre(s) :[/u][/b] [i]{0}[/i]"\
                 .format(smart_str(data_IMDB['genres']))
    elif (genre_TMDB in data_TMDB):
        for item in data_TMDB['genres']:
            genresList += "{0}, ".format(smart_str(item['name']))
        genres = "[b][u]Genre(s) :[/u][/b] [i]{0}[/i]".format(genresList)
    elif (genre_OMDB in data_OMDB):
        genres = "[b][u]Genre(s) :[/u][/b] [i]{0}[/i]"\
                 .format(smart_str(data_OMDB['Genre']))
    elif (genre_API in data_API):
        for item in data_API['genres']:
            genresList += "{0}, ".format(smart_str(item))
        genres = "[b][u]Genre(s) :[/u][/b] [i]{0}[/i]".format(genresList)
    else:
        genres = "[b][u]Genre(s) :[/u][/b] [i]N/A[/i]"

    # Directors
    [director_TMDB, director_OMDB,
     director_API] = ["production_companies", "Director", "directors"]

    if (director_OMDB in data_OMDB):
        directors = "[b][u]Director(s)[/u] : [/b] [i]{0}[/i]"\
                    .format(smart_str(data_OMDB['Director']))
    elif (director_API in data_API):
        for item in data_API['directors']:
            directorsList += "{0}, ".format(smart_str(item['name']))
        directors = "[b][u]Director(s)[/u] : [/b] [i]{0}[/i]"\
                    .format(directorsList)
    elif (director_TMDB in data_TMDB):
        for item in data_TMDB['production_companies']:
            directorsList += "{0}, ".format(smart_str(item['name']))
        directors = "[b][u]Director(s)[/u] : [/b] [i]{0}[/i]"\
                    .format(directorsList)
    else:
        directors = "[b][u]Director(s)[/u] : [/b] [i]N/A[/i]"

    # Runtime
    [runtime_IMDB, runtime_TMDB, runtime_API] = ["runtime", ] * 3
    runtime_OMDB = "Runtime"

    if (runtime_OMDB in data_OMDB and "N/A" != data_OMDB['Runtime']):
        runtime = "[b][u]Duration[/u] : [color=#980000][i]{0}"\
                  "[/i][/color][/b]".format(smart_str(data_OMDB['Runtime']))
    elif (runtime_API in data_API):
        for item in data_API['runtime']:
            runtimeList += "{0}, ".format(smart_str(item))
        runtime = "[b][u]Duration[/u] : [color=#980000]"\
                  "[i]{0}[/i][/color][/b]".format(runtimeList)
    elif (runtime_IMDB in data_IMDB):
        runtime = "[b][u]Duration[/u] : [color=#980000]"\
                  "[i]{0}[/i][/color][/b]"\
                  .format(smart_str(data_IMDB['runtime']))
    elif (runtime_TMDB in data_TMDB and "0" != data_TMDB['runtime']):
        runtime = "[b][u]Duration[/u] : [color=#980000]"\
                  "[i]{0}[/i][/color][/b]"\
                  .format(smart_str(data_TMDB['runtime']))
    else:
        runtime = "[b][u]Duration[/u] : [color=#980000]"\
                  "[i]N/A[/i][/color][/b]"

    # Actors
    [actors_OMDB, actors_API] = ["Actors", "actors"]

    if (actors_API in data_API):
        for item in data_API['actors']:
            actorsList += "{0}, ".format(smart_str(item['actorName']))
        actors = "[spoil=Casting][i]{0}[/i][/spoil]".format(actorsList)
    elif (actors_OMDB in data_OMDB):
        actors = "[spoil=Casting][i]{0}[/i][/spoil]"\
                 .format(smart_str(data_OMDB['Actors']))
    else:
        actors = "[spoil=Casting][i]N/A[/i][/spoil]"

    # Rating
    [rating_IMDB, rating_TMDB, rating_OMDB,
     rating_API] = ["rating", "vote_average", "imdbRating", "rating"]

    if (rating_IMDB in data_IMDB):
        rating = "[b][u]IMDB Rating[/u] : [/b] [i]{0}[/i]"\
                 .format(smart_str(data_IMDB['rating']))
    elif (rating_OMDB in data_OMDB):
        rating = "[b][u]IMDB Rating[/u] : [/b] [i]{0}[/i]"\
                 .format(smart_str(data_OMDB['imdbRating']))
    elif (rating_TMDB in data_TMDB):
        rating = "[b][u]IMDB Rating[/u] : [/b] [i]{0}[/i]"\
                 .format(smart_str(data_TMDB['vote_average']))
    elif (rating_API in data_API):
        rating = "[b][u]IMDB Rating[/u] : [/b] [i]{0}[/i]"\
                 .format(smart_str(data_API['rating']))
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
    prezSize = "[size=6][color=#980000][b]{0}[/b][/color][/size]"\
               .format(size)
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

    # VERIFICATION
    if (title_TMDB not in data_TMDB and title_IMDB not in data_IMDB
            and title_OMDB not in data_OMDB and title_API not in data_API):
        genprez_error()

    # if ok -> WRITE
    else:
        temp = sys.stdout
        sys.stdout = open('{0}{1}_prez.txt'.format(thumb, name), 'w')
        print smart_str(prez)
        sys.stdout.close()
        sys.stdout = temp
        genprez_success()

if (__name__ == "__main__"):
    main()
