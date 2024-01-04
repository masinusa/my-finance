import logging
from sys import stdout
from time import time
import os
from pathlib import Path

ROOT_LOGGER= 'plaid_api'
LOG_DIR='/finapp/logs/plaid_api'

_time_format = "%d-%m-%Y %H:%M"

Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

def get_logger(name):
    logger_name = f"{ROOT_LOGGER}.{name}"
    if logger_name in logging.Logger.manager.loggerDict.keys():
        return logging.getLogger(logger_name)
    
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)


    # Handler for 'All' logfile
    all_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', _time_format)
    all_handler = logging.FileHandler(f"{LOG_DIR}/all.log")
    all_handler.setFormatter(all_formatter)
    all_handler.setLevel(logging.INFO)
    logger.addHandler(all_handler)

    # Handler for modular file
    module_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s', _time_format)
    module_handler = logging.FileHandler(f"{LOG_DIR}/{name}.log")
    module_handler.setFormatter(module_formatter)
    logger.addHandler(module_handler)

    return logger