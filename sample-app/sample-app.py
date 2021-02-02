from flask import Flask
from flask import request
from logging.config import dictConfig
import logging
import asyncio
import os
import sys


class TestClient:
    def __init__(self):
        self.globalData = "Hello team, This is a test client app\n"
        self.failureData = "On purpose FAILURE, dofail = yes\n"
        self.badRequest = "Record Not Found\n"


app = Flask(__name__)

test_client = TestClient()

"""
curl http://0.0.0.0:8080?dofail=yes to return a 500
curl http://0.0.0.0:8080 for other statuses
"""


@app.route("/", methods=["GET"])
def getSomeData():
    try:
        req = request.args.get("dofail")
        if req == "yes":
            app.logger.critical("On purpose FAILURE, dofail = yes\n")
            return test_client.failureData, 500

    except Exception as e:
        msg = "Bad Request (400): " + str(e)
        app.logger.info(msg)
        # print(msg)
        return msg, 400
    app.logger.info("SUCCESS\n")
    return test_client.globalData, 200


"""
curl http://0.0.0.0:8080/crash to cause flask / python to exit
"""


@app.route("/crash", methods=["GET"])
def crash():
    app.logger.info("client app trying to exit")

    # sys.exit would work but os.exit will cause python to exit with flask apps.
    # https://stackoverflow.com/questions/52427999/python-flask-app-not-exiting-with-sys-exit
    os._exit(0)


# Set up logging (formatters, handlers and levels) -> log handler to sys.stdout
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "CRITICAL" "handlers": ["wsgi"]},
    }
)


async def main_async():
    # Initialize logging
    if not app.debug:
        handler = logging.StreamHandler(sys.stdout)
        app.logger.addHandler(handler)

    # Set the logger level -> (default) log handler to sys.stderr
    # app.logger.setLevel(logging.INFO)
    # app.logger.setLevel(logging.CRITICAL)

    # Log App Test Client Start
    app.logger.info("LOB App Test Client starting...\n")

    # Run the flask app
    await app.run(host="0.0.0.0", port=8080)

    # Log App test client finish
    app.logger.info("LOB App Test Client Finished.\n")


if __name__ == "__main__":
    asyncio.run(main_async())
