import sys

from datetime import datetime
import logging

sys.path.append('/finapp/')
from lib import utils

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler=logging.FileHandler("/finapp/logs/plaid_api_processing.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger = logger



def squeeze_transaction(account, transaction: dict) -> dict:
  # https://www.programiz.com/python-programming/datetime/strptime
  # example: 'Fri, 28 Apr 2023 00:00:00 GMT'

  # date_given = transaction["authorized_datetime"]
  # logger.debug(str(type(date_time)))
  # logger.debug(str(date_time))
  # if date_given is None:
  #   date_given = transaction['authorized_date']
  date_given = transaction["authorized_datetime"] or transaction['authorized_date']
  if date_given:
    date_time = datetime.strptime(date_given, "%a, %d %b %Y %H:%M:%S %Z")
    # logger.debug('no datetime authorized given:')
    # logger.debug(str(type(date_time)))
    # logger.debug(str(date_time))
    timestamp = utils.time_.datetime_to_timestamp(date_time)
  else:
    timestamp = None
  return {"_id": transaction["transaction_id"],
          "date_authorized": timestamp,
          "account": account,
          "name": transaction["name"],
          "amount": transaction["amount"],
          "category": "N/A"}

