import requests
import sys
import json

# Add base container path
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from lib.mongo import mongo
from flask import jsonify, current_app


def update_balances(month_offset: int = 0):
  current_app.logger.info("Updating Balances")
  resp_status = {'status': 200, 'institutions':[]}

  # Get Existing Institutions
  a_tokens = mongo.get_access_tokens()

  # Get associated balance for each
  for institution in a_tokens:
      a_t = institution['access_token']
      if institution['working']:
        # Request Institution's Balance
        inst_token_status = {'institution': institution['institution'], 'code': 200}
        try:
            # logger.info(f"requesting balance for {a_t['bank_name']}")
            resp = requests.get('http://plaid:5000/api/get_balance', params={"access_token":a_t}, timeout=10)
            response = resp.json()
            resp_status['institutions'].append(inst_token_status)
        except Exception as e:
            resp_status['status'] = 500
            current_app.logger.exception(f"Failed to retrieve {institution['institution']}'s balance: {e.__class__.__name__}, {str(e)}")
            inst_token_status.update({'code': 500,
                                'error_name': e.__class__.__name__,
                                'error_message': str(e)})
            resp_status['institutions'].append(inst_token_status)


      # Update database with every account in the institution's balance
      # TODO: provide error checking and response code for upserting into database
        if inst_token_status != 200:
          try:
            params = { "month_offset": month_offset }
            for account in response['accounts']:
                  data = {
                    'institution': response['institution'],
                    'balance': account['balance'],
                    'account': account['account'],
                    'subtype': account['subtype'] 
                  }  
                  response = requests.put("http://db_connector:5000/database/balances/update", params=params, json=json.dumps(data))

          except Exception as e:
            current_app.logger.exception(f"Failed to retrieve {institution['institution']}'s balance: {e.__class__.__name__}")
      return jsonify(resp_status)
      