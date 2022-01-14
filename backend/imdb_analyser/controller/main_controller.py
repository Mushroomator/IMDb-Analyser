import logging
from concurrent.futures import ThreadPoolExecutor

from flask import redirect, url_for, Blueprint

from imdb_analyser.utils.WebscrapingStatus import WebscrapingStatus
from imdb_analyser.utils import DatabaseConnector
from imdb_analyser.utils.WebScraper import WebScraper

# configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(name)s]  [%(levelname)s] %(message)s')

# create main controller
main_controller = Blueprint("main_controller", __name__, url_prefix="/api/v1")

web_scraper = None
"""
:type web_scraper: WebScraper
Global instance of webscraper, which makes sure only
one instance of a webscraper can run at any one time.
"""
no_all_actors = 50


@main_controller.route("/delete-all", methods=["DELETE"])
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


@main_controller.route("/scrape", methods=["POST"])
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


@main_controller.route("/scrape/progress", methods=["POST"])
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


@main_controller.route("/healthcheck")
def handle_healthcheck():
    """
    Handle a healthcheck request to make sure the webserver is still up and running.
    Used e.g. by the Docker image.

    Note: what is returned is not really important. Just the fact that something has been returned
    is enough for docker to consider the container healthy.

    :return:
    """
    return {
        "status": "Up"
    }
