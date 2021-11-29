from sqlalchemy import VARCHAR, SMALLINT


class AwardCategory:
    """
    Category and award belongs to.
    """

    @staticmethod
    def db_table_name():
        """
        Database table name.

        :return: database table name
        """
        return "award_category"

    @staticmethod
    def db_column_config():
        """
        Database column data types.

        :return: database column data types
        """
        return {
            "awc_id": SMALLINT(),
            "awc_cat_name": VARCHAR(length=50)
        }

    @staticmethod
    def db_columns():
        """
        Database column names.

        :return: database column names
        """
        return list(AwardCategory.db_column_config().keys())

    @staticmethod
    def db_column_types():
        """
        Database column data types.

        :return: database column data types
        """
        return list(AwardCategory.db_column_config().values())
