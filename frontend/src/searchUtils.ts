import { mapSexIdentToTxt } from "./config";
import { IActorAbout, IActorAward, IActorMovie, IPerYearMovieRating } from "./types";

/**
 * Find all actors which have the a search string in any of their properties. Case sensitive.
 * @param allActors actors to be search
 * @param searchStr string to find
 * @returns all actors which property values contain the string
 */
export async function searchForStrInActorsAbout(allActors: Array<IActorAbout>, searchStr: string): Promise<Array<IActorAbout>> {
    if (searchStr === "") return allActors;
    const results: Array<IActorAbout> = [];
    allActors.forEach(it => {
        if (it.act_fullname.toLowerCase().includes(searchStr)
            || it.act_bio.toLowerCase().includes(searchStr)
            || mapSexIdentToTxt[it.act_sex].toLowerCase().includes(searchStr)
            || it.act_href.toLowerCase().includes(searchStr)
            || it.act_img_url.toLowerCase().includes(searchStr)) results.push(it);
    });
    return results;
}

export async function searchForStrInRatings(all: Array<IPerYearMovieRating>, searchStr: string): Promise<Array<IPerYearMovieRating>> {
    if (searchStr === "") return all;
    const results: Array<IPerYearMovieRating> = [];
    all.forEach(it => {
        if (it.mov_rating.toString().includes(searchStr)
            || it.mov_year.toString().includes(searchStr)) results.push(it);
    });
    return results;
}

export async function searchForStrInMovies(all: Array<IActorMovie>, searchStr: string): Promise<Array<IActorMovie>> {
    if (searchStr === "") return all;
    const results: Array<IActorMovie> = [];
    all.forEach(it => {
        if (it.met_name.toString().toLowerCase().includes(searchStr)
            || it.mov_href.toString().toLowerCase().includes(searchStr)
            || it.mov_rating.toString().toLowerCase().includes(searchStr)
            || it.mov_title.toString().toLowerCase().includes(searchStr)
            || it.mov_year.toString().toLowerCase().includes(searchStr)
            || it.mov_genres.some(genre => genre.toLowerCase().includes(searchStr))) results.push(it);
    });
    return results;
}

export async function searchForStrInAwards(all: Array<IActorAward>, searchStr: string): Promise<Array<IActorAward>> {
    if (searchStr === "") return all;
    const results: Array<IActorAward> = [];
    all.forEach(it => {
        if (it.aw_description.toString().toLowerCase().includes(searchStr)
            || it.aw_movie_name.toString().toLowerCase().includes(searchStr)
            || it.aw_outcome.toString().toLowerCase().includes(searchStr)
            || it.aw_year.toString().toLowerCase().includes(searchStr)
            || it.awc_cat_name.toString().toLowerCase().includes(searchStr)
            || it.aw_movie_href.toString().toLowerCase().includes(searchStr)) results.push(it);
    });
    return results;
}