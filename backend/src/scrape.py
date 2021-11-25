import math
import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

from data_classes.Actor import Actor
from data_classes.Award import Award
from data_classes.Movie import Movie
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(threadname)s] [%(name)s]  [%(levelname)s] %(message)s')

BASE_DOMAIN = "http://www.imdb.com"
# Set request header to US language to get english names for movies instead of german (= default)
REQ_HEADERS = {"Accept-Language": "en-US,en;q=0.5"}


class WebScraper:
    """
    WebScraper which allows you to scrape the IMDb Website and store information
    on actors/ actresses, their movies and awards.
    """

    def __init__(self):
        """
        Create a WebScraper instance which allows you to scrape the IMDb Website and store information
        on actors/ actresses, their movies and awards.
        """

        self.actor_df = pd.DataFrame(columns=["actor_href", "fullname", "sex", "img", "bio"])
        """
        Hold all actor related data (corresponds to "Actor" table in database).
        """

        self.award_df = pd.DataFrame(columns=["actor_href", "award_id", "year", "outcome", "desc", "movie", "category"])
        """
        Hold all award related data (corresponds to "Award" table in database).
        """
        self.cast_df = pd.DataFrame(columns=["actor_href", "movie_href"])
        """
        Hold all cast related data (corresponds to "Cast" table in database).
        """
        self.movie_df = pd.DataFrame(columns=["href", "title", "year", "type"])
        """
        Hold all movie related data (corresponds to "Movie" table in database).
        """
        self.move_genre_df = pd.DataFrame(columns=["movie_href", "genre_id"])
        """
        Hold mapping from movies to genres (corresponds to "MovieGenre" table in database).
        """
        self.genre_df = pd.DataFrame(columns=["genre_id", "genre_name"])
        """
        Hold all genres and a unique ID to identify them (corresponds to "Genre" table in database).
        """
        self.award_category_df = pd.DataFrame(columns=["id", "cat_name"])
        """
        Hold all categories for awards and a unique ID to identify them (corresponds to "AwardCategory" table in database).
        """
        self.medium_type_df = pd.DataFrame(columns=["met_id", "met_name"])
        """
        Hold all medium type for a medium/ movie e.g short movie, series etc. and a unique ID to identify them (corresponds to "MediumType" table in database).
        """
        self.movie_dict = {}
        """
        Dictionary to hold all unique movies, allowing to fetch details for a movie only once.
        """
        self.all_genres = dict()
        """
        Dictionary that holds all unique genres of all movies.
        Note: dictionary is required (instead of a set) as order needs to be preserved (> Python 3.7 required)
        """

    def scrape(self):
        """
        Webscrape IMDb for actors/ actresses, their movies and awards.

        :return:
        """
        logger.info("Starting webscraping...")
        list_url = BASE_DOMAIN + "/list/ls053501318/"
        logger.info("Getting actor list from %s...", list_url)
        list_page = requests.get(list_url, headers=REQ_HEADERS)
        logger.info("Done. Got list of actors.")
        parsed_list_page = BeautifulSoup(list_page.text, "html.parser")
        actor_hrefs = self.get_actor_hrefs(parsed_list_page)
        logger.info("Getting all actor details for actors %s...", actor_hrefs)
        actor_details = self.get_all_actors_details(actor_hrefs)
        logger.info("Done. Gathered all actor details.")
        logger.info("Getting all details for all movies...", self.movie_dict)
        self.get_all_movies_details()
        logger.info("Done. Got all movie details.")
        self.put_into_dataframes(actor_details)

    def process_movie(self, movie):
        """
        Process a movie.
            1.   Transform Movie object to a dictionary so it can be inserted into movie_df
            2.   Replace genre name with the unique genre id (required for database normalization)
            3.   Insert movie_href and the genre_ids for a movie into the bridge table move_genre_df
                 (required as table Movie and Genre have a n:m relationship)
        :param movie: an instance of Movie
        :type movie: Movie
        :return:
        """
        # transform to dictionary
        mov = movie.to_dict()

        # create bridge table for with the current movie ID as a constant value in one column and the genre ID
        # in the other column
        mov_genres = pd.DataFrame(columns=["movie_href", "genre_id"])

        # Map the genre name to its unique ID (DB normalization!)
        mapped_genres = map(lambda genre_name: self.genre_df.loc[genre_name, "genre_id"], movie.genres)
        mov_genres["genre_id"] = list(mapped_genres)
        # now fill all rows (determined by length of list above) with current movie_href as constant value
        mov_genres["movie_href"] = movie.movie_href
        # Append the bridge table for this movie to the bridge table containing all the movies
        self.move_genre_df = self.move_genre_df.append(mov_genres)


        # Genre does not need to be stored in Movie table so remove it and free taken up memory
        del mov["genres"]
        # now return movie dictionary as it has required format
        return mov

    def process_award(self, award):
        return award.to_dict()

    def process_actor(self, actor):
        return actor.to_dict()

    def put_into_dataframes(self, actor_details):
        keys = self.all_genres.keys()
        self.genre_df["genre_id"] = range(len(keys))
        self.genre_df["genre_name"] = keys
        self.genre_df.set_index("genre_name", inplace=True)

        for actor in actor_details:
            cast = pd.DataFrame(columns=["actor_href", "movie_href"])
            cast["movie_href"] = actor.movies
            cast["actor_href"] = actor.actor_href
            self.cast_df = self.cast_df.append(cast)

            transformed_awards = map(self.process_award, actor.awards)
            award = pd.DataFrame(list(transformed_awards), columns=["actor_href", "year", "outcome", "desc", "movie", "category"])
            award["award_id"] = range(award.shape[0])
            award["actor_href"] = actor.actor_href
            self.award_df = self.award_df.append(award)

        transformed_actors = map(self.process_actor, actor_details)
        self.actor_df = pd.DataFrame(list(transformed_actors), columns=["actor_href", "fullname", "sex", "img", "bio"])

        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)

        # Process each movie (use map() built-in for better performance)
        # i. e. Transform movie object and fill related tables MovieGenre und Genre
        transformed_movies = map(self.process_movie, self.movie_dict.values())
        # Fill table "Movie"
        self.movie_df = pd.DataFrame(list(transformed_movies))
        print("Genre Table")
        print(self.genre_df)
        print("MovieGenre Table")
        print(self.move_genre_df)
        print("Movie Table")
        print(self.movie_df)
        print("Cast Table")
        print(self.cast_df)
        print("Award Table")
        print(self.award_df)
        print("Actor table")
        print(self.actor_df)


    def get_actor_hrefs(self, list_page):
        """Get hrefs for all the relevant actors/ actresses.

        :param list_page: parsed HTML for "actor list page"
        :type list_page: BeautifulSoup
        :return: list of hrefs, one for each actor
        """
        hrefs = []
        actors = list_page.select(
            "#main > div > div.lister.list.detail.sub-list > div.lister-list > * > div.lister-item-content > h3 > a")
        for actor in actors:
            hrefs.append(actor["href"])
        return hrefs

    def get_actor_img(self, actor_page):
        """Get URL to Image

        :param actor_page: parsed HTML page for actor
        :type actor_page: BeautifulSoup
        :return:
        """
        imgTag = actor_page.find(id="name-poster")
        return imgTag["src"]

    def get_actor_bio(self, actor_href):
        """Get an actor/ actresses biography.

        :param actor_href: href for a single actor/ actress
        :type actor_href: str
        :return: biography for given actor/ actress
        """
        bio_page = requests.get(BASE_DOMAIN + actor_href + "/bio", headers=REQ_HEADERS)
        parsed_bio_page = BeautifulSoup(bio_page.text, "html.parser")
        bio_tag = parsed_bio_page.find("p")
        bio_text = str(bio_tag.get_text()).strip()
        return bio_text

    def get_actor_movies(self, actor_page):
        """Get all movies an actor/ actress has done.

        :param actor_page: BeautifulSoup
        :return: list of all movies the actor/ actress was involved in
        """
        # Replace '&nbsp;' which is turned to Unicode by beautiful soup with actual space
        all_movies = actor_page.find_all("div", class_="filmo-row", id=re.compile("^actor-"))
        movies = {}
        for movie in all_movies:
            year = np.NAN
            title = ""
            href = ""
            type = "Movie"
            for i, element in enumerate(movie.children):
                if i == 1:
                    # in first span is the
                    year_str = str(element.get_text())
                    multiple_years = year_str.split("-")
                    if len(multiple_years) == 2:
                        year_str = multiple_years[0]
                    year_str = re.sub("\xa0|\n", "", year_str)
                    year_str = re.search("[1-2][0-9][0-9][0-9]", year_str)
                    if year_str:
                        year = int(year_str.group(0))
                if i == 3:
                    movie_link = next(element.children)
                    href = movie_link["href"]
                    title = movie_link.get_text()
                if i == 4:
                    # There might be a movie status in brackets instead of the movie type
                    if not ("class" in element and element["class"] == "in_production"):
                        movie_type_match = re.search("(?<=\().+?(?=\))", element.get_text())
                        if movie_type_match:
                            # there might be a movie type there might not be one, if not the type is movie as defined above
                            type = movie_type_match.group(0)
            movies[href] = Movie(movie_href=href, title=title, year=year, type=type)
        return movies

    def get_actor_awards(self, actor_href):
        actor_awards_page = requests.get(BASE_DOMAIN + actor_href + "/awards")
        parsed_awards_page = BeautifulSoup(actor_awards_page.text, "html.parser")
        award_tables = parsed_awards_page.find_all("table", class_="awards")

        awards = []
        for table in award_tables:
            # each table represents one category of awards
            award_category_tables = table.find_all("tr")
            # award information of previous row (required to fill in information of "grouped" rows)
            prev_award = None
            # for each award category, process all the rows
            for tableRow in award_category_tables:
                prev_award = self.process_actor_award_row(prev_award, tableRow)
                awards.append(prev_award)
        return awards

    def process_actor_award_row(self, prev_award, award_row):
        """
        Process a single row in an awards table

        :param prev_award: previous award
        :type prev_award: Award
        :param award_row: row in the table (a tr tag)
        :return: award and its details
        """

        def get_year(award_row):
            """
            Extract year from row

            :param award_row: row in the table (a <tr> tag)
            :return:
            """
            year = np.NAN
            year_tag = award_row.find("td", class_="award_year")
            if year_tag:
                year = int(year_tag.get_text().strip())
            return year

        def get_outcome(award_row):
            category = ""
            outcome = ""
            outcome_tag = award_row.find("td", class_="award_outcome")
            if outcome_tag:
                for i, tag in enumerate(outcome_tag):
                    if i == 1:
                        outcome = tag.get_text().strip()
                    if i == 4:
                        category = tag.get_text().strip()
            return category, outcome

        def get_desc(award_row):
            desc = ""
            movie = ""
            desc_tag = award_row.find("td", class_="award_description")
            if desc_tag:
                for i, content in enumerate(desc_tag.contents):
                    if i == 0:
                        # award description here
                        desc = content.get_text().strip()
                    elif i == 3:
                        # movie/ title name here
                        movie = content.get_text().strip()
            return desc, movie

        year = get_year(award_row)
        category, outcome = get_outcome(award_row)
        desc, movie = get_desc(award_row)

        # Process groups:
        # An actor may receive several awards in the same year,
        # he may also have several outcomes (winner, nominee) for the same award in the same year
        # and there may be different award categories in which the actor can win in the very same year at the
        # same award ceremony. IMDb groups all those special cases together: the first row always contains all the info and
        # in consecutive rows only the "changing information" is added.
        # So we need to add the missing information from the previous row if available to.
        # It can be proven by induction that every row after this process will have all the information available:
        # (1) prev_row = None; Row one has all the information available -> Done
        # (2) prev_row = will be set to first row (and has all the info available)
        #     it is checked if year, category and outcome are available in consecutive rows
        #     as a previous row has all the information available this info can be filled in from the previous row.
        #     Therefore the consecutive row will also have all information filled in and will become the previous row
        #     for a next possible row -> Done
        # if there is no year, take year from previous row
        if not year and prev_award:
            year = prev_award.year
        # if there is no category get it from previous row
        if not category and prev_award:
            category = prev_award.category
        if not outcome and prev_award:
            outcome = prev_award.outcome

        return Award(year=year, outcome=outcome, desc=desc, movie=movie, category=category)

    def get_actor_details(self, actor_href):
        """Get all details to an actor/ actress.

        :param actor_href: href to an actor/ actress
        :type actor_href: str
        :return: an actor/ actress with their details
        """
        actor_url = BASE_DOMAIN + actor_href
        logger.info("Getting details for actor from %s...", actor_url)
        actor_page = requests.get(actor_url, headers=REQ_HEADERS)
        parsed_actor_page = BeautifulSoup(actor_page.text, "html.parser")
        # Get fullname
        fullname = parsed_actor_page.find("span", class_="itemprop").get_text()
        # Get biography
        bio = self.get_actor_bio(actor_href)
        # Get image URL
        img = self.get_actor_img(parsed_actor_page)
        # Get movies
        movies = self.get_actor_movies(parsed_actor_page)
        # Merge movie dicts so movies will not be fetched twice
        self.movie_dict = self.movie_dict | movies
        # Get awards
        awards = self.get_actor_awards(actor_href)
        # Create a new actor object for an actor/ actress with all their details
        actor = Actor(actor_href=actor_href, fullname=fullname, bio=bio, awards=awards, movies=movies.keys(),
                      sex="Male", img=img)
        logger.info("Done. Got all details for actor %s => %s", actor_href, actor)
        return actor

    def get_all_movies_details(self):
        """
        Get all details to all movies.

        :return:
        """
        counter = 0
        for href, movie in self.movie_dict.items():
            logger.info("Getting movie details for movie %s", href)
            self.get_movie_details(href, movie)
            logger.info("Got details for movie %s => %s", href, movie)
            counter += 1
            if counter == 4:
                break

    def get_movie_details(self, movie_href, movie):
        """Get all details for a specific movie.

        :param movie_href: href to a movie
        :type movie_href: str
        :param movie: movie object
        :type movie: Movie
        :return: all details for a specific movie
        """
        movie_page = requests.get(BASE_DOMAIN + movie_href, headers=REQ_HEADERS)
        parsed_movie_page = BeautifulSoup(movie_page.text, "html.parser")
        # The rating is a span with an class that starts with "AggregateRatingButton__RatingScore-sc"
        rating_span = parsed_movie_page.find("span", class_=re.compile("AggregateRatingButton__RatingScore-sc"))
        if not rating_span:
            rating = np.NAN
        else:
            # get the text and parse it as a float (may be a decimal number between 0.0 and 10.0)
            rating = float(rating_span.get_text())
        # genres are in within a div with has the "data-testid" value set to "genres"
        genre_div = parsed_movie_page.find("div", attrs={"data-testid": "genres"})
        # actual genre names are in spans with "ipc-chip__text" class
        genre_spans = genre_div.find_all("span", class_="ipc-chip__text")
        genres = set()
        for genre in genre_spans:
            gtxt = genre.get_text()
            genres.add(gtxt)
            self.all_genres[gtxt] = None

        # add missing information to movie instances
        movie.genres = genres
        movie.rating = rating

    def get_all_actors_details(self, actor_hrefs):
        """Get all details to all actors.

        :param actor_hrefs: list of hrefs to an actor`s page
        :type actor_hrefs: list[str]
        :return: list of actors/ actresses with their details
        """
        actors = []
        for href in actor_hrefs:
            logger.info("Getting all Current actor: %s", href)
            actorDetail = self.get_actor_details(href)
            actors.append(actorDetail)
            break

        return actors


scraper = WebScraper()
scraper.scrape()
