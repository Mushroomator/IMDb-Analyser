from sqlalchemy import SMALLINT, VARCHAR


class MediumType:
    """
    Medium type of a medium (e.g. movie, short movie, series etc.).
    """

    @staticmethod
    def db_table_name():
        """
        Database table name.

        :return: database table name
        """
        return "medium_type"

    @staticmethod
    def db_column_config():
        """
        Database column data types.

        :return: database column data types
        """
        return {
            "met_id": SMALLINT(),
            "met_name": VARCHAR(length=35)
        }

    @staticmethod
    def db_columns():
        """
        Database column names.

        :return: database column names
        """
        return list(MediumType.db_column_config().keys())

    @staticmethod
    def db_column_types():
        """
        Database column data types.

        :return: database column data types
        """
        return list(MediumType.db_column_config().values())
