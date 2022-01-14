import logging
import os

from flask import Flask

from imdb_analyser.controller.main_controller import main_controller
from imdb_analyser.controller.actor_controller import actor_controller
from imdb_analyser.controller.movie_controller import movie_controller

# serve static files required for react
app = Flask(__name__, static_folder="../../frontend/build", static_url_path="/")

# register controllers
app.register_blueprint(main_controller)
app.register_blueprint(movie_controller)
app.register_blueprint(actor_controller)

# configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(name)s]  [%(levelname)s] %(message)s')

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

if __name__ == "__main__":
    # Start the application
    port = int(os.getenv("PORT", 5000))
    host = "localhost"
    app.logger.info("Starting Flask server listening on %s:%s", host, port)
    app.run(host=host, port=port)
