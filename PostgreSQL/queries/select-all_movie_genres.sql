/*
Select all movies and their genres in the database (independent of actor).
*/
SELECT mg.mg_movie_href,
	gen.genre_name
    FROM movie_genre AS mg
    INNER JOIN genre AS gen ON gen.genre_id = mg.mg_genre_id;