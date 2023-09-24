# source https://github.com/plaid/quickstart/blob/master/python/server.py#L243

from plaid.exceptions import ApiException
from plaid.model.payment_amount import PaymentAmount
from plaid.model.payment_amount_currency import PaymentAmountCurrency
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.recipient_bacs_nullable import RecipientBACSNullable
from plaid.model.payment_initiation_address import PaymentInitiationAddress
from plaid.model.payment_initiation_recipient_create_request import PaymentInitiationRecipientCreateRequest
from plaid.model.payment_initiation_payment_create_request import PaymentInitiationPaymentCreateRequest
from plaid.model.payment_initiation_payment_get_request import PaymentInitiationPaymentGetRequest
from plaid.model.link_token_create_request_payment_initiation import LinkTokenCreateRequestPaymentInitiation
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.asset_report_create_request import AssetReportCreateRequest
from plaid.model.asset_report_create_request_options import AssetReportCreateRequestOptions
from plaid.model.asset_report_user import AssetReportUser
from plaid.model.asset_report_get_request import AssetReportGetRequest
from plaid.model.asset_report_pdf_get_request import AssetReportPDFGetRequest
from plaid.model.auth_get_request import AuthGetRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.identity_get_request import IdentityGetRequest
from plaid.model.investments_transactions_get_request_options import InvestmentsTransactionsGetRequestOptions
from plaid.model.investments_transactions_get_request import InvestmentsTransactionsGetRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
from plaid.model.item_get_request import ItemGetRequest
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
from plaid.model.transfer_authorization_create_request import TransferAuthorizationCreateRequest
from plaid.model.transfer_create_request import TransferCreateRequest
from plaid.model.transfer_get_request import TransferGetRequest
from plaid.model.transfer_network import TransferNetwork
from plaid.model.transfer_type import TransferType
from plaid.model.transfer_user_in_request import TransferUserInRequest
from plaid.model.ach_class import ACHClass
from plaid.model.transfer_create_idempotency_key import TransferCreateIdempotencyKey
from plaid.model.transfer_user_address_in_request import TransferUserAddressInRequest
from plaid.api import plaid_api
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import Blueprint
from datetime import datetime
from datetime import timedelta
import plaid
import base64
import os
import datetime
import json
import logging
import time
from dotenv import load_dotenv
from werkzeug.wrappers import response

load_dotenv()

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler=logging.FileHandler("/finapp/logs/plaid_api_processing.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# +---------------+
# | Helpers       |
# +---------------+------------------------------------------------------------
def empty_to_none(field):
    value = os.getenv(field)
    if value is None or len(value) == 0:
        return None
    return value

def pretty_print_response(response):
  print(json.dumps(response, indent=2, sort_keys=True, default=str))



def format_error(e):
    response = json.loads(e.body)
    return {'error': {'status_code': e.status, 'display_message':
                      response['error_message'], 'error_code': response['error_code'], 'error_type': response['error_type']}}



# +------------------------+
# | Environment Setup      |
# +----------------------------------------------------------------------------
PLAID_ENV = os.getenv('PLAID_ENV')
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_PRODUCTS = os.getenv('PLAID_PRODUCTS').split(',')
PLAID_REDIRECT_URI = empty_to_none('PLAID_REDIRECT_URI')
PLAID_COUNTRY_CODES = os.getenv('PLAID_COUNTRY_CODES').split(',')



host = plaid.Environment.Sandbox

if PLAID_ENV == 'sandbox':
    host = plaid.Environment.Sandbox

if PLAID_ENV == 'development':
    host = plaid.Environment.Development

if PLAID_ENV == 'production':
    host = plaid.Environment.Production


configuration = plaid.Configuration(
    host=host,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
        'plaidVersion': '2020-09-14'
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

products = []
for product in PLAID_PRODUCTS:
    products.append(Products(product))
logger.debug(f"Products: {str(products)}")



# We store the access_token in memory - in production, store it in a secure
# persistent data store.
access_token = None
# The payment_id is only relevant for the UK Payment Initiation product.
# We store the payment_id in memory - in production, store it in a secure
# persistent data store.
payment_id = None
# The transfer_id is only relevant for Transfer ACH product.
# We store the transfer_id in memomory - in produciton, store it in a secure
# persistent data store
transfer_id = None

item_id = None



# +------------------------+
# | Plaid functions      |
# +----------------------------------------------------------------------------

# @plaid_link.route('/api/create_link_token', methods=['POST'])
def create_link_token():
    try:
        logger.debug(f"Products (type/value): {str(type(products))}/{str(products)}")
        request = LinkTokenCreateRequest(
            products=products,
            client_name="Plaid Quickstart",
            country_codes=list(map(lambda x: CountryCode(x), PLAID_COUNTRY_CODES)),
            language='en',
            user=LinkTokenCreateRequestUser(
                client_user_id=str(time.time())
            )
        )
        if PLAID_REDIRECT_URI!=None:
            request['redirect_uri']=PLAID_REDIRECT_URI
    # create link token
        response = client.link_token_create(request)
        return response.to_dict()
        # return jsonify(response.to_dict())
    except plaid.ApiException as e:
        return json.loads(e.body)


# Exchange token flow - exchange a Link public_token for
# an API access_token
# https://plaid.com/docs/#exchange-token-flow


# @plaid_link.route('/api/set_access_token', methods=['POST'])
def get_access_token(public_token):
    global access_token
    global item_id
    global transfer_id
    try:
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=public_token)
        exchange_response = client.item_public_token_exchange(exchange_request)
        access_token = exchange_response['access_token']
        item_id = exchange_response['item_id']
        if 'transfer' in PLAID_PRODUCTS:
            transfer_id = authorize_and_create_transfer(access_token)
        return exchange_response.to_dict()
        # return jsonify(exchange_response.to_dict())
    except plaid.ApiException as e:
        return json.loads(e.body)


# Retrieve ACH or ETF account numbers for an Item
# https://plaid.com/docs/#auth


# @plaid_link.route('/api/auth', methods=['GET'])
def get_auth(access_token):
    try:
       request = AuthGetRequest(
            access_token=access_token
        )
       response = client.auth_get(request)
       pretty_print_response(response.to_dict())
       return jsonify(response.to_dict())
    except plaid.ApiException as e:
        error_response = format_error(e)
        return jsonify(error_response)


# Retrieve Transactions for an Item
# https://plaid.com/docs/#transactions


# @plaid_link.route('/api/transactions', methods=['GET'])
def get_transactions(bank_name, access_token, cursor:str = ''):

    # New transaction updates since "cursor"
    added = []
    modified = []
    removed = [] # Removed transaction ids
    has_more = True
    try:
        # Iterate through each page of new transaction updates for item
        while has_more:
            request = TransactionsSyncRequest(
                access_token=access_token,
                cursor=cursor,
                count=500
            )
            response = client.transactions_sync(request).to_dict()
            # Add this page of results
            added.extend(response['added'])
            modified.extend(response['modified'])
            removed.extend(response['removed'])
            has_more = response['has_more']
            # Update cursor to the next cursor
            cursor = response['next_cursor']
            pretty_print_response(response)

        # Return the 8 most recent transactions
        #TODO DON'T LIMIT TO 8
        latest_transactions = sorted(added, key=lambda t: t['date'])
        return cursor, jsonify({
            'latest_transactions': latest_transactions})

    except plaid.ApiException as e:
        error_response = format_error(e)
        return jsonify(error_response)


# Retrieve Identity data for an Item
# https://plaid.com/docs/#identity


# @plaid_link.route('/api/identity', methods=['GET'])
def get_identity(access_token):
    try:
        request = IdentityGetRequest(
            access_token=access_token
        )
        response = client.identity_get(request)
        pretty_print_response(response.to_dict())
        return jsonify(
            {'error': None, 'identity': response.to_dict()['accounts']})
    except plaid.ApiException as e:
        error_response = format_error(e)
        return jsonify(error_response)


# Retrieve real-time balance data for each of an Item's accounts
# https://plaid.com/docs/#balance


# @plaid_link.route('/api/balance', methods=['GET'])
def get_balance(access_token):
    try:
        logger.info(f"getting balance with access_token: {access_token}")
        request = AccountsBalanceGetRequest(
            access_token=access_token
        )
        response = client.accounts_balance_get(request)
        logger.debug("no errors in plaid_lib.get_balance()")
        pretty_print_response(response.to_dict())
        return jsonify(response.to_dict())
    except plaid.ApiException as e:
        logger.debug("error found in plaid_lib.get_balance()")
        error_response = format_error(e)
        raise error_response


# Retrieve an Item's accounts
# https://plaid.com/docs/#accounts


# @plaid_link.route('/api/accounts', methods=['GET'])
def get_accounts():
    try:
        request = AccountsGetRequest(
            access_token=access_token
        )
        response = client.accounts_get(request)
        pretty_print_response(response.to_dict())
        return jsonify(response.to_dict())
    except plaid.ApiException as e:
        error_response = format_error(e)
        return jsonify(error_response)


# Retrieve high-level information about an Item
# https://plaid.com/docs/#retrieve-item


# @plaid_link.route('/api/item', methods=['GET'])
def item(access_token):
    try:
        request = ItemGetRequest(access_token=access_token)
        response = client.item_get(request)
        request = InstitutionsGetByIdRequest(
            institution_id=response['item']['institution_id'],
            country_codes=list(map(lambda x: CountryCode(x), PLAID_COUNTRY_CODES))
        )
        institution_response = client.institutions_get_by_id(request)
        pretty_print_response(response.to_dict())
        pretty_print_response(institution_response.to_dict())
        return {'error': None, 
                'item': response.to_dict()['item'], 
                'institution': institution_response.to_dict()['institution']}
    except plaid.ApiException as e:
        error_response = format_error(e)
        return jsonify(error_response)

if __name__ == '__main__':
    pass