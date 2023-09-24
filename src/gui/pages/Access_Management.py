import requests
import sys
import os 
from pathlib import Path
import logging
import pandas as pd

import streamlit as st

base_container_path = str(Path(os.path.abspath(__file__)).parents[1]).replace('\\', '/')
if base_container_path not in sys.path:
    sys.path.append(base_container_path)
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')


from lib.mongo import mongo
from lib import utils
from breakdown import Breakdown
from balances import Balance, load_balances, update_balances
import gui_utils
from categories.directory import load_categories

# Setup logger
logger = gui_utils.setup_logger(__name__)


def _check_at_status():
   
   # Get current access tokens
   a_tokens = mongo.get_access_tokens()

   # Setup progress bar
   progress, p_text, p_step  = 0, "Checking Access Token", int((1/len(a_tokens))*100)
   progress_bar = st.progress(progress, text=p_text)
   progress_bar.progress(progress + 5, text=f"{p_text}\n\nLoading First Bank")

   # Iterate through each institution
   for a_t in a_tokens:
      if a_t['working']:
         try:
            # Update progress bar
            progress_bar.progress(progress + 5, text=f"{p_text}\n\nChecking {a_t['bank_name']} Token")

            # request plaid information to check token
            resp = requests.get('http://plaid:5000/api/get_balance', params={"access_token":a_t['access_token']}, timeout=10)
            

         except Exception as e:
            st.error(f"Failed bank: {a_t['bank_name']}")
            st.error(e)
            logger.debug(f"Access token for: {a_t['bank_name']} is not working: {e.__str__()}")
            mongo.set_access_token(a_t['access_token'], a_t['bank_name'], working=False )
         
         # Update progress bar
         progress += p_step
         if progress >= 100: progress = 100
         progress_bar.progress(progress, text=f"{p_text}\n\nCompleted {a_t['bank_name']}")

   progress_bar.progress(progress, text='Finished Refreshing Bank Balances') 

if __name__ == '__main__':
   
   # get current access tokens
   a_tokens = mongo.get_access_tokens()

   # Display token status
   df = pd.DataFrame(a_tokens)
   st.table(df)

   # Allow option to update Access Tokens
   update = st.button("Update Token Status", on_click=_check_at_status)

