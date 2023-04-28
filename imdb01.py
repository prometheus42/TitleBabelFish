
"""
???

Alternativen zu IMDB:
 * https://www.omdbapi.com - offen, aber scheinbar keine lokalisierten Namen
 * https://www.themoviedb.org - offen, nur mit Anmeldung

Sources: 
 * https://cinemagoer.readthedocs.io/en/latest/
 * 
"""

from imdb import helpers
from imdb import Cinemagoer


# create an instance of the Cinemagoer class
ia = Cinemagoer()

# get a movie by URL
searched_movie = helpers.get_byURL('https://www.imdb.com/title/tt0099423/')

# show all information that are currently available for a movie
print(sorted(searched_movie.keys()))

# show all information sets that can be fetched for a movie
print(searched_movie['localized title'])

print(helpers.getAKAsInLanguage(searched_movie, 'Germany'))
