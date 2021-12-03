from flask import Blueprint
from datetime import datetime

from markupsafe import escape

from imdb_analyser.model import actor_model

actor_controller = Blueprint("actor_controller", __name__, url_prefix="/api/v1/actors")

@actor_controller.route("", methods=["POST"])
def handle_actor_list():
    all_actors_df = actor_model.get_all_actors_about()
    all_actors = all_actors_df.to_dict(orient="records")
    return {
        "timestamp": datetime.now().isoformat(),
        "data": all_actors
    }


@actor_controller.route("/<string:actor_href>", methods=["POST"])
def handle_actor_req(actor_href):
    # escape parameter as it could be manipulated by the user
    esc_actor_href = escape(actor_href)

    # ABOUT
    about_df = actor_model.get_actor_about(actor_id=esc_actor_href)
    about = about_df.to_dict(orient="records")[0]

    # AWARDS
    awards_df = actor_model.get_actor_awards(esc_actor_href)
    awards = awards_df.to_dict(orient="records")

    movies_df = actor_model.get_actor_movies(actor_id=esc_actor_href)
    movies_df["mov_year"].fillna(0, inplace=True)
    movies_df["mov_year"] = movies_df["mov_year"].astype(int)

    # get movies and their genres
    movie_genres_df = actor_model.get_all_movie_genres(esc_actor_href)
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
    mapped_genres = map(lambda movie_href: map_genres_to_movie(movie_href=movie_href), movies_df["mov_href"])
    # add column with all genres for this movie
    movies_df["mov_genres"] = list(mapped_genres)


    # ALL TIME MOVIES
    all_time_movies = movies_df[["mov_href", "mov_year", "mov_title", "mov_rating", "met_name", "mov_genres"]].sort_values(by=["mov_year"], ascending=False).fillna(0).to_dict(orient="records")

    # RATINGS
    # get everything required to calculate with rating
    rating_df = movies_df[["mov_year", "mov_rating"]].copy()
    # drop movies without a rating
    rating_df.dropna(inplace=True)
    mean_overall = rating_df["mov_rating"].mean()
    top5_movies = movies_df[["mov_href", "mov_year", "mov_title", "mov_rating", "met_name", "mov_genres"]].nlargest(columns=["mov_rating"], n=5).to_dict(orient="records")
    movie_rating_per_year_df = rating_df.groupby(by=["mov_year"], as_index=False).mean()
    movie_rating_per_year = movie_rating_per_year_df.to_dict(orient="records")

    genres_df = actor_model.get_actor_genres(actor_id=esc_actor_href)
    # sort alphabetically and return as list
    genres = genres_df["genre_name"].sort_values(ascending=True).to_list()

    return {
        "timestamp": datetime.now().isoformat(),
        "data": {
            "about": about,
            "awards": awards,
            "allTimeMovies": all_time_movies,
            "genres": genres,
            "topFiveMovies": top5_movies,
            "overallRating": mean_overall,
            "perYearRating": movie_rating_per_year,
        }
    }