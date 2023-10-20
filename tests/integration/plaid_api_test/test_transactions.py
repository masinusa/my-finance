import requests
import pytest
import sys
import os 
from pathlib import Path
import datetime
import json

base_container_path = str(Path(os.path.abspath(__file__)).parents[1]).replace('\\', '/')
if base_container_path not in sys.path:
    sys.path.append(base_container_path)
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from lib.utils.time_ import datetime_to_month_offset

"""
  return {"_id": transaction["transaction_id"],
          "date_authorized": timestamp,
          "account": account,
          "name": transaction["name"],
          "amount": transaction["amount"],
          "category": "N/A"}
"""

def test_latest_transactions():
    """ Test Mongo Database Balances retrieval """
    params = {'access_token': 'access-sandbox-605ef917-d2a1-4dc1-b310-d59cc03d8425'}
    response = requests.get("http://plaid:5000/api/transactions", params=params)
    cursor, transactions = response.json()
    print(response.json())
    assert cursor == 'CAESJW5QUmpqNUc0NVhoNUx6cEFNUDZNaXdReEVxeXk2OUMzUXd5dkIaDAiRubmpBhDI+9PIAyIMCJG5uakGEMj708gDKgwIkbm5qQYQyPvTyAM='
    assert type(transactions) == list
    assert type(transactions[0]) == dict
    assert transactions[0] == {'_id': 'dKMrrwkgwlfy4xBeLGwZCQaQnQk5vPhDPzJDo', 'account': 'Chase', 'amount': 12.0, 'category': 'N/A', 'date_authorized': '2021-10-04', 'name': "McDonald's"}, {'_id': 'aA6lle8keEunxzG4bQJ6UMbMnM3jpWC1RJZ1R', 'account': 'Chase', 'amount': 4.33, 'category': 'N/A', 'date_authorized': '2021-10-04', 'name': 'Starbucks'}
    assert response.ok

# def test_set_transactions():
#     """ Test Mongo Database access_token posting """
#     June_2023_offset = datetime_to_month_offset(datetime.date(2023, 6, 23))
#     params = { "month_offset": June_2023_offset }
#     req_json = {'transactions': {"_id": "01"",
#           "date_authorized": "99/99/9999",
#           "account": "account_name",
#           "name": transaction["name"],
#           "amount": transaction["amount"],
#           "category": "N/A"}}
#     response = requests.post("http://db_connector:5000/database/access_tokens/", params=params, json=req_json)
#     assert response.ok

#     response = requests.get("http://db_connector:5000/database/access_tokens/")
#     assert response.ok
#     resp_json = response.json()
#     print(resp_json)
#     for item in resp_json:
#         print("Item values")
#         print(item.values())
#         if 'Chase' in item.values():
#             assert item['access_token'] == 'access-sandbox-605ef917-d2a1-4dc1-b310-d59cc03d8425'
#             return 
#     assert False

# @app.route('/api/get_transactions', methods=['GET'])
# def get_transactions():
#     app.logger.info("GET /api/get_transactions")
#     access_token = request.args.get('access_token')

#     bank_name = plaid_lib.item(access_token)['institution']['name']
#     cursor = mongo.get_transaction_cursor(bank_name)
#     cursor, transactions = plaid_lib.get_transactions(bank_name=bank_name, 
#                                               cursor=cursor, 
#                                               access_token=access_token)
#     count = 0 # to return how many transactions got updated
#     for transact in transactions.get_json()['latest_transactions']:
#         squeezed_transaction = plaid_utils.squeeze_transaction(bank_name, transact)

#         mongo.set_transaction(squeezed_transaction)
#         count += 1
    
#     mongo.set_transaction_cursor(bank_name, cursor)
#     return f"Updated {count} Transactions"