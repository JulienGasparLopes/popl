import logging
import sys


def get_logger(module_name: str, level: int = "INFO") -> logging.Logger:
    logger = logging.getLogger(module_name)
    logger.setLevel(level)
    handler = logging.StreamHandler(stream=sys.stdout)
    logger.addHandler(handler)

    return logger
