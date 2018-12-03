import logging
import logging.handlers
from flask import request
from flask.logging import default_handler

from settings import LOG_LEVEL


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        record.full_path = request.full_path.rstrip('?')
        record.method = request.method
        return super(RequestFormatter, self).format(record)


def init_logging(app, log_file):
    formatter = RequestFormatter(
        '[%(asctime)s][%(name)s][%(levelname)s]: %(remote_addr)s - "%(method)s %(full_path)s" - %(message)s'
    )
    fh = logging.handlers.TimedRotatingFileHandler(filename=log_file, when='MIDNIGHT', backupCount=7, utc=True)
    fh.setFormatter(formatter)
    app.logger.addHandler(fh)
    app.logger.setLevel(set_log_level(LOG_LEVEL))
    # default_handler.setFormatter(formatter)
    app.logger.removeHandler(default_handler)


def set_log_level(level):
    switcher = {
        "ERROR": logging.ERROR,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "WARNING": logging.WARNING,
        "CRITICAL": logging.CRITICAL
    }
    return switcher.get(level.upper(), "Invalid LOG LEVEL")
