
"""
Translate all titles from LibreOffice Calc list.

Sources:
 * https://github.com/celiao/tmdbsimple/
 * https://pypi.org/project/pyexcel-ods3/
 * https://developers.themoviedb.org/3/getting-started/introduction
"""


import timeit

import tmdbsimple as tmdb

from dvd_list import read_titles_from_dvd_list


api_key_v3 = ''
api_key_v4 = ''
tmdb.API_KEY = api_key_v3


def get_german_info_for_id(id):
    movie = tmdb.Movies(id)
    x = movie.info(language='DE', append_to_response='alternative_titles')
    overview = x['overview']
    for t in x['alternative_titles']['titles']:
        # TODO: check if there could be more than one German title
        if 'iso_3166_1' in t and t['iso_3166_1'] in ('DE', 'CH', 'AT'):
            return t['title'], overview
    return None, None


def check_all_dvd_titles():
    movies = 0
    fails = 0
    for title in read_titles_from_dvd_list():
        #print(title)
        movies += 1
        german_title, overview = get_german_info_for_id(title[0])
        if german_title == None:
            fails += 1
            continue
        if title[2] != german_title:
            print(f'{title[2]} != {german_title}')
    print(f'Insgesamt {fails} fehlende deutsche Titel bei {movies} Filmen.')


if __name__ == '__main__':
    print(timeit.timeit('check_all_dvd_titles()', number=1, globals=globals()))
