import logging

# Setup logger
logger = logging.getLogger('db_connector')
logger.setLevel(logging.DEBUG)
handler=logging.FileHandler("/finapp/logs/db_connector.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger = logger

