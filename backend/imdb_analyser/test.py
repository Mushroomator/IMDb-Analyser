import pandas as pd

from imdb_analyser.data_classes.Actor import Actor
from imdb_analyser.data_classes.Award import Award
from imdb_analyser.data_classes.DataClass import DataClass
from imdb_analyser.utils import DatabaseConnector


DatabaseConnector.delete_all_data()