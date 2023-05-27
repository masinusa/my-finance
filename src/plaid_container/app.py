import os
import sys
from pathlib import Path
import logging

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

import plaid_link

# +-----------------+-------------------------------------------------
# | Initialize App  |
# +-----------------+ 

def create_app() -> Flask:
    app = Flask(__name__)

    # Setup logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler=logging.FileHandler("/finapp/logs/plaid_api_processing.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    app.logger = logger

    # Initialize Mongo DB Client
    app.client = pymongo.MongoClient("mongodb://rootuser:rootpass@mongo:27017/")

    # Get Public Token 
    collection = app.client.plaidDB.userTokens
    query = collection.find_one({"link_token": {"$exists": "true"}})
    if query is None:
        token = plaid_link.create_link_token()['link_token']
        collection.insert_one({"link_token": token})
    else:
        token = query['link_token']
    app.token = token

    # Update Bank Tokens
    collection = app.client.plaidDB.bankTokens
    banks = collection.find({"bank_name": {"$exists": "true"}})

    def check_working(access_t):
        PLAID_CLIENT_ID = '62edf4d4f8e7e40013eb8749'
        PLAID_SECRET = '4c45a3df6d7d8c6b5b72ee524f43f4'

        host = plaid.Environment.Development
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
        try:
            request = AccountsBalanceGetRequest(
                access_token=access_t
            )
            response = app.plaid_client.accounts_balance_get(request)
            return True
        except plaid.ApiException as e:
            return False
    for bank in banks:
        if not check_working(bank['access_token']):
            collection.update_one({'_id':bank['_id']}, {"$set": {"working": False} }, upsert=True)
        

    return app

app = create_app()


# +-----------------+-------------------------------------------------
# | Flask Routes    |
# +-----------------+ 

@app.route('/')
def exists() -> Response:
    return 'Plaid API Container is Running'


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
    
@app.route('/exchange_public_token', methods=['POST'])
def exchange_public_token():
    global access_token
    public_token = request.form['public_token']
    request = ItemPublicTokenExchangeRequest(
      public_token=public_token
    )
    response = app.plaid_client.item_public_token_exchange(request)
    # These values should be saved to a persistent database and
    # associated with the currently signed-in user
    access_token = response['access_token']
    item_id = response['item_id']

    # Store these values in database
    app.logger.info("Entered exchange public token and storing it now")
    collection = app.client.plaidDB.bankTokens
    collection.insert_one({"access_token": access_token, "item_id": item_id})
    return jsonify({'public_token_exchange': 'complete', "access_token": access_token, "item_id": item_id})


@app.route('/plaid_link', methods=['GET'])
def plaid_link_popup():
    collection = app.client.plaidDB.bankTokens
    accessible_banks = []
    for doc in collection.find({"working": True}):
        accessible_banks.append(doc['bank_name'])
    inaccessible_banks = []
    for doc in collection.find({"working": False}):
        inaccessible_banks.append(doc['bank_name'])
    return render_template('index.html', token = app.token, acc_banks=accessible_banks, inacc_banks=inaccessible_banks)



if __name__ == "__main__":
    app.run(debug=True)