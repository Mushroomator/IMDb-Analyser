from sqlalchemy import VARCHAR, SMALLINT


class Genre:
    """
    Genre of movie.
    """

    @staticmethod
    def db_table_name():
        """
        Database table name.

        :return: database table name
        """
        return "genre"

    @staticmethod
    def db_column_config():
        """
        Database column data types.

        :return: database column data types
        """
        return {
            "genre_id": SMALLINT(),
            "genre_name": VARCHAR(length=25)
        }

    @staticmethod
    def db_columns():
        """
        Database column names.

        :return: database column names
        """
        return list(Genre.db_column_config().keys())

    @staticmethod
    def db_column_types():
        """
        Database column data types.

        :return: database column data types
        """
        return list(Genre.db_column_config().values())
