/*
	Create table to store actor information
*/
CREATE TABLE IF NOT EXISTS actor (
	act_href varchar(15) PRIMARY KEY NOT NULL,
    act_fullname varchar(50) NOT NULL,
    -- "F": Female, "M": Male, "D": Diverse
	act_sex char(1) NOT NULL,
	act_img_url varchar(255) NOT NULL,
    act_bio text NOT NULL
);

/*
	Create table to store award category information
*/
CREATE TABLE IF NOT EXISTS award_category  (
	awc_id SMALLINT PRIMARY KEY NOT NULL,
    awc_cat_name varchar(50) NOT NULL
);

/*
	Create table to store movie medium_types
*/
CREATE TABLE IF NOT EXISTS medium_type (
	met_id smallint PRIMARY KEY NOT NULL,
	met_name varchar(25) NOT NULL
);

/*
	Create table to store movies
*/
CREATE TABLE IF NOT EXISTS movie (
	mov_href varchar(10) PRIMARY KEY NOT NULL,
	mov_title varchar(80) NOT NULL,
	-- movie might not have been released yet so it can be null
	mov_year smallint,
	mov_type smallint NOT NULL,
	mov_rating DECIMAL(2,1),
	FOREIGN KEY (mov_type) REFERENCES medium_type(met_id)
);

/*
	Create table to store award information
*/
CREATE TABLE IF NOT EXISTS award  (
    aw_actor_href varchar(15) NOT NULL,
	aw_id SMALLINT NOT NULL,
	aw_year SMALLINT NOT NULL,
    -- "Winner" or "Nominee" 
	aw_outcome varchar(7) NOT NULL,
	aw_description varchar(255),
	aw_movie_href varchar(10),
	aw_movie_name varchar(255),
    aw_category_id SMALLINT,
	PRIMARY KEY (aw_id, aw_actor_href),
	FOREIGN KEY (aw_actor_href) REFERENCES actor (act_href),
    FOREIGN KEY (aw_category_id) REFERENCES award_category(awc_id)
);

/*
	Create table to store images
*/
CREATE TABLE IF NOT EXISTS genre (
	genre_id smallint PRIMARY KEY NOT NULL,
    genre_name varchar(25) NOT NULL
);

/*
	Create table to store movie genres
*/
CREATE TABLE IF NOT EXISTS movie_genre  (
	mg_movie_href varchar(10) NOT NULL,
    mg_genre_id smallint NOT NULL,
	PRIMARY KEY (mg_movie_href, mg_genre_id),
	FOREIGN KEY (mg_movie_href) REFERENCES movie(mov_href),
	FOREIGN KEY (mg_genre_id) REFERENCES genre(genre_id)
);

/*
	Create table to store cast for movies
*/
CREATE TABLE IF NOT EXISTS movie_cast (
	cast_actor_href varchar(15) NOT NULL,
	cast_movie_href varchar(10) NOT NULL,
	PRIMARY KEY (cast_actor_href, cast_movie_href),
	FOREIGN KEY (cast_actor_href) REFERENCES actor(act_href),
	FOREIGN KEY (cast_movie_href) REFERENCES movie(mov_href)
);