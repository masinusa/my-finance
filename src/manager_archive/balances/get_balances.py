import requests
import sys
import json

from flask import current_app

# Add base container path
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from lib.mongo import mongo

def get_balances(month_offset: int = 0) -> list:
  """ Returns a given month's last recorded balances

  Produces: 
    balances: tuple[dict], [{institution: str, balance: int, last_updated: str},
                           {institution: str, balance: int, last_updated: str},
                           {...}, ...
                          ]
  """

  # Request Information from Mongo DB
  params = {"month_offset": month_offset}
  current_app.logger.info(f"month_offset: {month_offset}")
  db_balances = requests.get("http://db_connector:5000/database/balances", params=params)
  # Parse result for each account in the database
  current_app.logger.info(f"Response code from db_connector: {db_balances.status_code}")
  if db_balances.status_code == 200:
     current_app.logger.info(f"Response: {db_balances.json()}")
  balances = []
  current_app.logger.info(f"Retrieved balances: {db_balances.json()}")
  for account in db_balances.json():
      account_balance = account['balance']
      institution = account['institution']
      last_updated = account['last_updated']
      account_name = account['account']
      subtype = account['subtype']

      if subtype in ['student', 'credit card']:
         account_balance = -1 * account_balance
 

      balances.append({'institution': institution,
                       'account': account_name,
                       'subtype': subtype,
                       'balance': round(account_balance, 2).__str__(),
                       'last_updated': last_updated})
  return json.dumps(balances)