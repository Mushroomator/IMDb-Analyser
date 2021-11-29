from abc import abstractmethod, ABC


class DataClass(ABC):
    """
    Abstract super class for all data classes.
    """

    @staticmethod
    @abstractmethod
    def db_table_name():
        """
        Database table name.

        :return: database table name
        """
        pass

    @staticmethod
    @abstractmethod
    def db_column_config():
        """
        Database column configuration.

        :return: database column configuration
        """
        pass

    @staticmethod
    @abstractmethod
    def db_columns():
        """
        Database column names.

        :return: database column names
        """
        pass

    @staticmethod
    @abstractmethod
    def db_column_types():
        """
        Database column data types.

        :return: database column data types
        """
        pass
