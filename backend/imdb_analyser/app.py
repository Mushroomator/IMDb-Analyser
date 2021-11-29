import asyncio
import json
import os
import logging
from concurrent.futures import ThreadPoolExecutor, Future
from markupsafe import escape
from datetime import datetime

from flask import Flask

from imdb_analyser.model import actor_model
from imdb_analyser.utils import DatabaseConnector
from utils.WebScraper import WebScraper

app = Flask(__name__, static_folder="../../frontend/build", static_url_path="/")

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(name)s]  [%(levelname)s] %(message)s')

executor = ThreadPoolExecutor(max_workers=3)


@app.route("/")
def index():
    """
    Serve index.html so the react frontend can start up and take over.
    :return: index.html
    """
    return app.send_static_file("index.html")


@app.route("/api/delete-all", methods=["DELETE"])
def handle_delete():
    """
    Deletion of all data in the database is requested.

    :return:
    """
    # delete all data in the database
    is_deleted = DatabaseConnector.delete_all_data()
    if is_deleted:
        msg = {
            "success": True,
            "message": "All data has been deleted!"
        }
    else:
        msg = {
            "success": False,
            "message": "Could not delete data in the database!"
        }
    return msg


@app.route("/api/scrape", methods=["POST"])
def handle_web_scape():
    scraper = WebScraper()
    scrape_task = executor.submit(scraper.scrape)
    scrape_task.add_done_callback(lambda future: app.logger.info("Web scraped everything"))
    return {
        "success": True,
        "message": "Started web scraping from https://imdb.com..."
    }


@app.route("/api/actor/<string:actor_href>", methods=["POST"])
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
    movies_df["genres"] = list(mapped_genres)


    # ALL TIME MOVIES
    all_time_movies = movies_df[["mov_href", "mov_year", "mov_title", "mov_rating", "met_name", "genres"]].sort_values(by=["mov_year"], ascending=False).to_dict(orient="records")

    # RATINGS
    # get everything required to calculate with rating
    rating_df = movies_df[["mov_year", "mov_rating"]].copy()
    # drop movies without a rating
    rating_df.dropna(inplace=True)
    mean_overall = rating_df["mov_rating"].mean()
    top5_movies = movies_df[["mov_href", "mov_year", "mov_title", "mov_rating", "met_name", "genres"]].nlargest(columns=["mov_rating"], n=5).to_dict(orient="records")
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

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    host = "localhost"

    app.logger.info("Starting Flask server listening on %s:%s", host, port)
    app.run(host=host, port=port)
