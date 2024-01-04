import requests
import pytest
import sys
import os 
from pathlib import Path
import datetime
import json

base_container_path = str(Path(os.path.abspath(__file__)).parents[1]).replace('\\', '/')
if base_container_path not in sys.path:
    sys.path.append(base_container_path)
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from lib.utils import time_

def test_get_transaction_cursors():
    """ Test Mongo Database Transactions Cursors Retrieval """
    response = requests.get("http://db_connector:5000/database/transaction_cursors/")
    print(response.json())
    assert response.ok

def test_set_transaction_cursors():
    """ Test Mongo Database Transactions Cursors Setting """
    response = requests.get("http://db_connector:5000/database/transaction_cursors/")
    cursors = response.json()
    inst = cursors[0]['bank_name']
    cur = cursors[0]['transaction_cursor']
    req_json = {
        'institution': inst,
        'transaction_cursor': cur
        }
    response = requests.put("http://db_connector:5000/database/transaction_cursors/", json=req_json)

    response = requests.get("http://db_connector:5000/database/transaction_cursors/")
    assert response.ok
    print(response.json())
    check = 1
    for cursor in response.json():
        if time_.timestamp() == cursor['last_updated'] and inst == cursor['bank_name'] and cur == cursor['transaction_cursor']:
            check -= 1
    assert check == 0
    assert response.ok

def test_get_accesstokens():
    """ Test Mongo Database Balances retrieval """
    response = requests.get("http://db_connector:5000/database/access_tokens/")
    assert response.ok

def test_set_accesstokens():
    """ Test Mongo Database access_token posting """
    req_json = {'item': 'Chase', 'access_token': 'access-sandbox-c1da46e8-2c29-4167-ae88-a179c5e18f2d'}
    response = requests.post("http://db_connector:5000/database/access_tokens/", json=req_json)
    assert response.ok

    response = requests.get("http://db_connector:5000/database/access_tokens/")
    assert response.ok
    resp_json = response.json()
    print(resp_json)
    for item in resp_json:
        print("Item values")
        print(item.values())
        if 'Chase' in item.values():
            assert item['access_token'] == 'access-sandbox-c1da46e8-2c29-4167-ae88-a179c5e18f2d'
            assert item['last-updated'] == time_.timestamp()
            return 
    assert False



