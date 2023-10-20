import requests
import sys
import json

from flask import current_app


def get_transactions(month_offset: int = 0) -> list:
  """ Returns a given month's transactions

  Produces: 
    transactions: ...
  """

  # Request Information from Mongo DB
  params = {"month_offset": month_offset}
  current_app.logger.info(f"month_offset: {month_offset}")
  transactions = requests.get("http://db_connector:5000/database/transactions", params=params)
  # Parse result for each account in the database
  current_app.logger.info(f"Response code from db_connector: {transactions.status_code}")
  return json.dumps(transactions.json())
  # transactions = []
  # for account in db_balances.json():
  #     account_balance = account['balance']
  #     institution = account['institution']
  #     last_updated = account['last_updated']
 

  #     transactions.append({'institution': institution,
  #                       'balance': round(account_balance, 2).__str__(),
  #                       'last_updated': last_updated})
  # return json.dumps(balances)