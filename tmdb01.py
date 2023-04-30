
"""
Get German title from TMDB.

Sources:
 * https://github.com/celiao/tmdbsimple/
 * 
"""


import json
import pprint
import requests
import tmdbsimple as tmdb


api_key_v3 = ''
api_key_v4 = ''
tmdb.API_KEY = api_key_v3


def get_movie_by_imdb_id(api_key, imdb_id):
    url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={api_key}&language=de-DE&external_source=imdb_id"
    response = requests.get(url)
    if response.status_code == 200:
        movie_data = response.json()["movie_results"][0]
        movie_id = movie_data["id"]
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=de-DE&append_to_response=translations"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            pprint.pprint(data)
            return
            german_name = None
            for translation in data.get("translations", {}).get("translations", []):
                if translation.get("iso_639_1") == "de":
                    german_name = translation.get("data", {}).get("title")
                    break
            return {
                "title": data.get("title"),
                "german_title": german_name,
                "release_date": data.get("release_date"),
                "overview": data.get("overview"),
            }
    return None


def get_german_info(imdb_id):
    movie = tmdb.Movies(imdb_id)
    try:
        info = movie.info(language='de-DE')
    except requests.exceptions.HTTPError as e:
        tv = tmdb.TV(imdb_id)
        try:
            info = tv.info(language='de-DE')
            pprint.pprint(info)
        except requests.exceptions.HTTPError as e:
            return None, None, None
    # find title
    if info['original_language'] in ('de', 'ch', 'at'):
        german_title = info['original_title']
    else:
        german_title = info['title']
    # find description
    german_desc = info['overview']
    print(f'Title: {german_title}')
    print(f'Description: {german_desc}')


get_german_info('tt0499549')
get_german_info('tt0071458')
get_german_info('tt0088763')
get_german_info('tt0071141')
get_german_info('tt0245429')
