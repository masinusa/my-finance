import os
import sys
from pathlib import Path
import logging
import json

import flask
from flask import Flask, render_template, jsonify, request, Response
import requests
import configparser
import pymongo
import plaid
from plaid.api import plaid_api
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

base_container_path = str(Path(os.path.abspath(__file__)).parents[1]).replace('\\', '/')
if base_container_path not in sys.path:
    sys.path.append(base_container_path)

sys.path.append('/finapp/')
import plaid_lib
import plaid_utils
from plaid_api import logging_utils
import lib.mongo.mongo as mongo
from lib.utils import time_

# +---------------+
# | Initialize App      |
# +---------------+------------------------------------------------------------

def create_app() -> Flask:
    app = Flask(__name__)

    # Setup logger
    logger = logging_utils.get_logger('app')
    app.logger = logger

    # Get Public Token 
    collection = mongo.client.plaidDB.userTokens
    query = collection.find_one({"link_token": {"$exists": "true"}})
    if query is None:
        token = plaid_lib.create_link_token()['link_token']
        collection.insert_one({"link_token": token})
    else:
        token = query['link_token']
    app.token = token

    return app

app = create_app()


# +-----------------+-------------------------------------------------
# | Flask Routes    |
# +-----------------+ 

@app.before_request 
def before_request_callback(): 
    app.logger.info(f"Recieved {request.method}: {request.url}")

@app.after_request 
def after_request_callback( response ): 
    app.logger.info(f"Completed {request.method}: {request.url}")
    return response 

@app.errorhandler(Exception)
def handle_exception(e):
    # log the exception
    app.logger.exception('Exception occurred')
    app.logger.exception(e)
    # return a custom error page or message
    return "Error Occured"

@app.route('/')
def exists() -> Response:
    return 'Plaid API Container is Running'

@app.route('/test')
def test() -> Response:
    at = mongo.get_access_token('platypus')
    response = plaid_lib.item(at)
    return response

@app.route('/plaid_link', methods=['GET'])
def plaid_link():
    collection = mongo.client.plaidDB.bankTokens
    accessible_banks = []
    # for doc in collection.find({"working": True}):
    #     accessible_banks.append(doc['bank_name'])
    inaccessible_banks = []
    # for doc in collection.find({"working": False}):
    #     inaccessible_banks.append(doc['bank_name'])
    return render_template('index.html', token = app.token, acc_banks=accessible_banks, inacc_banks=inaccessible_banks)

# +-----------------------+
# |       |
# +---------------+------------------------------------------------------------

@app.route('/link_token', methods=['GET', 'POST'])
def token_api():
    # GET request
    if request.method == 'GET':
        message = {'token': app.token}
        return jsonify(message)  # serialize and use JSON headers
    # POST request
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return 'Sucesss', 200

# +-----------------------+
# | Plaid API ROUTES    |
# +---------------+------------------------------------------------------------
# Checks whether or not the user has an access token for a financial institution
# TODO
@app.route('/is_user_connected', methods=['GET'])
def is_user_connected():
    return jsonify({'status': False})

@app.route('/connect', methods=['GET'])
def connect():
    return render_template('connect.html')

@app.route('/oauth-return', methods=['GET'])
def oauth_return():
    return render_template('oauth-return.html')

@app.route('/create_link_token', methods=['GET', 'POST'])
def create_link_token(): return plaid_lib.create_link_token()

@app.route('/api/exchange_public_token', methods=['GET', 'POST'])
def exchange_public_token():
    app.logger.debug("Exchanging public token")
    public_token = request.get_json()['public_token']
    response = plaid_lib.get_access_token(public_token)
    access_token = response['access_token']
    bank_name = plaid_lib.item(access_token)['institution']['name']
    req_json = {"item": bank_name, 'access_token': access_token}
    app.logger.info(f"Saving access token: {bank_name}:{access_token}")
    response = requests.post("http://db_connector:5000/database/access_tokens/", json=req_json)
    assert response.ok
    return response

@app.route('/api/get_balance', methods=['GET'])
def get_balance():
    """ Return balance of given access token 
    Produces: 
        balance: dict, {institution: str,
                        accounts: [{account_name:str , balance: int, subtype: str},
                                    {account_name:str , balance: int, subtype: str},
                                    ...]
  """
    app.logger.info(f"GET /api/get_balance")

    # Request access token's associated institution
    access_token = request.args.get('access_token')
    bank_name = plaid_lib.item(access_token)['institution']['name']

    # Request institution's balance
    try:
        response = plaid_lib.get_balance(access_token)
        app.logger.debug("no error found, received request")
    except Exception as e:
        app.logger.exception("Error found in api/get_balance")
        return f"Error occured: {e}", 400
    
    # Parse results
    result = {'institution': bank_name, 'accounts': []}
    # Add every account's balance
    for accounts in response.get_json()['accounts']:
        account_balance = accounts['balances']['current']
        account_name = accounts['official_name']
        account_subtype = accounts['subtype']
        result['accounts'].append({'account': account_name,
                                   'balance': account_balance,
                                   'subtype': account_subtype})
        
    app.logger.debug(f"Returning: {result}")
    return jsonify(result)

@app.route('/api/transactions', methods=['GET'])
def latest_transactions():
    """
    Params: 
        access_token, URL param str
        transaction_cursor, URL param str
    """
    access_token = request.args.get('access_token')
    inst_name = plaid_lib.item(access_token)['institution']['name']
    cursor = request.args.get('transactions_cursor')
    if cursor:
        cursor = request.args.get('transactions_cursor')
        app.logger.debug(f"Attempting with Given Cursor: {cursor}")
        new_cursor, transactions = plaid_lib.latest_transactions(cursor=cursor, access_token=access_token)
    else: 
        app.logger.debug(f"No Transactions Cursor Recieved for: {inst_name}")
        new_cursor, transactions = plaid_lib.latest_transactions(access_token=access_token)
    
 
    # cursor = mongo.get_transaction_cursor(inst_name)
    stransactions = [] # Squeezed Transactions
    for transact in transactions.get_json()['latest_transactions']:
        squeezed_transaction = plaid_utils.squeeze_transaction(inst_name, transact)
        stransactions.append(squeezed_transaction)
        # mongo.set_transaction(squeezed_transaction)
    
    # mongo.set_transaction_cursor(bank_name, cursor)
    return jsonify(new_cursor, stransactions)
    return f"Updated {count} Transactions"

if __name__ == "__main__":
    app.run(debug=True)