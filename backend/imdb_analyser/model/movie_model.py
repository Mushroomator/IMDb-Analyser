from imdb_analyser.utils import DatabaseConnector


def get_all_movies():
    """
    Get all movies independent of actor.

    :return: all movies
    """

    query = """
    SELECT distinct(gen.genre_name)
    FROM actor AS act
    INNER JOIN movie_cast AS mc ON act.act_href = mc.cast_actor_href
    INNER JOIN movie_genre AS mg ON mg.mg_movie_href = mc.cast_movie_href
    INNER JOIN genre AS gen ON gen.genre_id = mg.mg_genre_id
    WHERE act.act_href = %(actor_id)s;
    """

    genres = DatabaseConnector.query(query_str=query, query_params={"actor_id": actor_id})
    return genres