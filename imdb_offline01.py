
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


def get_german_title_from_id(id):
    csv.field_size_limit(sys.maxsize)
    with open('title.akas.tsv', encoding='utf-8') as data_file:
    #with io.TextIOWrapper(gzip.open('title.akas.tsv.gz'), encoding='utf-8') as data_file:
        tsv_reader = csv.reader(data_file, delimiter="\t")

        # skip the first row, which is the header
        next(tsv_reader)

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


print(timeit.timeit('print(get_german_title_from_id("tt0099423"))', number=1, globals=globals()))
