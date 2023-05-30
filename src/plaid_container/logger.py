import logging

# Setup logger
logger = logging.getLogger('plaid_container')
logger.setLevel(logging.DEBUG)
handler=logging.FileHandler("/finapp/logs/plaid_api_processing.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger = logger

