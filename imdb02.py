
"""
???

Alternativen zu IMDB:
 * https://www.omdbapi.com - offen, aber scheinbar keine lokalisierten Namen
 * https://www.themoviedb.org - offen, nur mit Anmeldung

Sources: 
 * https://cinemagoer.readthedocs.io/en/latest/
 * 
"""

import timeit

from imdb import helpers
from imdb import Cinemagoer

from dvd_list import read_titles_from_dvd_list


def get_german_title_from_id(ia, id):
    # get a movie from IMDB ID
    x = int(id.replace('tt', ''))
    searched_movie = ia.get_movie(x)
    original_title = searched_movie['title']
    overview = searched_movie['plot outline']
    print(overview)
    print(f'Originaltitel von IMDB: {original_title}')
    #searched_movie = helpers.get_byURL('https://www.imdb.com/title/tt0099423/')
    # show all information that are currently available for a movie
    #print(sorted(searched_movie.keys()))
    # show all information sets that can be fetched for a movie
    #print(searched_movie['title'], searched_movie['original title'],searched_movie['localized title'])
    #print(helpers.getAKAsInLanguage(searched_movie, 'de'))
    #german_title = searched_movie['title']
    for t in searched_movie['akas']:
        if 'Germany' in t:
            german_title = t.replace('(Germany)', '').strip()
            print(f'Deutscher Titel von IMDB: {german_title}')
            return german_title


def check_all_dvd_titles():
    ia = Cinemagoer()
    movies = 0
    fails = 0
    for title in read_titles_from_dvd_list():
        print(title)
        movies += 1
        german_title = get_german_title_from_id(ia, title[0])
        if german_title == None:
            fails += 1
            continue
        if title[2] != german_title:
            print(f'{title[2]} != {german_title}')
    print(f'Insgesamt {fails} fehlende deutsche Titel bei {movies} Filmen.')


if __name__ == '__main__':
    print(timeit.timeit('check_all_dvd_titles()', number=1, globals=globals()))
