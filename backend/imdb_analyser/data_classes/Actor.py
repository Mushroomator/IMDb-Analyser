from sqlalchemy import VARCHAR, BOOLEAN, TEXT, CHAR

from imdb_analyser.data_classes.DataClass import DataClass


class Actor(DataClass):
    """
    An actor/ actress with all their information.
    """

    @staticmethod
    def db_table_name():
        """
        Database table name.

        :return: database table name
        """
        return "actor"

    @staticmethod
    def db_column_config():
        """
        Database column data types.

        :return: database column data types
        """
        return {
            "act_href": VARCHAR(length=10),
            "act_fullname": VARCHAR(length=50),
            "act_sex": CHAR(length=1),
            "act_img_url": VARCHAR(length=255),
            "act_bio": TEXT()
        }

    @staticmethod
    def db_columns():
        """
        Database column names.

        :return: database column names
        """
        return list(Actor.db_column_config().keys())

    @staticmethod
    def db_column_types():
        """
        Database column data types.

        :return: database column data types
        """
        return list(Actor.db_column_config().values())

    def __init__(self, actor_href, fullname, sex, img, bio, movies, awards):
        self.actor_href = actor_href
        self.fullname = str(fullname)
        self.sex = str(sex)
        self.img = str(img)
        self.bio = str(bio)
        self.movies = movies
        self.awards = awards

    def to_db_dict(self):
        """
        Transform object to dictionary with key names equivalent to database column names and only containing data
        necessary for database.
        :return: transformed actor
        """

        actor = vars(self).copy()
        del actor["movies"]
        del actor["awards"]
        return {db_key: attr_val for db_key, attr_val in zip(Actor.db_columns(), actor.values())}

    def __str__(self):
        return f'{type(self).__name__}({", ".join(f"{str(member[0])}={str(member[1])}" for member in vars(self).items())})'

    def __repr__(self):
        return f'{type(self).__name__}({", ".join(f"{str(member[0])}={str(member[1])}" for member in vars(self).items())})'

    def __getnewargs__(self):
        return ()