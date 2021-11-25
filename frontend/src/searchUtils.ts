import { IActorDetails, IAward, IMovie, TSex } from "./types";

/**
 * Find all actors which have the a search string in some of their properties. Case sensitive.
 * @param allActors actors to be search
 * @param searchStr string to find
 * @returns all actors which property values contain the string
 */
export function searchForStrInActors(allActors: Array<IActorDetails>, searchStr: string): Array<IActorDetails> {
    if (searchStr === "") return allActors;
    const results: Array<IActorDetails> = [];
    allActors.forEach(it => {
        if (it.firstName.toLowerCase().includes(searchStr) 
        || it.lastName.toLowerCase().includes(searchStr) 
        || it.bio.toLowerCase().includes(searchStr)
        || it.sex.toLowerCase().includes(searchStr)
        || searchForStrInAwards(it.awards, searchStr)
        || searchForStrInMovies(it.movies, searchStr)) results.push(it);
    });
    return results;
}

function searchForStrInAwards(allAwards: Array<IAward>, searchStr: string): boolean {
    let found = false;
    allAwards.some(award => {
        console.log(`Search string:`, searchStr, "Name", award.name)
        if(award.name.toLowerCase().includes(searchStr) || award.year.toString().includes(searchStr)) {
            found = true;
            return true;
        }
        else return false;
    })
    return found;
}

function searchForStrInMovies(allMovies: Array<IMovie>, searchStr: string): boolean {
    let found = false;
    allMovies.some(movie => {
        if(movie.title.toLowerCase().includes(searchStr) || movie.year.toString().includes(searchStr) || movie.genres.some(genre => genre.toLowerCase().includes(searchStr) ? true: false)) {
            found = true;
            return true;
        }
        else return false;
    })
    return found;
}

export function actors2LowerCase(allActors: Array<IActorDetails>): Array<IActorDetails>{
    return allActors.map(actor => {
        actor.bio = actor.bio.toLowerCase()
        actor.firstName = actor.firstName.toLowerCase()
        actor.lastName = actor.lastName.toLowerCase()
        actor.movies = movies2LowerCase(actor.movies);
        actor.awards = awards2LowerCase(actor.awards);
        actor.sex = actor.sex.toLowerCase() as TSex;
        return actor;
    });
}

function movies2LowerCase(allMovies: Array<IMovie>): Array<IMovie>{
    return allMovies.map(movie => {
        movie.title = movie.title = movie.title.toLowerCase();
        movie.genres = movie.genres.map(genre => genre.toLowerCase())
        return movie;
    });
}

function awards2LowerCase(allAwards: Array<IAward>): Array<IAward>{
    return allAwards.map(award => { 
        award.name = award.name.toLowerCase()
        return award;
    });
}