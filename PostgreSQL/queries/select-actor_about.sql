/*
Select all information about an actor/ actress.

Here an example for actor '/name/nm0000136' => Johnny Depp
*/
SELECT act_href,
	   act_fullname,
	   act_sex,
	   act_img_url,
	   act_bio
FROM actor
WHERE act_href = '/name/nm0000136';