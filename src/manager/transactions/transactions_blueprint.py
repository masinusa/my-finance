import sys
import os 
from pathlib import Path
import requests

from flask import Blueprint, request, current_app

# Add base container path
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from transactions.get_transactions import get_transactions
from transactions.update_transactions import update_transactions

transactions_blueprint = Blueprint('transactions_blueprint', __name__)

@transactions_blueprint.route('/transactions/')
def _get_transactions():
    month = request.args.get('month_offset')
    month = int(month)
    return get_transactions(month)

@transactions_blueprint.route('/transactions/', methods=['PUT'])
def _update_transactions():
    # Retrieve Transactions from plaid_api and update database
    return update_transactions()

