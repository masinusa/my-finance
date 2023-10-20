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

def test_manager_get_transactions():
    """ Test Manager Transactions retrieval """
    June_2023_offset = datetime_to_month_offset(datetime.date(2023, 6, 23)) 
    params = { "month_offset": June_2023_offset }
    response = requests.get("http://manager:5000/transactions/", params=params)
    assert response.ok

def test_manager_update_transactions():
    """ Test Mongo Database transactions retrieval
    """
    params = { "month_offset": 0 }
    # Update
    response = requests.put("http://manager:5000/transactions/", params=params)
    print(response)
    assert response.ok
        
    # # Check Successful Update
    # response = requests.get("http://manager:5000/balances/", params=params)
    # assert response.ok


