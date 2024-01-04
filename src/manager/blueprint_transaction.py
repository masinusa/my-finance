import sys
import os 
from pathlib import Path
import requests

from flask import Blueprint, request, current_app

from manager.balances.BalanceODM import TransactionODM

transactions_blueprint = Blueprint('transactions_blueprint', __name__)

@transactions_blueprint.route('/transactions/<int:month_offset>')
def _get_transactions(month_offset):
    transactions = TransactionODM.find()
    # # Request Information from Mongo DB
    # params = {"month_offset": month_offset}
    # current_app.logger.info(f"month_offset: {month_offset}")
    # transactions = requests.get("http://db_connector:5000/database/transactions", params=params)
    # # Parse result for each account in the database
    # current_app.logger.info(f"Response code from db_connector: {transactions.status_code}")
    # return json.dumps(transactions.json())

@transactions_blueprint.route('/transactions/', methods=['PUT'])
def _update_transactions():
    # Retrieve Transactions from plaid_api and update database
    return update_transactions()

