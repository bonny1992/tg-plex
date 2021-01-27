import sys
import logging

def set_logger(name = __name__, level = 'INFO'):

    format = logging.Formatter("%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s")
    logger = logging.getLogger(name)

    if level == 'INFO':
        level = logging.INFO
    elif level == 'WARNING':
        level = logging.WARNING
    elif level == 'ERROR':
        level = logging.ERROR
    elif level == 'DEBUG':
        level = logging.DEBUG
    elif level == 'CRITICAL':
        level = logging.CRITICAL

    logger.setLevel(level)
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(format)

    logger.addHandler(ch)

    return logger