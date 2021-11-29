/*
Select all movies and their genres for a given actor.

Here an example for actor '/name/nm0000136' => Johnny Depp
*/
SELECT mg.mg_movie_href,
	   gen.genre_name
    FROM actor AS act
    INNER JOIN movie_cast AS mc ON act.act_href = mc.cast_actor_href
    INNER JOIN movie_genre AS mg ON mg.mg_movie_href = mc.cast_movie_href
    INNER JOIN genre AS gen ON gen.genre_id = mg.mg_genre_id
    WHERE act.act_href = '/name/nm0000136';