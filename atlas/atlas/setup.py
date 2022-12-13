import logging
import os

def start_logger(loglevel: str = logging.INFO) -> object:
    logger = logging.getLogger("main")
    logger.setLevel(loglevel)
    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(threadName)s:%(lineno)d - %(funcName)s() - %(levelname)s - %(message)s'))
    logger.addHandler(ch)
    return logger