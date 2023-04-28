
from pyexcel_ods3 import get_data


filename = 'dvd_listing.ods'
no_of_movies = 20


def read_titles_from_dvd_list():
    sheet = 'Filme'    
    data = get_data(filename)
    # get ID and titles from file
    for row in data[sheet][100:100+no_of_movies]:
        RIPPED = 1
        GERMAN = 2
        ORIGINAL = 3
        IMDB_ID = 4
        OWNER = 5
        NOTE = 6
        # check if the first cell in the row is empty
        try:
            if not row[GERMAN]:
                break  # end the loop if the first cell is empty
            yield row[IMDB_ID], row[ORIGINAL], row[GERMAN]
        except IndexError as e:
            break
