from imdb_analyser.utils import DatabaseConnector

def get_all_actors_about():
    """
    Get all information about all actors/ actresses

    :return: all information about all actors/ actresses
    """
    query = """
        SELECT act_href,
    	       act_fullname,
    	       act_sex,
    	       act_img_url,
    	       act_bio
        FROM actor
        """

    actor_about = DatabaseConnector.query(query_str=query)
    return actor_about

def get_actor_about(actor_id):
    """
    Get all information about an actor/ actress

    :param actor_id: actor-ID
    :return: all information about an actor/ actress
    """
    query="""
    SELECT act_href,
	       act_fullname,
	       act_sex,
	       act_img_url,
	       act_bio
    FROM actor
    WHERE act_href = %(actor_id)s;
    """

    actor_about = DatabaseConnector.query(query_str=query, query_params={"actor_id": actor_id})
    return actor_about

def get_actor_genres(actor_id):
    """
    Get all genres the actor has covered.

    :param actor_id: actor-ID
    :type actor_id: str
    :return: genres for the specified actor
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


def get_actor_movies(actor_id):
    """
    Get all movies an actor has played in.

    :param actor_id: actor-ID
    :type actor_id: str
    :return: all movies
    """
    query = """
        SELECT mov.mov_href,
               mov.mov_title,
    	       mov.mov_year,
    	       mov.mov_rating,
    	       mt.met_name
        FROM actor AS act
        INNER JOIN movie_cast AS mc ON act.act_href = mc.cast_actor_href
        INNER JOIN movie AS mov ON mc.cast_movie_href = mov.mov_href
        INNER JOIN medium_type as mt ON mov.mov_type = mt.met_id
        WHERE act.act_href = %(actor_id)s;
        """
    results = DatabaseConnector.query(query_str=query, query_params={"actor_id": actor_id})
    return results

def get_all_movie_genres(actor_id):
    """
        Get all movies and their genres for a given actor.

        :param actor_id: actor-ID
        :type actor_id: str
        :return: all movies the actor was in and their genres
        """
    query = """
            SELECT mg.mg_movie_href,
	               gen.genre_name
            FROM actor AS act
            INNER JOIN movie_cast AS mc ON act.act_href = mc.cast_actor_href
            INNER JOIN movie_genre AS mg ON mg.mg_movie_href = mc.cast_movie_href
            INNER JOIN genre AS gen ON gen.genre_id = mg.mg_genre_id
            WHERE act.act_href = %(actor_id)s;
            """
    results = DatabaseConnector.query(query_str=query, query_params={"actor_id": actor_id})
    return results

def get_actor_awards(actor_id):
    """
    Get all awards an actor/ actress has won or was nominated for.

    :param actor_id: actor-ID
    :return: all awards for an actor/ actress
    """

    query = """
    SELECT aw.aw_year,
           aw.aw_outcome,
           aw.aw_description,
           aw.aw_movie_name,
           aw.aw_movie_href,
           ac.awc_cat_name
        FROM actor AS act
        INNER JOIN award AS aw ON aw.aw_actor_href = act.act_href
        INNER JOIN award_category as ac ON ac.awc_id = aw.aw_category_id
        WHERE act.act_href = %(actor_id)s
        group by aw.aw_year,
        	aw.aw_outcome,
        	aw.aw_description,
        	aw.aw_movie_name,
        	aw.aw_movie_href, 
        	aw.aw_category_id,
        	ac.awc_cat_name
        order by aw.aw_year DESC, aw.aw_category_id;
    """

    awards = DatabaseConnector.query(query_str=query, query_params={"actor_id": actor_id})
    return awards