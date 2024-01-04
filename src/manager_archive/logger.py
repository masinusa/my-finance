import logging

# Setup logger
logger = logging.getLogger('manager')
logger.setLevel(logging.DEBUG)
handler=logging.FileHandler("/finapp/logs/manager.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger = logger

