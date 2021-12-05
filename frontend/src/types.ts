/**
 * All allowed values for sex of an actor/ actress
 */
export type TActSex = "M" | "F" | "D";

/**
 * All information to life of an actor/ actress
 */
export interface IActorAbout {
    act_bio: string
    act_rank: number
    act_fullname: string
    act_href: string
    act_img_url: string
    act_sex: TActSex
}

/**
 * All information about a movie
 */
export interface IActorMovie {
    mov_genres: Array<string>
    met_name: string
    mov_href: string
    mov_rating: number
    mov_title: string
    mov_year: number
}

/**
 * Mean movie rating per year
 */
export interface IPerYearMovieRating {
    mov_rating: number
    mov_year: number
}

/**
 * Information on a award
 */
export interface IActorAward {
    aw_description: string,
    aw_movie_href: string,
    aw_movie_name: string,
    aw_outcome: string,
    aw_year: number,
    awc_cat_name: string
}

/**
 * Information for an actor/ actress
 */
export interface IActor {
    about: IActorAbout
}

/**
 * Response for request to /api/actors
 * containing all the actors and their information.
 */
export interface IActorsResponse {
    timestamp: string
    data: Array<IActorAbout>
}

export interface IActorDetailsResponse {
    timestamp: string
    data: IActorDetails
}

export interface IMovieResponse {
    timestamp: string
    data: Array<IActorMovie>
}

export interface ITriggerWebscrapingResponse {
    success: boolean
    message: string
    monitorProgressVia: {
        endpoint: string
        method: string
        intervalInS: number
    }
}

export interface IDeleteAllResponse {
    success: boolean
    message: string
}

export type TWebScrapingStatus = "idle" | "running" | "finished";

export interface IWebscrapingProgressResponse {
    status: TWebScrapingStatus
    progress: number
}

export interface IError {
    title: string
    desc: string
} 


/**
 * Details for an actor/ actress
 */
export interface IActorDetails extends IActor {
    allTimeMovies: Array<IActorMovie>
    topFiveMovies: Array<IActorMovie>
    overallRating: number
    perYearRating: Array<IPerYearMovieRating>
    awards: Array<IActorAward>
    genres: Array<string>
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
 * Interface to provide is loading props
 */
export interface IIsLoading {
    isLoading: boolean
    setIsLoading: React.Dispatch<React.SetStateAction<boolean>>
}

/**
 * Movie genre
 */
export type TMovieGenre = string;

/**
 * Sex of a person
 */
export type TSex = "Male" | "Female" | "Non-binary";

