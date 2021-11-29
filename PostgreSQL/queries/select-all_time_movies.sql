/*
Query an actor's/actress's all time movies.

Here an example for actor '/name/nm0000136' => Johnny Depp
*/
SELECT mov.mov_title,
	mov.mov_year
FROM actor AS act
INNER JOIN movie_cast AS mc ON act.act_href = mc.cast_actor_href
INNER JOIN movie AS mov ON mc.cast_movie_href = mov.mov_href
WHERE act.act_href = '/name/nm0000136';