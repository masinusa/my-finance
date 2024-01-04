import sys
import os 
from pathlib import Path
import requests

from fastapi import APIRouter

from manager.object_data_managers import AccountODM

account_api = APIRouter()

@account_api.get("/account/")
def _get_accounts():
    accounts = AccountODM.find()
    # # Request Information from Mongo DB
    # params = {"month_offset": month_offset}
    # current_app.logger.info(f"month_offset: {month_offset}")
    # transactions = requests.get("http://db_connector:5000/database/transactions", params=params)
    # # Parse result for each account in the database
    # current_app.logger.info(f"Response code from db_connector: {transactions.status_code}")
    # return json.dumps(transactions.json())

@account_api.put("/account/")
def _update_accounts():

    # Retrieve Transactions from plaid_api and update database
    return update_accounts()

