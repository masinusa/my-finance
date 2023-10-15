import requests
import pytest
import sys
import os 
from pathlib import Path
import datetime
import json

# base_container_path = str(Path(os.path.abspath(__file__)).parents[1]).replace('\\', '/')
# if base_container_path not in sys.path:
#     sys.path.append(base_container_path)
# if "/finapp/" not in sys.path:
#     sys.path.append('/finapp')

# from lib.utils.time_ import datetime_to_month_offset

def test_get_accesstokens():
    """ Test Mongo Database Balances retrieval """
    response = requests.get("http://db_connector:5000/database/access_tokens/")
    assert response.ok

def test_set_accesstokens():
    """ Test Mongo Database access_token posting """
    req_json = {'item': 'Chase', 'access_token': 'access-sandbox-605ef917-d2a1-4dc1-b310-d59cc03d8425'}
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
            assert item['access_token'] == 'access-sandbox-605ef917-d2a1-4dc1-b310-d59cc03d8425'
            return 
    assert False



