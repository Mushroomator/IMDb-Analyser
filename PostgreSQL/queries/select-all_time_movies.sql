/*
Select all movies stored in the database (independent of actor).
*/
SELECT mov.mov_href,
       mov.mov_title,
       mov.mov_year,
       mov.mov_rating,
       mt.met_name
FROM movie AS mov
INNER JOIN medium_type AS mt ON mov.mov_type = mt.met_id;