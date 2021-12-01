/**
 * Request deletion of all data from database.
 * @returns true if deletion is successful, false otherwise
 */
export async function deleteAllDataFromDb(): Promise<boolean>{
    const response = await fetch("/api/delete-all", { method: "DELETE"});
    const parsed = await response.json()
    return parsed.success;
}

/**
 * Triggers the start of the web scraping process. First data is web scraped from https://imdb.com
 * then it is inserted into the PostgreSQL database.
 * @returns true if web scraping has successfully been started, false otherwise
 */
export async function triggerWebscraping(): Promise<void>{
    const response = await fetch("/api/scrape", { method: "POST"});
    const parsed = await response.json()
    return parsed.success;
}