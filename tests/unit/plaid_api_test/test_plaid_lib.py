import requests
import pytest
import sys
import os 
from pathlib import Path
import datetime
import json

import flask

base_container_path = str(Path(os.path.abspath(__file__)).parents[1]).replace('\\', '/')
if base_container_path not in sys.path:
    sys.path.append(base_container_path)
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from lib.utils.time_ import datetime_to_month_offset
from src.plaid_api.plaid_lib import create_link_token, get_access_token, item, latest_transactions

def test_create_link_token():
    response = create_link_token()
    print(response.keys())
    assert list(response.keys()) == ['link_token', 'expiration', 'request_id']

def test_item():
    access_token='access-sandbox-c1da46e8-2c29-4167-ae88-a179c5e18f2d'
    bank_name = item(access_token)['institution']['name']
    assert bank_name == 'Chase'

def test_latest_transactions():
    app = flask.Flask(__name__)
    access_token='access-sandbox-c1da46e8-2c29-4167-ae88-a179c5e18f2d'
    with app.app_context():
        transactions = latest_transactions(access_token)
    cursor = transactions[0]
    print(cursor)
    assert cursor == 'CAESJW5QUmpqNUc0NVhoNUx6cEFNUDZNaXdReEVxeXk2OUMzUXd5dkIaDAiRubmpBhDI+9PIAyIMCJG5uakGEMj708gDKgwIkbm5qQYQyPvTyAM='
    transactions = json.loads(transactions[1].get_data(as_text=True))
    assert type(transactions) == dict