# import sys
# import os 
# from pathlib import Path
# import requests
# import json

# from flask import Blueprint, request, current_app, jsonify

# from .BalanceODM import BalanceODM

# # Create Flask Blueprint
# balances_blueprint = Blueprint('balances_blueprint', __name__)

# @balances_blueprint.route('/balances/<int:month_offset>', methods=['GET'])
# def get_monthly_balances(month_offset):
#     """  Gives a month's last recorded total balances. 
    
#     See get_balances()
#     """

#     """ Returns a given month's last recorded balances

#     Produces: 
#         balances: tuple[dict], [{institution: str, balance: int, last_updated: str},
#                             {institution: str, balance: int, last_updated: str},
#                             {...}, ...
#                             ]
#     """

#     # Request Information from Mongo DB
#     params = {"month_offset": month_offset}
#     current_app.logger.info(f"month_offset: {month_offset}")
#     db_balances = requests.get("http://db_connector:5000/database/balances", params=params)
#     # Parse result for each account in the database
#     current_app.logger.info(f"Response code from db_connector: {db_balances.status_code}")
#     if db_balances.status_code == 200:
#         current_app.logger.info(f"Response: {db_balances.json()}")
#     balances = []
#     current_app.logger.info(f"Retrieved balances: {db_balances.json()}")
#     for account in db_balances.json():
#         account_balance = account['balance']
#         institution = account['institution']
#         last_updated = account['last_updated']
#         account_name = account['account']
#         subtype = account['subtype']

#         if subtype in ['student', 'credit card']:
#             account_balance = -1 * account_balance
    

#         balances.append({'institution': institution,
#                         'account': account_name,
#                         'subtype': subtype,
#                         'balance': round(account_balance, 2).__str__(),
#                         'last_updated': last_updated})
#     return json.dumps(balances)

# @balances_blueprint.route('/balances/<int:month_offset>', methods=['PUT'])
# def update_monthly_balances(month_offset):
#     current_app.logger.info("Updating Balances")

#     # Initialize Response Status
#     update_status = {'status': 200, 'institutions':[]}

#     # Get Existing Item/Institution Access Tokens
#     current_app.logger.info(f"Getting access tokens")
#     a_tokens = requests.get('http://db_connector:5000/database/access_tokens')

#     # Check if any Access Tokens Exist in Database, exit if not
#     try: current_app.logger.info(f"Got access tokens:{a_tokens.json()}")
#     except Exception as e: 
#         current_app.logger.info(f"No access tokens stored")
#         return "No Access Tokens Saved"
        
#     # Get Associated Balance For Each Item/Institution
#     for item in a_tokens.json():
#         a_t = item['access_token']
#         item_update_status = {'institution': item['institution'], 'code': 200}
#         # Request Institution's Balance
#         try:
#             if item['institution'] == 'Capital One':
#                 raise Exception("Capital One Balances not supported")
#             # logger.info(f"requesting balance for {a_t['bank_name']}")
#             resp = requests.get('http://plaid:5000/api/get_balance', params={"access_token":a_t}, timeout=35)
#             current_app.logger.info(f"Requesting Item's Balance from plaid, status: {resp.status_code}")
#             if not resp.ok:
#                 raise Exception(f"Plaid API returned non-200 HTTP code for {item['institution']}")
#             response = resp.json()
#             current_app.logger.debug(f"Received type response from plaid/api/get_balance: {type(response)}")
#             current_app.logger.debug(f"Received response from plaid/api/get_balance: {response}")
#             update_status['institutions'].append(item_update_status)
#             params = { "month_offset": month_offset }
#             for account in response['accounts']:
#                     data = {
#                     'institution': response['institution'],
#                     'account': account['account'],
#                     'balance': account['balance'],
#                     'account': account['account'],
#                     'subtype': account['subtype'] 
#                     }  
#                     _ = requests.put("http://db_connector:5000/database/balances/update", params=params, json=json.dumps(data))
#                     assert(_.ok)
#         except Exception as e:
#             update_status['status'] = 500

#             current_app.logger.warning(f"Failed to retrieve {item['institution']}'s balance: {e.__class__.__name__}, {str(e)}")
#             item_update_status.update({'code': 500,
#                                 'error_name': e.__class__.__name__,
#                                 'error_message': str(e)})
#             update_status['institutions'].append(item_update_status)


#         # Update database with every account in the institution's balance
#         # TODO: provide error checking and response code for upserting into database
#     #       if inst_token_status != 200:
#     #         try:
#     #           params = { "month_offset": month_offset }
#     #           for account in response['accounts']:
#     #                 data = {
#     #                   'institution': response['institution'],
#     #                   'balance': account['balance'],
#     #                   'account': account['account'],
#     #                   'subtype': account['subtype'] 
#     #                 }  
#     #                 response = requests.put("http://db_connector:5000/database/balances/update", params=params, json=json.dumps(data))

#     #         except Exception as e:
#     #           current_app.logger.exception(f"Failed to retrieve {institution['institution']}'s balance: {e.__class__.__name__}")
#     current_app.logger.info(f"Returning: {update_status}")
#     return jsonify(update_status)

