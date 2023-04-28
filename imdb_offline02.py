
"""
???

Sources:
 * https://www.imdb.com/interfaces/

Data sources:
 * https://datasets.imdbws.com
"""

import io
import sys
import csv
import gzip
import timeit

from dvd_list import read_titles_from_dvd_list


def get_german_title_from_id(id, gzipped=False):
    csv.field_size_limit(sys.maxsize)
    file_handler = io.TextIOWrapper(gzip.open('title.akas.tsv.gz'), encoding='utf-8') if gzipped else open('title.akas.tsv', encoding='utf-8')
    with file_handler as data_file:
        tsv_reader = csv.reader(data_file, delimiter="\t")
        # skip the first row, which is the header
        next(tsv_reader)
        # search all rows of TSV file
        for row in tsv_reader:
            #titleId (string) - a tconst, an alphanumeric unique identifier of the title
            #ordering (integer) – a number to uniquely identify rows for a given titleId
            #title (string) – the localized title
            #region (string) - the region for this version of the title
            #language (string) - the language of the title
            #types (array) - Enumerated set of attributes for this alternative title. One or more of the following: "alternative", "dvd", "festival", "tv", "video", "working", "original", "imdbDisplay". New values may be added in the future without warning
            #attributes (array) - Additional terms to describe this alternative title, not enumerated
            #isOriginalTitle (boolean)
            titleId, ordering, title, region, language, types, attributes, isOriginalTitle = row
            if titleId == id and region == 'DE':
                return title


def check_all_dvd_titles():
    movies = 0
    fails = 0
    for title in read_titles_from_dvd_list():
        #print(title)
        movies += 1
        german_title = get_german_title_from_id(title[0], gzipped=False)
        if german_title == None:
            fails += 1
            continue
        if title[2] != german_title:
            print(f'{title[2]} != {german_title}')
    print(f'Insgesamt {fails} fehlende deutsche Titel bei {movies} Filmen.')


if __name__ == '__main__':
    print(timeit.timeit('check_all_dvd_titles()', number=1, globals=globals()))
