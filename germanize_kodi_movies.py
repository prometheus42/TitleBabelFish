
import csv
import json
from xml.sax.saxutils import escape

import requests
import tmdbsimple as tmdb
from rich.progress import track
from rich.table import Table
from rich.console import Console
from rich import print as rprint


cfg_server = ''
cfg_port = 8080
cfg_username = ''
cfg_password = ''

tmdb.API_KEY = ''


def get_german_info_for_id(id):
    movie = tmdb.Movies(id)
    try:
        x = movie.info(language='DE', append_to_response='alternative_titles')
    except requests.exceptions.HTTPError as e:
        # print(e)
        return None, None, None
    tmdb_id = x['id']
    overview = x['overview']
    for t in x['alternative_titles']['titles']:
        # TODO: check if there could be more than one German title
        if 'iso_3166_1' in t and t['iso_3166_1'] in ('DE', 'CH', 'AT'):
            return t['title'], overview, tmdb_id
    return None, overview, tmdb_id


def rpc(method, params={}):
    rpc_req = {'jsonrpc': '2.0', 'method': method, 'params': params, 'id': 1}
    r = requests.get('http://{}:{}/jsonrpc'.format(cfg_server, cfg_port),
                     params={'request': json.dumps(rpc_req)}, auth=(cfg_username, cfg_password))
    return r.json()['result']


def get_movies_filtered(filter):
    props = ['file', 'title', 'runtime']
    props += ['genre', 'year', 'rating', 'country']
    props += ['originaltitle', 'sorttitle']
    props += ['imdbnumber']
    props += ['streamdetails']
    r = rpc('VideoLibrary.GetMovies', params={
            'properties': props, 'filter': filter})
    return r


def get_movies_unfiltered():
    props = ['file', 'title', 'runtime']
    props += ['genre', 'year', 'rating', 'country']
    props += ['originaltitle', 'sorttitle']
    props += ['imdbnumber']
    props += ['streamdetails']
    r = rpc('VideoLibrary.GetMovies', params={'properties': props})
    return r


def germanize_kodi_movies():
    mlist = []
    nogerman = []
    response = get_movies_unfiltered()
    for movie in track(response['movies'], description='Downloading movie infos from TMDB...'):
        imdb_id = movie['imdbnumber']
        german_title, german_desc, tmdb_id = get_german_info_for_id(imdb_id)
        if not german_title and not german_desc:
            print(
                f'Error downloading information about: {movie["title"]} ({imdb_id})')
        if not german_title:
            nogerman.append(
                (movie['title'], imdb_id, f'https://www.imdb.com/title/{imdb_id}/', str(tmdb_id), f'https://www.themoviedb.org/movie/{tmdb_id}'))
        movie['german_title'] = german_title if german_title else movie['title']
        movie['german_descr'] = german_desc if german_desc else ''
        mlist.append(movie)
    return mlist, nogerman


if __name__ == '__main__':
    mlist, nogerman = germanize_kodi_movies()
    json.dump(mlist, open('output.json', 'w'))
    #console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column('Title')
    table.add_column('IMDB id')
    table.add_column('IMDB link')
    table.add_column('TMDB id')
    table.add_column('TMDB link')
    table.title = '*** Not translated titles ***'
    for e in nogerman:
        table.add_row(*e)
    #console.print(table)
    with open('not_translated_titles.txt', 'w') as f:
        rprint(table, file=f)
