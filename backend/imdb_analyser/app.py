import logging
import os
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, redirect, url_for

from imdb_analyser.utils.WebscrapingStatus import WebscrapingStatus
from imdb_analyser.controller.actor_controller import actor_controller
from imdb_analyser.controller.movie_controller import movie_controller
from imdb_analyser.utils import DatabaseConnector
from utils.WebScraper import WebScraper

# serve static files required for react
app = Flask(__name__, static_folder="../../frontend/build", static_url_path="/")

# register controllers
app.register_blueprint(movie_controller)
app.register_blueprint(actor_controller)

# configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(name)s]  [%(levelname)s] %(message)s')

web_scraper = None
"""
:type web_scraper: WebScraper
Global instance of webscraper, which makes sure only
one instance of a webscraper can run at any one time.
"""
no_all_actors = 50


@app.errorhandler(404)
def page_not_found(err):
    """
    Serve index.html so the React frontend can start up and take over.
    Because client-side routing is in-place reloading the page which is not the "/"
    route will result in a 404 error. In that case just send the "index.html"
    so the client-side routing will take effect again.

    :return: index.html
    """
    return app.send_static_file("index.html")


@app.route("/")
def index():
    """
    Serve index.html so the React frontend can start up and take over.
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
    global web_scraper

    if web_scraper:
        redirect(url_for("handle_progress"))

    web_scraper = WebScraper()
    # start webscraping in another thread so the main thread can keep serving requests
    executor = ThreadPoolExecutor(max_workers=1)
    DatabaseConnector.delete_all_data()
    logging.info("Starting webscraping master thread...")

    future = executor.submit(web_scraper.scrape)
    future.add_done_callback(lambda _: logging.info("Webscraping master thread finished."))

    return {
        "success": True,
        "message": "Started web scraping from https://imdb.com...",
        "monitorProgressVia": {
            "endpoint": "/api/v1/scrape/progress",
            "method": "POST",
            "intervalInS": 5
        }
    }


@app.route("/api/v1/scrape/progress", methods=["POST"])
def handle_progress():
    """
    Handles request for progress updates on the webscraping process.

    :return: progress in percent of webscraping process, and status of webscraping process
    """
    global web_scraper

    if not web_scraper:
        # there is no web scraping going on at the moment
        return {
            "status": WebscrapingStatus.IDLE,
            "progress": 0
        }
    progress = web_scraper.progress.get_progress()
    if progress == 100:
        # Webscraping is done, let garbage collector pick up
        # the webscraper instance and report that the job is done
        web_scraper = None
        return {
            "status": WebscrapingStatus.FINISHED,
            "progress": progress
        }

    # webscraping is in progress, report current progress
    return {
        "status": WebscrapingStatus.RUNNING,
        "progress": progress
    }


@app.route("/api/v1/healthcheck")
def handle_healthcheck():
    """
    Handle a healtcheck request to make sure the webserver is still up and running.
    User e.g. by the Docker image.

    :return:
    """
    return {
        "status": "Up"
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    host = "localhost"
    app.logger.info("Starting Flask server listening on %s:%s", host, port)
    app.run(host=host, port=port)
