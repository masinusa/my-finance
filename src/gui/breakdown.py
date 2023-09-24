from abc import ABC, abstractmethod
import requests
import sys
import os 
from pathlib import Path

if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from lib.mongo import mongo
from lib import utils

class Breakdown(ABC):
    
    def __init__(self, month: int):
        self.month = month
        self.base_salary = 0
        self.balances = {
            'account_balances': {},
            'total_balance': 0,
            'last_updated': None,
        }

    def get_balances(self):
        if self.balances['last_updated']:
            return self.balances
        else:
            db_balances = mongo.get_monthly_balances(month_offset=self.month)
            for account in db_balances:
                balance = account['balance']
                institution = account['institution']
                last_updated = account['last_updated']
                self.balances['total_balance'] += balance
                self.balances['account_balances'][f"{institution}"] = round(balance, 2).__str__()
                time_val = utils.time_.timestamp_to_int(last_updated)
                oldest_update = self.balances['last_updated']
                if oldest_update is None or time_val < oldest_update:
                    oldest_update = time_val
                self.balances['last_updated'] = oldest_update
            return self.balances