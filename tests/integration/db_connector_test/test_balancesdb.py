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

from lib.utils.time_ import datetime_to_month_offset

def test_get_balancesdb():
    """ Test Mongo Database Balances retrieval """
    June_2023_offset = datetime_to_month_offset(datetime.date(2023, 6, 23)) 
    params = { "month_offset": June_2023_offset }
    response = requests.get("http://db_connector:5000/database/balances/", params=params)
    assert response.ok

def test_update_balancesdb():
    """ Test Mongo Database Balances retrieval
    """
    June_2023_offset = datetime_to_month_offset(datetime.date(2023, 6, 23))
    params = { "month_offset": June_2023_offset }
    # Update
    data = {
        'institution': "example_institution",
        'balance': 100,
        'account': 'checkings',
        'subtype': 'checking' 
    }     
    response = requests.put("http://db_connector:5000/database/balances/update", params=params, json=json.dumps(data))
    assert response.ok
        
    # Check Successful Update
    response = requests.get("http://db_connector:5000/database/balances/", params=params)
    json_response = response.json()[0]
    print(type(json_response))
    print(json_response)
    assert data['institution'] == json_response['institution']
    assert data['balance'] == json_response['balance']
    assert response.ok


