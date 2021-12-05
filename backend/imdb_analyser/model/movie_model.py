from imdb_analyser.utils import DatabaseConnector

def get_all_movies():
    """
    Get all movies independent of actor.

    :return: all movies
    """

    query = """
            SELECT mov.mov_href,
	               mov.mov_title,
	               mov.mov_year,
	               mov.mov_rating,
	               mt.met_name
            FROM movie AS mov
            INNER JOIN medium_type AS mt ON mov.mov_type = mt.met_id
            """

    genres = DatabaseConnector.query(query_str=query)
    return genres

def get_all_movie_genres():
    """
    Select all movie-IDs and all the genres assigend to each of those ids

    :return: list of movie-ID and genres
    """
    query = """
    SELECT mg.mg_movie_href,
	gen.genre_name
    FROM movie_genre AS mg
    INNER JOIN genre AS gen ON gen.genre_id = mg.mg_genre_id
    """
    movie_genres = DatabaseConnector.query(query_str=query)
    return movie_genres