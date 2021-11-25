/**
 * Information for an actor/ actress
 */
export interface IActor {
    firstName: string
    lastName: string
    sex: TSex
    img: string
    bio: string
}

/**
 * Details for an actor/ actress
 */
export interface IActorDetails extends IActor {
    movies: Array<IMovie>
    awards: Array<IAward>
};

/**
 * Information on a movie
 */
export interface IMovie {
    title: string
    rating: number
    genres: Array<TMovieGenre>
    year: number
};

/**
 * Inforamtion on an award
 */
export interface IAward {
    name: string,
    year: number,
}

/**
 * Movie genre
 */
export type TMovieGenre = string;

/**
 * Sex of a person
 */
export type TSex = "Male" | "Female" | "Non-binary";

