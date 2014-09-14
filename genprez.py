#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#------------------  AnKoA  -----------------------#
#     Made with love by grm34 (FRIPOUILLEJACK)     #
#     ........fripouillejack@gmail.com .......     #
# Greetz: thibs, Rockweb, c0da, Hydrog3n, Speedy76 #
#--------------------------------------------------#

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

    #___ HELP ___#
    usage = "./genprez.py LANGUAGE QUALITY CODECS SUBS SIZE ID_IMDB"
    parser = optparse.OptionParser(usage = usage)
    (options, args) = parser.parse_args()
    if (len(args) != 6):
        parser.print_help()
        parser.exit(1)

    #___ VALUES ___#
    lang = sys.argv[1]
    qualite = sys.argv[2]
    format = sys.argv[3]
    sub = sys.argv[4]
    size = sys.argv[5]
    imdb = sys.argv[6]

    #___ CONNECT IMDB ___#
    searchIMDB = "http://deanclatworthy.com/imdb/?id=tt%s" % imdb
    try:
        data_IMDB = loads(urlopen(searchIMDB).read())
    except(HTTPError, ValueError):
        data_IMDB = ""
        pass

    #___ CONNECT TMDB ___#
    searchTMDB = "http://api.themoviedb.org/3/movie/tt%s?api_"\
                 "key=%s&language=fr" % (imdb, tmdb_api_key)
    dataTMDB = urllib2.Request(searchTMDB,
                               headers={"Accept": "application/json"})
    try:
        data_TMDB = loads(urllib2.urlopen(dataTMDB).read())
    except(HTTPError, ValueError):
        data_TMDB = ""
        pass

    #___ CONNECT OMDB ___#
    searchOMDB = "http://www.omdbapi.com/?i=tt%s" % imdb
    try:
        data_OMDB = loads(urlopen(searchOMDB).read())
    except(HTTPError, ValueError):
        data_OMDB = ""
        pass

    #---> Cover <---#
    cover_TMDB = "poster_path"
    cover_OMDB = "Poster"
    if (cover_TMDB in data_TMDB):
        post = "%s" % data_TMDB['poster_path']
        poster = "[img]https://d3gtl9l2a4fn1j.cloudfront.net/t/p/"\
                 "original"+post+"[/img]"
    else:
        if (cover_OMDB in data_OMDB):
            poster = "[img]%s[/img]" % data_OMDB['Poster']
        else:
            poster = "[img]N/A[/img]"

    #---> Overview <---#
    overview_TMDB = "overview"
    overview_OMDB = "Plot"
    if (overview_TMDB in data_TMDB):
        resp_TMDB = "%s" % data_TMDB['overview']
        if ("None" in resp_TMDB):
            if (overview_OMDB in data_OMDB):
                overview = "[i]%s[/i]" % data_OMDB['Plot']
            else:
                overview = "[i]N/A[/i]"
        else:
            overview = "[i]"+resp_TMDB+"[/i]"
    else:
        overview = "[i]N/A[/i]"

    #---> Title <---#
    title_IMDB = "title"
    title_TMDB = "original_title"
    title_OMDB = "Title"
    if (title_IMDB in data_IMDB):
        title = "[b][u]Title[/u] : [/b] [i]%s[/i]" % data_IMDB['title']
        dir = "%s" % data_IMDB['title']
    else:
        if (title_TMDB in data_TMDB):
            title = "[b][u]Title[/u] : [/b] [i]%s"\
                    "[/i]" % data_TMDB['original_title']
            dir = "%s" % data_TMDB['original_title']
        else:
            if (title_OMDB in data_OMDB):
                title = "[b][u]Title[/u] : [/b] [i]%s[/i]"\
                        % data_OMDB['Title']
                dir = "%s" % data_OMDB['Title']
            else:
                title = "[b][u]Title[/u] : [/b] [i]N/A[/i]"
                dir = "N/A"

    #---> Year <---#
    year_IMDB = "year"
    year_TMDB = "release_date"
    year_OMDB = "Year"
    if (year_IMDB in data_IMDB):
        year = "[b][u]Production Year[/u] : [/b] [i]%s[/i]"\
               % data_IMDB['year']
    else:
        if (year_OMDB in data_OMDB):
            year = "[b][u]Production Year[/u] : [/b] [i]%s"\
                   "[/i]" % data_OMDB['Year']
        else:
            if (year_TMDB in data_TMDB):
                year = "[b][u]Production Year[/u] : [/b] [i]%s"\
                       "[/i]" % data_TMDB['release_date']
            else:
                year = "[b][u]Production Year[/u] : [/b] [i]N/A[/i]"

    #---> Nationality <---#
    country_IMDB = "country"
    country_TMDB = "production_countries"
    if (country_IMDB in data_IMDB):
        country = "[b][u]Nationality[/u] : [/b] [i]%s[/i]"\
                  % data_IMDB['country']
    else:
        if (country_TMDB in data_TMDB):
            countryList = ""
            for country in data_TMDB['production_countries']:
                countryList += "%s, " % country['name']
            country = "[b][u]Nationality[/u] : [/b] [i]%s[/i]" % countryList
        else:
            country = "[b][u]Nationality[/u] : [/b] [i]N/A[/i]"

    #---> Genres <---#
    genre_IMDB = "genres"
    genre_TMDB = "genres"
    genre_OMDB = "Genre"
    if (genre_IMDB in data_IMDB):
        genres = "[b][u]Genre(s) :[/u][/b] [i]%s[/i]" % data_IMDB['genres']
    else:
        if (genre_TMDB in data_TMDB):
            genresList = ""
            for genres in data_TMDB['genres']:
                genresList += "%s, " % genres['name']
            genres = "[b][u]Genre(s) :[/u][/b] [i]%s[/i]" % genresList
        else:
            if (genre_OMDB in data_OMDB):
                genres = "[b][u]Genre(s) :[/u][/b] [i]%s"\
                         "[/i]" % data_OMDB['Genre']
            else:
                genres = "[b][u]Genre(s) :[/u][/b] [i]N/A[/i]"

    #---> Directors <---#
    director_TMDB = "production_companies"
    director_OMDB = "Director"
    if (director_OMDB in data_OMDB):
        directors = "[b][u]Director(s)[/u] : [/b] [i]%s"\
                    "[/i]" % data_OMDB['Director']
    else:
        if (director_TMDB in data_TMDB):
            directorsList = ""
            for production_companies in data_TMDB['production_companies']:
                directorsList += "%s, " % production_companies['name']
            directors = "[b][u]Director(s)[/u] : [/b] [i]%s"\
                        "[/i]" % directorsList
        else:
            directors = "[b][u]Director(s)[/u] : [/b] [i]N/A[/i]"

    #---> Runtime <---#
    runtime_IMDB = "runtime"
    runtime_TMDB = "runtime"
    runtime_OMDB = "Runtime"
    if (runtime_OMDB in data_OMDB):
        resp_OMDB = "%s" % data_OMDB['Runtime']
        if ("N/A" != resp_OMDB):
            runtime = "[b][u]Duration[/u] : [color=#980000][i]%s"\
                      "[/i][/color][/b]" % data_OMDB['Runtime']
        else:
            runtime = "[b][u]Duration[/u] : [color=#980000]"\
                      "[i]N/A[/i][/color][/b]"
    else:
        if (runtime_IMDB in data_IMDB):
            runtime = "[b][u]Duration[/u] : [color=#980000]"\
                      "[i]%s[/i][/color][/b]" % data_IMDB['runtime']
        else:
            if (runtime_TMDB in data_TMDB):
                rsp_TMDB = "%s" % data_TMDB[runtime]
                if ("0" != rsp_TMDB):
                    runtime = "[b][u]Duration[/u] : [color=#980000]"\
                              "[i]%s[/i][/color][/b]" % data_TMDB['runtime']
                else:
                    runtime = "[b][u]Duration[/u] : [color=#980000]"\
                              "[i]N/A[/i][/color][/b]"
            else:
                runtime = "[b][u]Duration[/u] : [color=#980000]"\
                          "[i]N/A[/i][/color][/b]"

    #---> Actors <---#
    actors_OMDB = "Actors"
    if (actors_OMDB in data_OMDB):
        actors = "[spoil=Casting][i]%s[/i][/spoil]" % data_OMDB['Actors']
    else:
        actors = "[spoil=Casting][i]N/A[/i][/spoil]"

    #---> Rating <---#
    rating_IMDB = "rating"
    rating_TMDB = "vote_average"
    rating_OMDB = "imdbRating"
    if (rating_IMDB in data_IMDB):
        rating = "[b][u]IMDB Rating[/u] : [/b] [i]%s[/i]"\
                 % data_IMDB['rating']
    else:
        if (rating_OMDB in data_OMDB):
            rating = "[b][u]IMDB Rating[/u] : [/b] [i]%s"\
                     "[/i]" % data_OMDB['imdbRating']
        else:
            if (rating_TMDB in data_TMDB):
                rating = "[b][u]IMDB Rating[/u] : [/b] [i]%s"\
                         "[/i]" % data_TMDB['vote_average']
            else:
                rating = "[b][u]IMDB Rating[/u] : [/b] [i]N/A[/i]"

    #---> DATAS <---#
    imdbLink = "[b][u]IMDB Link[/u] :[/b] [i]"\
               "http://www.imdb.com/title/tt%s[/i]" % imdb
    prezQualite = "[b][u]Quality[/u] :[/b] [i]%s[/i]" % qualite
    prezFormat = "[b][u]Codecs[/u] : [color=#980000]"\
                 "[i]%s[/i][/color][/b]" % format
    prezLang = "[b][u]Language(s)[/u] : [/b] [i]%s[/i]" % lang
    prezSub = "[b][u]Subtitles[/u] : [/b] [i]%s[/i][/size]" % sub
    prezSize = "[size=6][color=#980000][b]%s[/b][/color][/size]" % size
    font = "[center][size=4]\n"
    name = dir.replace(' ', '.').replace('/', '').replace('(', '')\
              .replace(')', '').replace('"', '').replace(':', '')\
              .replace("'", "").replace("[", "").replace("]", "")\
              .replace(";", "").replace(",", "")

     #---> GENPREZ <---#
    prez = "%s\n%s\n\n[img]http://fripouillejack.free.fr/synop.png[/img]"\
           "\n\n%s\n\n" % (font, poster, overview)
    prez += "[img]http://fripouillejack.free.fr/movie.png[/img]"\
            "\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n"\
            % (title, year, country, genres, directors, runtime,
               actors, rating, imdbLink)
    prez += "[img]http://fripouillejack.free.fr/thumbs.png[/img]\n\n"
    prez += "[spoil=Click Here][img]thumbnails_link[/img][/spoil]\n\n"
    prez += "[img]http://fripouillejack.free.fr/upload.png[/img]"\
            "\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s[/center]"\
            % (prezQualite, prezFormat, prezLang, prezSub, prezSize)

    if (title_TMDB not in data_TMDB and title_IMDB not in data_IMDB\
            and title_OMDB not in data_OMDB):
        print (GREEN+"\n -> "+BLUE+"Genprez ERROR : "+RED+"Movie not found"\
               ", please try again !\n"+END)
    else:
        #---> WRITE <---#
        temp = sys.stdout
        sys.stdout = open(thumb+name+'_prez.txt','w')
        print prez.encode('utf-8')
        sys.stdout.close()
        sys.stdout = temp

if (__name__ == "__main__"):
    main()