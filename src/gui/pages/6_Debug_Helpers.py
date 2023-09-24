import requests
import sys
import os 
from pathlib import Path
from datetime import datetime

import streamlit as st

base_container_path = str(Path(os.path.abspath(__file__)).parents[1]).replace('\\', '/')
if base_container_path not in sys.path:
    sys.path.append(base_container_path)
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')


from lib.mongo import mongo
from categories.directory import load_categories
import transactions
import gui_utils


reset_categories = st.button("Reset Categories")
month = gui_utils.choose_month_widget()
if reset_categories:
   transactions = mongo.get_transactions(month)
   for t in transactions:
       t['category'] = 'N/A'
       mongo.set_transaction(t)