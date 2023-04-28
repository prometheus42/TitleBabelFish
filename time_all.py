
import timeit


from tmdb02 import check_all_dvd_titles
print('=== TMDB ===')
print(timeit.timeit('check_all_dvd_titles()', number=1, globals=globals()))

from imdb02 import check_all_dvd_titles
print('=== IMDB ===')
print(timeit.timeit('check_all_dvd_titles()', number=1, globals=globals()))

from imdb_offline02 import check_all_dvd_titles
print('=== IMDB (offline) ===')
print(timeit.timeit('check_all_dvd_titles()', number=1, globals=globals()))

