import math

import numpy as np
from sqlalchemy import VARCHAR, SMALLINT, DECIMAL


class Movie:
    """
    A movie.
    """

    @staticmethod
    def db_table_name():
        """
        Database table name.

        :return: database table name
        """
        return "movie"

    @staticmethod
    def db_column_config():
        """
        Database column data types.

        :return: database column data types
        """
        return {
            "mov_href": VARCHAR(length=10),
            "mov_title": VARCHAR(length=80),
            "mov_year": SMALLINT(),
            "mov_type": SMALLINT(),
            # two digits, one after the decimal point
            "mov_rating": DECIMAL(precision=1, scale=2)
        }

    @staticmethod
    def db_columns():
        """
        Database column names.

        :return: database column names
        """
        return list(Movie.db_column_config().keys())

    @staticmethod
    def db_column_types():
        """
        Database column data types.

        :return: database column data types
        """
        return list(Movie.db_column_config().values())

    def __init__(self, movie_href, title, year, type):
        self.movie_href = movie_href
        self.title = str(title)
        if year == np.NAN or math.isnan(year):
            self.year = np.NAN
        else:
            self.year = int(year)
        self.type = type
        self.genres = set()
        self.rating = np.NAN

    def to_db_dict(self):
        """
        Transform object to dictionary with key names equivalent to database column names and only containing data
        necessary for database.
        :return: transformed movie
        """
        movie = vars(self).copy()
        del movie["genres"]
        return {db_key: attr_val for db_key, attr_val in zip(Movie.db_columns(), movie.values())}

    def __str__(self):
        return f'{type(self).__name__}({", ".join(f"{str(member[0])}={str(member[1])}" for member in vars(self).items())})'

    def __repr__(self):
        return f'{type(self).__name__}({", ".join(f"{str(member[0])}={str(member[1])}" for member in vars(self).items())})'
