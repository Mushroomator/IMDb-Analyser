import { IDeleteAllResponse, ITriggerWebscrapingResponse, IWebscrapingProgressResponse } from "./types";

/**
 * Request deletion of all data from database.
 * @returns true if deletion is successful, false otherwise
 */
export async function deleteAllDataFromDb(): Promise<boolean>{
    try {
        const response = await fetch("/api/v1/delete-all", { method: "DELETE"});
        const parsed: IDeleteAllResponse = await response.json();
        return parsed.success;
    } catch (error) {
        return false;
    }
}

/**
 * Triggers the start of the web scraping process. First data is web scraped from https://imdb.com
 * then it is inserted into the PostgreSQL database.
 * @returns true if web scraping has successfully been started, false otherwise
 */
export async function triggerWebscraping(): Promise<ITriggerWebscrapingResponse | null>{
    try {
        const response = await fetch("/api/v1/scrape", { method: "POST"});
        const parsed: ITriggerWebscrapingResponse = await response.json();
        return parsed;
    } catch (error) {
        return null;
    }
}

/**
 * Get progress of webscraping process.
 * @returns progress in percent
 */
export async function getWebscrapingProgress(): Promise<IWebscrapingProgressResponse | null>{
    try {
        const response = await fetch("/api/v1/scrape/progress", { method: "POST" });
        const parsed: IWebscrapingProgressResponse = await response.json();
        return parsed;
    } catch (error) {
        return null
    }
}