import { TActSex } from "./types";

/**
 * Maps identifier for actor/ actress sex to its UI string representation.
 */
export const mapSexIdentToTxt: Record<TActSex, string> = {
    M: "Male",
    F: "Female",
    D: "Diverse"
}

export const authorDetails = {
    firstName: "Thomas",
    lastName: "Pilz",
    img: "https://temp-bucket-imdb-analyser.s3.eu-central-1.amazonaws.com/Thomas_Pilz_bearbeitet.png"
}

export const baseDomain = "https://imdb.com";
export const moviePrefix = "/title/";
export const actorPrefix = "/name/";

export const maxRating = 10; 