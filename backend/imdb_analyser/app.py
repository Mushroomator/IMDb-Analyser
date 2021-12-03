import concurrent.futures
import itertools
import logging
import os
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, redirect, url_for

from imdb_analyser.actor_controller import actor_controller
from imdb_analyser.movie_controller import movie_controller
from imdb_analyser.utils import DatabaseConnector
from utils.WebScraper import WebScraper

# serve static files required for react
app = Flask(__name__, static_folder="../../frontend/build", static_url_path="/")

# register controllers
app.register_blueprint(movie_controller)
app.register_blueprint(actor_controller)

# configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(name)s]  [%(levelname)s] %(message)s')

# create a thread pool with multiple worker threads to divide work
max_workers = 1
executor = ThreadPoolExecutor(max_workers=max_workers)
workers = []


web_scraper = None
no_all_actors = 50


@app.route("/")
def index():
    """
    Serve index.html so the react frontend can start up and take over.
    :return: index.html
    """
    return app.send_static_file("index.html")


@app.route("/api/v1/delete-all", methods=["DELETE"])
def handle_delete():
    """
    Deletion of all data in the database is requested.

    :return:
    """
    # delete all data in the database
    is_deleted = DatabaseConnector.delete_all_data()
    if is_deleted:
        msg = {
            "success": True,
            "message": "All data has been deleted!"
        }
    else:
        msg = {
            "success": False,
            "message": "Could not delete data in the database!"
        }
    return msg


@app.route("/api/v1/scrape", methods=["POST"])
def handle_web_scape():
    """
    Triggers webscraping from https://imdb.com

    :return:
    """
    global web_scraper, workers

    if web_scraper:
        redirect(url_for("/api/v1/scrape/progress"))
    scraper = WebScraper()
    web_scraper = scraper

    def web_scrape_task_done(future, thread_id):
        global web_scraper, workers
        app.logger.info("Worker %d used for web scraping is done.", thread_id)
        if thread_id == max_workers:
            web_scraper = None
            workers = tuple()
            app.logger.info("Web scraped everything")

    def create_web_scrape_task(thread_id):
        future = executor.submit(scraper.scrape)
        future.set_running_or_notify_cancel()
        future.add_done_callback(lambda future: web_scrape_task_done(future, thread_id))
        app.logger.info("Launching worker %d for web scraping...", thread_id)
        return future

    workers = (create_web_scrape_task(thread_id) for thread_id in range(1, max_workers + 1))

    return {
        "success": True,
        "message": "Started web scraping from https://imdb.com...",
        "progress": {
            "endpoint": "/api/v1/scrape/progress",
            "method": "POST",
            "askAgainInS": 10
        }
    }


@app.route("/api/v1/scrape/progress", methods=["POST"])
def handle_progress():
    if not web_scraper:
        return {
            "success": False,
            "message": "No webscraper running at the moment"
        }
    no_actors = web_scraper.processed_actors.get()
    progress = no_actors / no_all_actors
    return {
        "success": True,
        "progress": progress
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    host = "localhost"
    app.logger.info("Starting Flask server listening on %s:%s", host, port)
    app.run(host=host, port=port)
