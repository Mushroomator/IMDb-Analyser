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

if __name__ == "__main__":
    # Start the application
    port = int(os.getenv("PORT", 5000))
    host = "localhost"
    app.logger.info("Starting Flask server listening on %s:%s", host, port)
    app.run(host=host, port=port)
