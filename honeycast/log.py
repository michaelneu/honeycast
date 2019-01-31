import logging

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt="%(asctime)s [%(levelname)s]\t%(message)s")
    handlers = [
        logging.StreamHandler(),
    ]

    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

logger = get_logger(__name__)
