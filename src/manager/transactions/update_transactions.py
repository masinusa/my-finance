import requests
import sys
import json

from flask import jsonify, current_app

# Add base container path
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from lib.utils import time_

def update_transactions():
  current_app.logger.info("Updating Transactions")

  # Get Existing Item/Institution Access Tokens
  current_app.logger.info(f"Getting access tokens")
  a_tokens = requests.get('http://db_connector:5000/database/access_tokens')
  # Check if any Access Tokens Exist in Database, exit if not
  try: current_app.logger.info(f"Got access tokens:{a_tokens.json()}")
  except Exception as e: 
    current_app.logger.info(f"No access tokens stored")
    return "No Access Tokens Saved"
  a_tokens = a_tokens.json()

  # Retrieve Latest Cursor
  current_app.logger.info(f"Getting transaction cursors")
  t_cursors = requests.get("http://db_connector:5000/database/transaction_cursors/")
  try: 
    current_app.logger.info(f"Got Transaction Cursors Data:{t_cursors}, {t_cursors.json()}")
    t_cursors = [cursor['transaction_cursor'] for cursor in t_cursors.json()]
  except Exception as e: 
    current_app.logger.info(f"No transaction cursors stored: {str(e)}")
    t_cursors = []

  # Initialize Response Status
  # update_status = {'status': 200, 'institutions':[]}
  update_status = []
  for item in a_tokens:
      a_t = item['access_token']
      item_update_status = {'institution': item['institution'], 'code': 200}
      try: 
         cursor = t_cursors[item['institution']]
      except:
         cursor = ''
      params = {"access_token": a_t,
                'transaction_cursor': cursor}
      # Request Institution's Balance
      try:
          # logger.info(f"requesting balance for {a_t['bank_name']}")
          resp = requests.get('http://plaid:5000/api/transactions', params=params, timeout=20)
          current_app.logger.info(f"Requesting transactions from plaid, status: {resp.status_code}")
          if not resp.ok:
              raise Exception(f"Plaid API returned non-200 HTTP code for {item['institution']}")
          new_cursor, transactions = resp.json()
          current_app.logger.debug(f"Received type response from plaid/api/transactions: {type(transactions)}")
          current_app.logger.debug(f"Received response from plaid/api/transactions: {transactions}")
          update_status.append(item_update_status)

          current_app.logger.debug("Assigning each transaction a month and storing it in the database")
          for t in transactions:
                current_app.logger.debug(f"t: {t}")
                month_offset = time_.month_offset(t['date_authorized'])
                params = { "month_offset": month_offset }
                _ = requests.put("http://db_connector:5000/database/transactions", params=params, json=json.dumps([t]))
                assert(_.ok)
      except Exception as e:
          current_app.logger.warning(f"Error while retrieving {item['institution']}'s transactions: {e.__class__.__name__}, {str(e)}")
          item_update_status.update({'code': 500,
                              'error_name': e.__class__.__name__,
                              'error_message': str(e)})
          update_status.append(item_update_status)


      # Update database with every account in the institution's balance
      # TODO: provide error checking and response code for upserting into database
  #       if inst_token_status != 200:
  #         try:
  #           params = { "month_offset": month_offset }
  #           for account in response['accounts']:
  #                 data = {
  #                   'institution': response['institution'],
  #                   'balance': account['balance'],
  #                   'account': account['account'],
  #                   'subtype': account['subtype'] 
  #                 }  
  #                 response = requests.put("http://db_connector:5000/database/balances/update", params=params, json=json.dumps(data))

  #         except Exception as e:
  #           current_app.logger.exception(f"Failed to retrieve {institution['institution']}'s balance: {e.__class__.__name__}")
  current_app.logger.info(f"Returning: {update_status}")
  return jsonify({"status": update_status})
      