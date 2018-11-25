import logging
import logging.handlers

from settings import LOG_LEVEL


def set_log_level(level):
    switcher = {
        "ERROR": logging.ERROR,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "WARNING": logging.WARNING,
        "CRITICAL": logging.CRITICAL
    }
    return switcher.get(level.upper(), "Invalid LOG LEVEL")


def init_logging(app, log_file):
    formatter = logging.Formatter(f'[%(asctime)s][%(name)s][%(levelname)s]: %(message)s')

    fh = logging.handlers.TimedRotatingFileHandler(filename=log_file, when='MIDNIGHT', backupCount=7, utc=True)
    fh.setFormatter(formatter)

    app.logger.addHandler(fh)
    app.logger.setLevel(set_log_level(LOG_LEVEL))
