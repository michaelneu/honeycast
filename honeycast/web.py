from .config import config
from .log import logger, apply_logger_config
from flask import Flask, jsonify
import logging

httpd = Flask(__name__)

werkzeug_logger = logging.getLogger("werkzeug")
apply_logger_config(werkzeug_logger)

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
        "name": config.get("device.device_name", "Device Name"),
        "detail": {
            "model_name": config.get("device.model_name", "Model Name"),
            "manufacturer": config.get("device.manufacturer", "Cast")
        }
    })

@httpd.route("/", defaults={ "path": "" })
@httpd.route("/<path:path>")
def catch_all(path):
    logger.info("not implemented route: %s", path)
    return "", 200

if __name__ == "__main__":
    httpd.run(debug=True)
