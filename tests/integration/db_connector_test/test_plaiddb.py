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
