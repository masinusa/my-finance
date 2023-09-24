import logging

def setup_logger(name, file_name):
    logger = logging.getLogger(name)
    if sum([isinstance(handler, logging.FileHandler) for handler in logger.handlers]):
        logger.setLevel(logging.DEBUG)
        handler=logging.FileHandler(f"/finapp/logs/{file_name}.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


