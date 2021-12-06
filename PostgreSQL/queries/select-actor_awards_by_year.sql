/*
Get all awards an actor/ actress has won or was nominated for.

Here an example for actor '/name/nm0000136' => Johnny Depp
*/
SELECT aw.aw_year,
	aw.aw_outcome,
	aw.aw_description,
	aw.aw_movie_name,
	aw.aw_movie_href,
	ac.awc_cat_name
FROM actor AS act
INNER JOIN award AS aw ON aw.aw_actor_href = act.act_href
INNER JOIN award_category as ac ON ac.awc_id = aw.aw_category_id
WHERE act.act_href = '/name/nm0000136'
group by aw.aw_year,
	aw.aw_outcome,
	aw.aw_description,
	aw.aw_movie_name,
	aw.aw_movie_href, 
	aw.aw_category_id,
	ac.awc_cat_name
order by aw.aw_year DESC, aw.aw_category_id;