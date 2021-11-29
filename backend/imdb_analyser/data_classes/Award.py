import math

import numpy as np
from sqlalchemy import VARCHAR, SMALLINT

from imdb_analyser.data_classes.DataClass import DataClass


class Award(DataClass):
    """
    Award for actor/ actress.
    """

    @staticmethod
    def db_table_name():
        """
        Database table name.

        :return: database table name
        """
        return "award"

    @staticmethod
    def db_column_config():
        """
        Database column data types.

        :return: database column data types
        """
        return {
            "aw_actor_href": VARCHAR(length=10),
            "aw_id": SMALLINT(),
            "aw_year": SMALLINT(),
            "aw_outcome": VARCHAR(length=7),
            "aw_description": VARCHAR(length=255),
            "aw_movie_href": VARCHAR(length=10),
            "aw_movie_name": VARCHAR(length=255),
            "aw_category_id": SMALLINT()
        }

    @staticmethod
    def db_columns():
        """
        Database column names.

        :return: database column names
        """
        return list(Award.db_column_config().keys())

    @staticmethod
    def db_column_types():
        """
        Database column data types.

        :return: database column data types
        """
        return list(Award.db_column_config().values())

    def __init__(self, year, outcome, desc, movie, movie_href, category):
        if year == np.NAN or math.isnan(year):
            self.year = np.NAN
        else:
            self.year = int(year)
        self.outcome = str(outcome)
        self.desc = str(desc)
        self.movie_href = str(movie_href)
        self.movie = str(movie)
        self.category = str(category)

    def to_db_dict(self):
        """
        Transform object to dictionary with key names equivalent to database column names and only containing data
        necessary for database.
        :return: transformed award
        """
        award = vars(self).copy()
        # First two values of db_columns() are not part of this object so skip them
        return {db_key: attr_val for db_key, attr_val in zip(Award.db_columns()[2:], award.values())}

    def __str__(self):
        return f'{type(self).__name__}({", ".join(f"{str(member[0])}={str(member[1])}" for member in vars(self).items())})'

    def __repr__(self):
        return f'{type(self).__name__}({", ".join(f"{str(member[0])}={str(member[1])}" for member in vars(self).items())})'
