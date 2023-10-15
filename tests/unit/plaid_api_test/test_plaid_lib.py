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
from src.plaid_api.plaid_lib import create_link_token, get_access_token

def test_create_link_token():
    response = create_link_token()
    print(response.keys())
    assert list(response.keys()) == ['link_token', 'expiration', 'request_id']