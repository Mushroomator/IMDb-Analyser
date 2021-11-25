import { TSex } from "../types";
import { Award } from "./Award";
import { Movie } from "./Movie";

/**
 * An actor/ actress with all their information.
 * @class Actor
 * @author Thomas Pilz
 */
export class Actor{
    /**
     * Actor's first name
     */
    private _firstName: string;
    public get firstName(): string {
        return this._firstName;
    }
    public set firstName(value: string) {
        this._firstName = value;
    }
    /**
     * Actor's last name
     */
    private _lastName: string;
    public get lastName(): string {
        return this._lastName;
    }
    public set lastName(value: string) {
        this._lastName = value;
    }
    private _sex: TSex;
    public get sex(): TSex {
        return this._sex;
    }
    public set sex(value: TSex) {
        this._sex = value;
    }
    private _img: URL;
    public get img(): URL {
        return this._img;
    }
    public set img(value: URL) {
        this._img = value;
    }
    private _bio: string;
    public get bio(): string {
        return this._bio;
    }
    public set bio(value: string) {
        this._bio = value;
    }
    private _movies: Array<Movie>;
    public get movies(): Array<Movie> {
        return this._movies;
    }
    public set movies(value: Array<Movie>) {
        this._movies = value;
    }
    private _awards: Array<Award>;
    public get awards(): Array<Award> {
        return this._awards;
    }
    public set awards(value: Array<Award>) {
        this._awards = value;
    }
    
    /**
     * Create a new actor/ actress
     * @param firstName first name
     * @param lastName last name
     * @param sex sex of actor/ actress
     * @param img URL to image
     * @param bio short biography
     * @param movies list of movies the actor has down
     * @param awards list of awards the actor has won
     */
    constructor(firstName: string, lastName: string, sex: TSex, img: URL, bio: string, movies: Array<Movie>, awards: Array<Award>){
        this._firstName = firstName;
        this._lastName = lastName;
        this._sex = sex;
        this._img = img;
        this._bio = bio;
        this._movies = movies;
        this._awards = awards;
    }
}