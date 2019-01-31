from .log import logger
from flask import Flask, jsonify
import logging

httpd = Flask("honeycast")

werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.disabled = True
httpd.logger = logger

@httpd.after_request
def set_custom_headers(response):
    response.headers["Server"] = ""
    return response

@httpd.route("/setup/reboot", methods=["POST"])
def reboot():
    return "", 200

@httpd.route("/setup/eureka_info", methods=["GET"])
def eureka_info():
    return jsonify({
        "name": "ThisIsName",
        "detail": {
            "model_name": "ThisIsModelName",
            "manufacturer": "JJ"
        }
    })

@httpd.route("/", defaults={ "path": "" })
@httpd.route("/<path:path>")
def catch_all(path):
    logger.info("not implemented route: %s", path)
    return "", 200

if __name__ == "__main__":
    httpd.run(debug=True)
