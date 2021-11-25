import os
import logging

from flask import Flask

app = Flask(__name__, static_folder="../../frontend/build", static_url_path="/")

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(name)s]  [%(levelname)s] %(message)s')


@app.route("/")
def index():
    """
    Serve index.html so the react frontend can start up and take over.
    :return: index.html
    """
    return app.send_static_file("index.html")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    host = "localhost"
    app.logger.info("Starting Flask server listening on %s:%s", host, port)
    app.run(host=host, port=port)
