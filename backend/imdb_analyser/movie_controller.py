from flask import Blueprint

from imdb_analyser.model import movie_model
from datetime import datetime

movie_controller = Blueprint("movie_controller", __name__, url_prefix="/api/v1/movies")


@movie_controller.route("", methods=["POST"])
def handle_movie_list():
    all_movies_df = movie_model.get_all_movies()

    movie_genres_df = movie_model.get_all_movie_genres()
    movie_genres = movie_genres_df.groupby(["mg_movie_href"])["genre_name"].apply(list)

    def map_genres_to_movie(movie_href):
        """
        Associates genres to a given movie.

        :param movie_href: movie-ID
        :type movie_href: str
        :return: list of genres associated with the movie
        """
        if movie_genres.index.__contains__(movie_href):
            return movie_genres.at[movie_href]
        else:
            return []

    mapped_genres = map(lambda movie_href: map_genres_to_movie(movie_href=movie_href), all_movies_df["mov_href"])
    # add column with all genres for this movie
    all_movies_df["mov_genres"] = list(mapped_genres)
    # fill non-present values with 0 (year and rating)
    all_movies_df.fillna(0, inplace=True)
    # cast year to integer
    all_movies_df["mov_year"] = all_movies_df["mov_year"].astype(int)
    all_movies = all_movies_df.to_dict(orient="records")

    return {
        "timestamp": datetime.now().isoformat(),
        "data": all_movies
    }
