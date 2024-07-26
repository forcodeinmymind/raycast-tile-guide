import logging
import os


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# main_log = setup_logger('main_log', 'main.log', logging.DEBUG)


logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w", \
                    format="%(asctime)s - %(levelname)s - %(message)s")