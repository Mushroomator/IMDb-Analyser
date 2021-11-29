from sqlalchemy import VARCHAR


class MovieCast:
    """
    Cast for a movie.
    """

    @staticmethod
    def db_table_name():
        """
        Database table name.

        :return: database table name
        """
        return "movie_cast"

    @staticmethod
    def db_column_config():
        """
        Database column data types.

        :return: database column data types
        """
        return {
            "cast_actor_href": VARCHAR(length=10),
            "cast_movie_href": VARCHAR(length=10),
        }

    @staticmethod
    def db_columns():
        """
        Database column names.

        :return: database column names
        """
        return list(MovieCast.db_column_config().keys())

    @staticmethod
    def db_column_types():
        """
        Database column data types.

        :return: database column data types
        """
        return list(MovieCast.db_column_config().values())
