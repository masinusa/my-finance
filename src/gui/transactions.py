import requests
import sys
import os 
from pathlib import Path
from datetime import datetime
import logging

base_container_path = str(Path(os.path.abspath(__file__)).parents[1]).replace('\\', '/')
if base_container_path not in sys.path:
    sys.path.append(base_container_path)
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')


from lib.mongo import mongo
from categories.directory import load_categories
import gui_utils
from lib import utils


# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler=logging.FileHandler("/finapp/logs/mongo_debug.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

categories = load_categories()

def sort(month_offset: int = 0):
  transactions = mongo.get_transactions(category='N/A', month_offset=month_offset)
  count = 0
  for t in transactions:
      category = 'N/A'
      for cat in categories:
        logger.debug(f"Checking Category: {cat.name}")
        if cat.check(t):
          category = cat.name
          t['category'] = category
          logger.debug(f"Found keyword in {t['name']}, setting category: {cat.name}")
          mongo.set_transaction(t)
          count += 1
        
  return count