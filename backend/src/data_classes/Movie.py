import math

import numpy as np


class Movie:

    def __init__(self, movie_href, title, year, type):
        self.movie_href = movie_href
        self.title = str(title)
        if year == np.NAN or math.isnan(year):
            self.year = np.NAN
        else:
            self.year = int(year)
        self.type = type
        self.genres = {}
        self.rating = np.NAN

    def to_dict(self):
        return vars(self)

    def __str__(self):
        return f'{type(self).__name__}({", ".join(f"{str(member[0])}={str(member[1])}" for member in vars(self).items())})'

    def __repr__(self):
        return f'{type(self).__name__}({", ".join(f"{str(member[0])}={str(member[1])}" for member in vars(self).items())})'
