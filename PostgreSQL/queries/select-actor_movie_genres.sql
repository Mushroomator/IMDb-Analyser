/*
Select all genres which an actor/ actress has covered.

Here an example for actor '/name/nm0000136' => Johnny Depp
*/
SELECT distinct(gen.genre_name)
FROM actor AS act
INNER JOIN movie_cast AS mc ON act.act_href = mc.cast_actor_href
INNER JOIN movie_genre AS mg ON mg.mg_movie_href = mc.cast_movie_href
INNER JOIN genre AS gen ON gen.genre_id = mg.mg_genre_id
WHERE act.act_href = '/name/nm0000136';