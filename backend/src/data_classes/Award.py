import math

import numpy as np


class Award:

    def __init__(self, year, outcome, desc, movie, category):
        if year == np.NAN or math.isnan(year):
            self.year = np.NAN
        else:
            self.year = int(year)
        self.outcome = str(outcome)
        self.desc = str(desc)
        self.movie = str(movie)
        self.category = str(category)

    def to_dict(self):
        return vars(self)

    def __str__(self):
        return f'{type(self).__name__}({", ".join(f"{str(member[0])}={str(member[1])}" for member in vars(self).items())})'

    def __repr__(self):
        return f'{type(self).__name__}({", ".join(f"{str(member[0])}={str(member[1])}" for member in vars(self).items())})'