import os
import sys
from pathlib import Path
import logging
import json

from flask import Flask, render_template, jsonify, request, Response
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
import lib.mongo.mongo as mongo

# +---------------+
# | Initialize App      |
# +---------------+------------------------------------------------------------

def create_app() -> Flask:
    app = Flask(__name__)

    # Setup logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler=logging.FileHandler("/finapp/logs/plaid_api_processing.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
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

    # Update Bank Tokens
    collection = mongo.client.plaidDB.bankTokens
    banks = collection.find({"bank_name": {"$exists": "true"}})

    def check_working(access_t):
        PLAID_CLIENT_ID = '62edf4d4f8e7e40013eb8749'
        PLAID_SECRET = '4c45a3df6d7d8c6b5b72ee524f43f4'

        # host = plaid.Environment.Development
        host = plaid.Environment.Sandbox
        configuration = plaid.Configuration(
            host=host,
            api_key={
                'clientId': PLAID_CLIENT_ID,
                'secret': PLAID_SECRET,
                'plaidVersion': '2020-09-14'
            }
        )
        api_client = plaid.ApiClient(configuration)
        app.plaid_client = plaid_api.PlaidApi(api_client)
        request = AccountsBalanceGetRequest(
            access_token=access_t
        )
        response = app.plaid_client.accounts_balance_get(request)
        return True
    # for bank in banks:
    #     if not check_working(bank['access_token']):
    #         collection.update_one({'_id':bank['_id']}, {"$set": {"working": False} }, upsert=True)
        

    return app

app = create_app()


# +-----------------+-------------------------------------------------
# | Flask Routes    |
# +-----------------+ 

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
    for doc in collection.find({"working": True}):
        accessible_banks.append(doc['bank_name'])
    inaccessible_banks = []
    for doc in collection.find({"working": False}):
        inaccessible_banks.append(doc['bank_name'])
    return render_template('index.html', token = app.token, acc_banks=accessible_banks, inacc_banks=inaccessible_banks)



# +-----------------------+
# | GUI ROUTES      |
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
    public_token = request.get_json()['public_token']
    response = plaid_lib.get_access_token(public_token)
    access_token = response['access_token']
    bank_name = plaid_lib.item(access_token)['institution']['name']
    mongo.set_access_token(access_token=access_token, bank_name=bank_name)
    return response


@app.route('/api/get_balance', methods=['GET'])
def get_balance():
    app.logger.info("GET /api/exchange_public_token")
    access_token = request.args.get('access_token')
    bank_name = plaid_lib.item(access_token)['institution']['name']
    response = plaid_lib.get_balance(access_token)
    for accounts in response.get_json()['accounts']:
          balance = accounts['balances']['current']
          institution = f"{bank_name} - {accounts['name']}"
          app.logger.info(f"saving {institution} balance")
          mongo.set_institution_balance(
                institution,
                balance)
    return response


@app.route('/api/get_transactions', methods=['GET'])
def get_transactions():
    app.logger.info("GET /api/get_transactions")
    access_token = request.args.get('access_token')

    bank_name = plaid_lib.item(access_token)['institution']['name']
    cursor = mongo.get_transaction_cursor(bank_name)
    cursor, transactions = plaid_lib.get_transactions(bank_name=bank_name, 
                                              cursor=cursor, 
                                              access_token=access_token)
    app.logger.debug(f"{type(transactions.get_json()['latest_transactions'])}")
    app.logger.debug(f"{str(transactions.get_json()['latest_transactions'])}")

    count = 0
    for transact in transactions.get_json()['latest_transactions']:
        squeezed_transaction = plaid_utils.squeeze_transaction(bank_name, transact)
        app.logger.debug(str(squeezed_transaction))
        mongo.set_transaction(squeezed_transaction, month_offset=0)
        count += 1
    
    mongo.set_transaction_cursor(bank_name, cursor)
    return f"Updated {count} Transactions"


if __name__ == "__main__":
    app.run(debug=True)