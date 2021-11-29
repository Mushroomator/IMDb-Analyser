from sqlalchemy import VARCHAR, SMALLINT


class MovieGenre:
    """
    Mapping between a movie and its genre.
    """

    @staticmethod
    def db_table_name():
        """
        Database table name.

        :return: database table name
        """
        return "movie_genre"

    @staticmethod
    def db_column_config():
        """
        Database column data types.

        :return: database column data types
        """
        return {
            "mg_movie_href": VARCHAR(length=18),
            "mg_genre_id": SMALLINT()
        }

    @staticmethod
    def db_columns():
        """
        Database column names.

        :return: database column names
        """
        return list(MovieGenre.db_column_config().keys())

    @staticmethod
    def db_column_types():
        """
        Database column data types.

        :return: database column data types
        """
        return list(MovieGenre.db_column_config().values())
