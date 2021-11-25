class Actor:
    """An actor/ actress with all their information."""

    def __init__(self, actor_href, fullname, sex, img, bio, movies, awards):
        self.actor_href = actor_href
        self.fullname = str(fullname)
        self.sex = str(sex)
        self.img = str(img)
        self.bio = str(bio)
        self.movies = movies
        self.awards = awards

    def to_dict(self):
        """

        :return:
        """
        actor = vars(self)
        del actor["movies"]
        del actor["awards"]
        return actor

    def __str__(self):
        return f'{type(self).__name__}({", ".join(f"{str(member[0])}={str(member[1])}" for member in vars(self).items())})'

    def __repr__(self):
        return f'{type(self).__name__}({", ".join(f"{str(member[0])}={str(member[1])}" for member in vars(self).items())})'
