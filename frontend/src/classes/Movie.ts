import { TMovieGenre } from "../types";

export class Movie {
    private title: string;
    private rating: number;
    private genres: Array<TMovieGenre>;
    private year: number;

    constructor(title: string, rating: number, genres: Array<TMovieGenre>, year: number){
        this.title = title 
        this.rating = rating
        this.genres = genres
        this.year = year
    }
}