import { TActSex } from "./types";

/**
 * Maps identifier for actor/ actress sex to its UI string representation.
 */
export const mapSexIdentToTxt: Record<TActSex, string> = {
    M: "Male",
    F: "Female",
    D: "Diverse"
}

export const baseDomain = "https://imdb.com";
export const moviePrefix = "/title/";
export const actorPrefix = "/name/";

export const maxRating = 10; 