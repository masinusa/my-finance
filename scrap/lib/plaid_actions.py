
from dotenv import load_dotenv

from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
import plaid
from plaid.api import plaid_api
from plaid.model.transactions_sync_request import TransactionsSyncRequest

import utils
from . import secrets

import streamlit as st
st.write(secrets.__dict__.keys())

# +--------------+
# | Plaid Config |
# +-------------+-------------------------------------------------------------
PLAID_CLIENT_ID = secrets.PLAID_CLIENT_ID
PLAID_SECRET = secrets.PLAID_SECRET

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
client = plaid_api.PlaidApi(api_client)


def get_balance(access_t):
    try:
        request = AccountsBalanceGetRequest(
            access_token=access_t
        )
        response = client.accounts_balance_get(request)
        # utils.pretty_print_response(response.to_dict())
        return response.to_dict()
    except plaid.ApiException as e:
        error_response = utils.format_error(e)
        return error_response

def get_transactions(access_t, cursor_param):
    # Set cursor to empty to receive all historical updates
    # cursor = ''
    cursor = cursor_param

    # New transaction updates since "cursor"
    added = []
    modified = []
    removed = [] # Removed transaction ids
    has_more = True
    try:
        # Iterate through each page of new transaction updates for item
        while has_more:
            request = TransactionsSyncRequest(
                access_token=access_t,
                cursor=cursor,
            )
            response = client.transactions_sync(request).to_dict()
            # Add this page of results
            added.extend(response['added'])
            modified.extend(response['modified'])
            removed.extend(response['removed'])
            has_more = response['has_more']
            # Update cursor to the next cursor
            cursor = response['next_cursor']

        # Return the 50 most recent transactions
        # print('response type: ', type(response['added']))
        # print('response: ', utils.pretty_print_response(response['added']))
        latest_transactions = sorted(added, key=lambda t: t['date'])[-100:]
        return cursor, latest_transactions

    except plaid.ApiException as e:
        error_response = utils.format_error(e)
        return error_response

def squeeze_transaction(transaction):
  date_time = transaction["authorized_datetime"]
  if date_time is not None:
    date_time = date_time.strftime("%m/%d/%Y(%H:%M)")
  return {"_id": transaction["transaction_id"],
                        "date_authorized": date_time,
                        "name": transaction["name"],
                        "amount": transaction["amount"],
                        "category": "N/A"}