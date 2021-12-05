import concurrent.futures
import logging
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, FIRST_EXCEPTION, ALL_COMPLETED
from timeit import default_timer as timer

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from numpy import isnan

from imdb_analyser.data_classes.Actor import Actor
from imdb_analyser.data_classes.Award import Award
from imdb_analyser.data_classes.AwardCategory import AwardCategory
from imdb_analyser.data_classes.Genre import Genre
from imdb_analyser.data_classes.MediumType import MediumType
from imdb_analyser.data_classes.Movie import Movie
from imdb_analyser.data_classes.MovieCast import MovieCast
from imdb_analyser.data_classes.MovieGenre import MovieGenre
from imdb_analyser.utils import DatabaseConnector
from imdb_analyser.utils.Progress import Progress

logging.basicConfig(filename="test.log", encoding="UTF-8", level=logging.INFO,
                    format='%(asctime)s [%(name)s]  [%(levelname)s] %(message)s')

BASE_DOMAIN = "http://www.imdb.com"
ACTOR_PAGE_PREFIX = "/name/"
MOVIE_PAGE_PREFIX = "/title/"
# Set request header to US language to get english names for movies instead of german (= default)
REQ_HEADERS = {"Accept-Language": "en-US,en;q=0.5"}

proxy = None


# proxy = {"http": "http://36.67.66.100:30142"}

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

        self.actor_df = pd.DataFrame(columns=Actor.db_columns())
        """
        Hold all actor related data (corresponds to "Actor" table in database).
        """

        self.award_df = pd.DataFrame(columns=Award.db_columns())
        """
        Hold all award related data (corresponds to "Award" table in database).
        """
        self.movie_cast_df = pd.DataFrame(columns=MovieCast.db_columns())
        """
        Hold all cast related data (corresponds to "Cast" table in database).
        """
        self.movie_df = pd.DataFrame(columns=Movie.db_columns())
        """
        Hold all movie related data (corresponds to "Movie" table in database).
        """
        self.movie_genre_df = pd.DataFrame(columns=MovieGenre.db_columns())
        """
        Hold mapping from movies to genres (corresponds to "MovieGenre" table in database).
        """
        self.genre_df = pd.DataFrame(columns=Genre.db_columns())
        """
        Hold all genres and a unique ID to identify them (corresponds to "Genre" table in database).
        """
        self.award_category_df = pd.DataFrame(columns=AwardCategory.db_columns())
        """
        Hold all categories for awards and a unique ID to identify them (corresponds to "AwardCategory" table in database).
        """
        self.medium_type_df = pd.DataFrame(columns=MediumType.db_columns())
        """
        Hold all medium type for a medium/ movie e.g short movie, series etc. and a unique ID to identify them (corresponds to "MediumType" table in database).
        """
        self.movie_dict = dict()
        """
        Dictionary to hold all unique movies, allowing to fetch details for a movie only once.
        """
        self.all_genres = set()
        """
        Dictionary that holds all unique genres of all movies.
        Note: dictionary is required (instead of a set) as order needs to be preserved (> Python 3.7 required)
        """
        self.medium_types = dict()
        self.progress = Progress()
        """
        Keeps track of progress of webscraping (thread-safe!).
        """
        self._merge_dict_lock = threading.Lock()
        """
        Lock when merging dictionaries to prevent corruption of data by race-conditions.
        """
        self._all_genres_lock = threading.Lock()
        """
        Lock when merging dictionaries to prevent corruption of data by race-conditions.
        """
        self.max_workers = 5
        """
        Number of threads which perform web scraping.
        5 seems to work without getting 503s because of the IP address getting blocked due to the high request ratio.
        """
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        """
        Executor to schedule worker threads.
        """

    def scrape(self):
        """
        Webscrape IMDb for actors/ actresses, their movies and awards.

        :return: true if successful, false otherwise
        """
        logging.info("Starting webscraping...")
        list_url = BASE_DOMAIN + "/list/ls053501318/"
        logging.info("Getting actor list from %s...", list_url)
        list_page = requests.get(list_url, headers=REQ_HEADERS, proxies=proxy)
        if list_page.status_code != 200:
            logging.error("Failed to get list of actors from %s. Status code: %d", list_url, list_page.status_code)
            return False
        logging.info("Done. Got list of actors.")
        parsed_list_page = BeautifulSoup(list_page.text, "html.parser")
        actor_ranks = self.get_actor_hrefs(parsed_list_page)
        actor_ids = list(actor_ranks.keys())
        logging.info("Getting all actor details for actors %s...", actor_ids)
        actor_details = self.get_all_actors_details(actor_ranks)
        logging.info("Done. Gathered all actor details.")
        logging.info("Getting all details for all %d movies...", len(self.movie_dict))
        self.get_all_movies_details()
        logging.info("Done. Got all movie details.")
        logging.info("Inserting gathered data into PostgreSQL database...")
        self.put_into_dataframes(actor_details)
        logging.info("Done. Inserted gathered data into PostgreSQL database.")
        # no set progress to finished! MUST be last instruction otherwise caller might think processing is finished when
        # it is not and thus suspend the call to early. In case of any failure during processing the progress will not
        # be at 100% so whenever that happens something went wrong.
        self.progress.set_finished()
        return True

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
        mov = movie.to_db_dict()

        # create bridge table for with the current movie ID as a constant value in one column and the genre ID
        # in the other column
        mov_genres = pd.DataFrame(columns=MovieGenre.db_columns())

        # Map the genre name to its unique ID (DB normalization!)
        mapped_genres = map(lambda genre_name: self.genre_df.loc[genre_name, "genre_id"], movie.genres)
        mov_genres["mg_genre_id"] = list(mapped_genres)
        # now fill all rows (determined by length of list above) with current movie_href as constant value
        mov_genres["mg_movie_href"] = movie.movie_href
        # Append the bridge table for this movie to the bridge table containing all the movies
        self.movie_genre_df = self.movie_genre_df.append(mov_genres)
        # now return movie dictionary as it has required format
        return mov

    def process_award(self, award):
        """
        Process/ transform a single award instance.
        Turns object into dictionary with key names being equivalent to database column names.

        :param award: award to be processed
        :type award: Award
        :return:
        """
        return award.to_db_dict()

    def process_actor(self, actor):
        """
        Process/ transform a single actor instance.
        Turns object into dictionary with key names being equivalent to database column names.

        :param actor: actor to be processed
        :type actor: Actor
        :return:
        """
        return actor.to_db_dict()

    def read_from_csv_files(self):
        """
        Read data from .csv files instead of webscraping it.
        Allows to have the data available without having to webscrape it before.
        Note: Mainly used for testing purposes.

        :return:
        """
        self.actor_df = pd.read_csv("data/actor.csv", usecols=Actor.db_columns())
        self.award_category_df = pd.read_csv("data/award_category.csv", usecols=AwardCategory.db_columns())
        self.medium_type_df = pd.read_csv("data/medium_type.csv", usecols=MediumType.db_columns())
        self.movie_df = pd.read_csv("data/movie.csv", usecols=Movie.db_columns())
        self.award_df = pd.read_csv("data/award.csv", usecols=Award.db_columns())
        self.genre_df = pd.read_csv("data/genre.csv", usecols=Genre.db_columns())
        self.movie_genre_df = pd.read_csv("data/movie_genre.csv", usecols=MovieGenre.db_columns())
        self.movie_cast_df = pd.read_csv("data/movie_cast.csv", usecols=MovieCast.db_columns())

    def write_to_csv_files(self):
        """
        Write content of all dataframes to .csv files to be able to skip webscraping when needed.

        :return:
        """
        self.actor_df.to_csv("data/actor.csv", columns=Actor.db_columns())
        self.award_category_df.to_csv("data/award_category.csv", columns=AwardCategory.db_columns())
        self.medium_type_df.to_csv("data/medium_type.csv", columns=MediumType.db_columns())
        self.movie_df.to_csv("data/movie.csv", columns=Movie.db_columns())
        self.award_df.to_csv("data/award.csv", columns=Award.db_columns())
        self.genre_df.to_csv("data/genre.csv", columns=Genre.db_columns())
        self.movie_genre_df.to_csv("data/movie_genre.csv", columns=MovieGenre.db_columns())
        self.movie_cast_df.to_csv("data/movie_cast.csv", columns=MovieCast.db_columns())

    def insert_into_db(self):
        """
        Insert all data into PostgreSQL database.

        :return: true if insertion is successful, false otherwise
        """
        success = DatabaseConnector.insert_into_db_table(self.actor_df, Actor)
        if not success:
            return False
        success = DatabaseConnector.insert_into_db_table(self.award_category_df, AwardCategory)
        if not success:
            return False
        success = DatabaseConnector.insert_into_db_table(self.medium_type_df, MediumType)
        if not success:
            return False
        success = DatabaseConnector.insert_into_db_table(self.movie_df, Movie)
        if not success:
            return False
        success = DatabaseConnector.insert_into_db_table(self.award_df, Award)
        if not success:
            return False
        success = DatabaseConnector.insert_into_db_table(self.genre_df, Genre)
        if not success:
            return False
        success = DatabaseConnector.insert_into_db_table(self.movie_genre_df, MovieGenre)
        if not success:
            return False
        success = DatabaseConnector.insert_into_db_table(self.movie_cast_df, MovieCast)
        if not success:
            return False
        return True

    def put_into_dataframes(self, actor_details):
        """

        :param actor_details:
        :return:
        """
        keys = list(self.all_genres)
        self.genre_df["genre_id"] = range(len(keys))
        self.genre_df["genre_name"] = keys
        self.genre_df.set_index("genre_name", inplace=True)

        for actor in actor_details:
            cast = pd.DataFrame(columns=MovieCast.db_columns())
            cast["cast_movie_href"] = actor.movies
            cast["cast_actor_href"] = actor.actor_href
            self.movie_cast_df = self.movie_cast_df.append(cast)
            transformed_awards = map(self.process_award, actor.awards)
            award = pd.DataFrame(list(transformed_awards), columns=Award.db_columns())
            award["aw_id"] = range(award.shape[0])
            award["aw_actor_href"] = actor.actor_href
            self.award_df = self.award_df.append(award)

        transformed_actors = map(self.process_actor, actor_details)
        self.actor_df = pd.DataFrame(list(transformed_actors), columns=Actor.db_columns())
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.max_rows', None)

        # Process each movie (use map() built-in for better performance)
        # i. e. Transform movie object and fill related tables MovieGenre und Genre
        transformed_movies = map(self.process_movie, self.movie_dict.values())
        # Fill table "Movie"
        self.movie_df = pd.DataFrame(list(transformed_movies), columns=Movie.db_columns())

        unq_cats = self.award_df["aw_category_id"].unique()
        ids = range(len(unq_cats))
        self.award_category_df = pd.DataFrame({"awc_id": ids, "awc_cat_name": unq_cats})
        map_cats_to_fk = dict(zip(unq_cats, ids))
        self.award_df["aw_category_id"] = list(map(lambda cat: map_cats_to_fk[cat], self.award_df["aw_category_id"]))

        unq_types = self.movie_df["mov_type"].unique()
        ids = range(len(unq_types))
        self.medium_type_df = pd.DataFrame({"met_id": ids, "met_name": unq_types})
        map_types_to_fk = dict(zip(unq_types, ids))
        self.movie_df["mov_type"] = list(map(lambda movie_type: map_types_to_fk[movie_type], self.movie_df["mov_type"]))

        self.genre_df = self.genre_df.reset_index()
        self.write_to_csv_files()
        self.insert_into_db()

        logging.info("Insertion into actor table is done")

    def get_actor_hrefs(self, list_page):
        """Get hrefs for all the relevant actors/ actresses.

        :param list_page: parsed HTML for "actor list page"
        :type list_page: BeautifulSoup
        :return: list of hrefs, one for each actor
        """
        # compile regex up front to increase performance
        match_actor_id = re.compile("(?<=\/name\/)\w*")
        match_actor_rank = re.compile("[1-9][0-9]*")
        hrefs = dict()
        actor_header = list_page.select(
            "#main > div > div.lister.list.detail.sub-list > div.lister-list > * > div.lister-item-content > h3")

        def get_actor_id(header_line):
            actor_id_link = header_line.find("a")
            if actor_id_link.has_attr("href"):
                actor_id_match = re.search(match_actor_id, actor_id_link["href"])
                if actor_id_match:
                    # get first (and only) match
                    actor_id = actor_id_match.group(0)
                    return actor_id
            else:
                logging.error("Could not retrieve an actor id!")
                return ""

        def get_actor_rank(header_line):
            actor_rank_span = header_line.find("span")
            actor_rank_match = re.search(match_actor_rank, actor_rank_span.get_text())
            if actor_rank_match:
                # get first (and only) match
                actor_rank = actor_rank_match.group(0)
                return actor_rank

        for header in actor_header:
            actor_id = get_actor_id(header)
            actor_rank = get_actor_rank(header)
            hrefs[actor_id] = actor_rank
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
        url = BASE_DOMAIN + ACTOR_PAGE_PREFIX + actor_href + "/bio"
        bio_page = requests.get(url, headers=REQ_HEADERS, proxies=proxy)
        if bio_page.status_code != 200:
            logging.warning("Failed to get biography from %s. Status code: %d", url, bio_page.status_code)
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

        # compile regex up-front to increase performance
        match_movie_id = re.compile("(?<=\/title\/)\w*")
        match_movie_type = re.compile("(?<=\().+?(?=\))")
        match_year = re.compile("[1-2][0-9][0-9][0-9]")
        match_invalid_chars = re.compile("\xa0|\n")
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
                    year_str = re.sub(match_invalid_chars, "", year_str)
                    year_str = re.search(match_year, year_str)
                    if year_str:
                        year = int(year_str.group(0))
                if i == 3:
                    movie_link = next(element.children)
                    # only get the number no need too get the /name prefix
                    href_match = re.search(match_movie_id, movie_link["href"])
                    if href_match:
                        # the first match is the relevant one (there is only one match)
                        href = href_match.group(0)
                    title = movie_link.get_text()
                if i == 4:
                    # There might be a movie status in brackets instead of the movie type
                    if not ("class" in element and element["class"] == "in_production"):
                        movie_type_match = re.search(match_movie_type, element.get_text())
                        if movie_type_match:
                            # there might be a movie type there might not be one, if not the type is movie as defined above
                            type = movie_type_match.group(0)
            movies[href] = Movie(movie_href=href, title=title, year=year, type=type)
        return movies

    def get_actor_awards(self, actor_href):
        """
        Get all awards an actor/ actress has won or was nominated for.

        :param actor_href: href to the actor detail page
        :type actor_href: str
        :return: list of awards the actor/ actress has won or was nominated for
        """
        url = BASE_DOMAIN + ACTOR_PAGE_PREFIX + actor_href + "/awards"
        actor_awards_page = requests.get(url, headers=REQ_HEADERS, proxies=proxy)
        if actor_awards_page.status_code != 200:
            logging.warning("Failed to get awards from %s. Status code: %d", url, actor_awards_page.status_code)
            return []
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

        # compile regex up front to increase performance
        match_movie_id = re.compile("(?<=\/title\/)\w*")

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
            href = ""
            desc_tag = award_row.find("td", class_="award_description")
            if desc_tag:
                for i, content in enumerate(desc_tag.contents):
                    if i == 0:
                        # award description here
                        desc = content.get_text().strip()
                    elif i == 3:
                        # if there is an href to a movie (starting with "/title/") get the string
                        href_exists = content.has_attr("href")
                        if href_exists:
                            # movie/ title name here; Add trailing slash to be compatible with movie href collected from actor details page,
                            # otherwise a foreign key error is thrown as the reference key will not be found because they are not the same
                            movie_id_regex_res = re.search(match_movie_id, content["href"])
                            if movie_id_regex_res:
                                # get first (and only) match
                                href = movie_id_regex_res.group(0)
                            movie = content.get_text().strip()
            return desc, movie, href

        year = get_year(award_row)
        category, outcome = get_outcome(award_row)
        desc, movie, href = get_desc(award_row)

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

        if not year or isnan(year) and prev_award:
            year = prev_award.year
        # if there is no category get it from previous row
        if not category and prev_award:
            category = prev_award.category
        if not outcome and prev_award:
            outcome = prev_award.outcome

        return Award(year=year, outcome=outcome, desc=desc, movie=movie, movie_href=href, category=category)

    def get_actor_sex(self, actor_page):
        """Get sex of the actor/ actress

        :param actor_page: BeautifulSoup
        :type actor_page: BeautifulSoup
        :return: "M" for male, "F" for female
        """
        jobs = actor_page.find(id="name-job-categories")
        # check wether a link with href to actor exists if yes -> male, else female
        # As the list only has actors and actresses it must be either of the two
        actor = jobs.find("a", attrs={"href": "#actor"})
        if not actor:
            sex = "F"
        else:
            sex = "M"
        return sex

    def get_actor_details(self, actor_href, rank):
        """Get all details to an actor/ actress.

        :param actor_href: href to an actor/ actress
        :type actor_href: str
        :param rank: rank of actor/ actress
        :type rank: int
        :return: an actor/ actress with their details
        """
        actor_url = BASE_DOMAIN + ACTOR_PAGE_PREFIX + actor_href
        logging.info("Getting details for actor %s from %s...", actor_href, actor_url)
        actor_page = requests.get(actor_url, headers=REQ_HEADERS, proxies=proxy)
        if actor_page.status_code != 200:
            logging.warning("Failed to get actor from %s. Status code: %d", actor_url, actor_page.status_code)
            return None
        parsed_actor_page = BeautifulSoup(actor_page.text, "html.parser")
        # Get fullname
        fullname = parsed_actor_page.find("span", class_="itemprop").get_text()
        sex = self.get_actor_sex(parsed_actor_page)
        # Get biography
        bio = self.get_actor_bio(actor_href)
        # Get image URL
        img = self.get_actor_img(parsed_actor_page)
        # Get movies
        movies = self.get_actor_movies(parsed_actor_page)
        # Merge movie dicts so movies will not be fetched twice (use lock to guarantee this operation is thread-safe)
        with self._merge_dict_lock:
            before = len(self.movie_dict)
            self.movie_dict = self.movie_dict | movies
            after = len(self.movie_dict)
            new = after - before
            # determine how many additional steps need to be done (number of unprecedented movies) and update current
            # step count by one as one actor is processed
            self.progress.increment_max(increment=new)
        # Get awards
        awards = self.get_actor_awards(actor_href)
        # Create a new actor object for an actor/ actress with all their details
        actor = Actor(actor_href=actor_href, rank=rank, fullname=fullname, bio=bio, awards=awards, movies=movies.keys(),
                      sex=sex, img=img)
        logging.info("Done. Got all details for actor %s \n%s", actor_url, actor)
        return actor

    def get_all_movies_details(self):
        """
        Get all details to all movies.

        :return:
        """

        no_movies = len(self.movie_dict)

        def process_movie(href, movie, count):
            url = BASE_DOMAIN + MOVIE_PAGE_PREFIX + href
            logging.info("(%d/%d) Getting movie details for movie %s", count + 1, no_movies, url)
            self.get_movie_details(href, movie)
            logging.info("(%d/%d) Got details for movie %s:\n%s", count + 1, no_movies, url, movie)
            # add one more movie to processed (so progress is shown correctly)
            self.progress.increment_cur(increment=1)

        start = timer()
        workers = [self.executor.submit(process_movie, href, movie, count) for count, (href, movie) in
                   enumerate(self.movie_dict.items())]
        done_tasks, pending_tasks = concurrent.futures.wait(workers, return_when=FIRST_EXCEPTION)
        end = timer()
        logging.info("Workers done: Tasks completed: %d\tTasks pending: %s", len(done_tasks), len(pending_tasks))
        elapsed = end - start
        logging.info("Gathered all movie data in %dmin %dsec", int(elapsed // 60), int(elapsed % 60))

    def get_movie_details(self, movie_href, movie):
        """Get all details for a specific movie.

        :param movie_href: href to a movie
        :type movie_href: str
        :param movie: movie object
        :type movie: Movie
        :return: all details for a specific movie
        """
        url = BASE_DOMAIN + MOVIE_PAGE_PREFIX + movie_href
        movie_page = requests.get(url, headers=REQ_HEADERS, proxies=proxy)
        if movie_page.status_code != 200:
            logging.warning("Failed to get movie details for %s. Status code: %d", url, movie_page.status_code)
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
        genres = set()

        if genre_div:
            # actual genre names are in spans with "ipc-chip__text" class
            genre_spans = genre_div.find_all("span", class_="ipc-chip__text")

            for genre in genre_spans:
                gtxt = genre.get_text()
                genres.add(gtxt)
                with self._all_genres_lock:
                    self.all_genres.add(gtxt)

        # add missing information to movie instances
        movie.genres = genres
        movie.rating = rating

    def get_all_actors_details(self, actors_with_rank):
        """Get all details to all actors.

        :param actors_with_rank: list of hrefs to an actor`s page
        :type actors_with_rank: dict[str,str]
        :return: list of actors/ actresses with their details
        """

        actors = list()
        list_lock = threading.Lock()
        logging.info(actors_with_rank)
        total_count = len(actors_with_rank)

        def process_actor(href, rank, count):
            logging.info("(%d/%d) Current actor: %s", count, total_count, href)
            actor_detail = self.get_actor_details(href, rank)
            with list_lock:
                actors.append(actor_detail)
                self.progress.increment_cur(increment=1)

        start = timer()
        workers = [self.executor.submit(process_actor, href, rank, count + 1) for count, (href, rank) in enumerate(actors_with_rank.items())]
        done_tasks, pending_tasks = concurrent.futures.wait(workers, return_when=ALL_COMPLETED)
        end = timer()
        logging.info("Workers done: Tasks completed: %d\tTasks pending: %s", len(done_tasks), len(pending_tasks))
        elapsed = end - start
        logging.info("Gathered all actor data in %dmin %dsec", int(elapsed // 60), int(elapsed % 60))
        return actors


# scraper = WebScraper()
# scraper.scrape()

# scraper.read_from_csv_files()
# scraper.insert_into_db()
# result = scraper.get_movie_details("tt0134119", Movie("tt0134119", "test", 2021, "Movie"))
# print(result)
