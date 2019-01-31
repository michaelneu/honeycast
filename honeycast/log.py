import logging
import sys

def apply_logger_config(logger):
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt="%(asctime)s [%(levelname)s]\t%(message)s")
    handlers = [
        logging.StreamHandler(stream=sys.stdout),
    ]

    logger.handlers.clear()

    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)

def get_logger(name):
    logger = logging.getLogger(name)
    apply_logger_config(logger)
    return logger

logger = get_logger(__name__)
