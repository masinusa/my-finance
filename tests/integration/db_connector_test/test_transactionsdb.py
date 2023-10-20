import requests
import pytest
import sys
import os 
from pathlib import Path
import datetime
import json
import random

from datetime import date

base_container_path = str(Path(os.path.abspath(__file__)).parents[1]).replace('\\', '/')
if base_container_path not in sys.path:
    sys.path.append(base_container_path)
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from lib.utils.time_ import datetime_to_month_offset

def test_get_transactions():
    """ Test Mongo Database Transactions retrieval """
    June_2023_offset = datetime_to_month_offset(datetime.date(2023, 6, 23)) 
    params = { "month_offset": June_2023_offset }
    response = requests.get("http://db_connector:5000/database/transactions/", params=params)
    assert response.ok

def test_update_balancesdb():
    """ Test Mongo Database Balances retrieval
    """
    today = date.today()
    month_offset = datetime_to_month_offset(today)
    params = { "month_offset": month_offset }
    rand_value1 = random.randrange(-100, 100)
    rand_value2 = random.randrange(-100, 100)
    # Update
    transactions = [{'_id': 'ygkppVXdVaI8b3KqJGXeTwQwywx5eKsWrn4yg', 'account': 'Chase', 'amount': str(rand_value1), 'category': 'N/A', 'date_authorized': str(today), 'name': 'TEST TRANSACTION 1'}, 
                    {'_id': 'ZLEJJqZbqxIolABPLzN6c7X7N7Z8vgCr8merx', 'account': 'Chase', 'amount': str(rand_value2), 'category': 'N/A', 'date_authorized': str(today), 'name': 'TEST TRANSACTION 2'}]  
    response = requests.put("http://db_connector:5000/database/transactions/", params=params, json=json.dumps(transactions))
    assert response.ok
        
    # Check Successful Update
    response = requests.get("http://db_connector:5000/database/transactions/", params=params)
    json_response = response.json()
    # print(type(json_response))
    # print(json_response)
    # assert both test transactions exist with current date
    check = 2
    for t in json_response:
        # print(t['date_authorized'])
        # print(t['name'])
        # print(t['amount'])
        if (t['date_authorized'] == str(today)):
            if (t['name'] == 'TEST TRANSACTION 1' and t['amount'] == str(rand_value1)):
                check -= 1
            elif t['name'] == 'TEST TRANSACTION 2' and t['amount'] == str(rand_value2):
                check -= 1
    assert check == 0
    assert response.ok


