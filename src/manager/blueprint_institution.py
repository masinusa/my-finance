import sys
import os 
from pathlib import Path
import requests

from flask import Blueprint, request, current_app

from manager.object_data_managers import AccountODM

institutions_blueprint = Blueprint('institutions_blueprint', __name__)

@institutions_blueprint.route('/accounts/', methods=['PUT'])
def _get_accounts():
    accounts = AccountODM.find()
    # # Request Information from Mongo DB
    # params = {"month_offset": month_offset}
    # current_app.logger.info(f"month_offset: {month_offset}")
    # transactions = requests.get("http://db_connector:5000/database/transactions", params=params)
    # # Parse result for each account in the database
    # current_app.logger.info(f"Response code from db_connector: {transactions.status_code}")
    # return json.dumps(transactions.json())

@institutions_blueprint.route('/accounts/', methods=['PUT'])
def _update_accounts():

    # Retrieve Transactions from plaid_api and update database
    return update_accounts()

