
"""
Get German title from TMDB.

Sources:
 * https://github.com/celiao/tmdbsimple/
 * 
"""

import requests
import tmdbsimple as tmdb


api_key_v3 = ''
api_key_v4 = ''
tmdb.API_KEY = api_key_v3
imdb_id = 'tt0099423'


def get_movie_by_imdb_id(api_key, imdb_id):
    url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={api_key}&language=en-US&external_source=imdb_id"
    response = requests.get(url)
    if response.status_code == 200:
        movie_data = response.json()["movie_results"][0]
        movie_id = movie_data["id"]
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US&append_to_response=translations"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
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


movie = tmdb.Movies(imdb_id)
print(movie.info()['title'])
for t in movie.alternative_titles()['titles']:
    if 'iso_3166_1' in t and t['iso_3166_1'] == 'DE':
        print(t['title'])
