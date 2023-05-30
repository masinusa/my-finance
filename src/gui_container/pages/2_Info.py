import requests
import sys
import os 
from pathlib import Path

import streamlit as st

base_container_path = str(Path(os.path.abspath(__file__)).parents[1]).replace('\\', '/')
if base_container_path not in sys.path:
    sys.path.append(base_container_path)
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')


from lib.mongo import mongo
from lib import utils


# _____ Active Banks _____
st.title('Active Banks')
banks = mongo.get_institutions()
for bank in banks:
    st.write(bank['bank_name'])
    
# _____ Bank Balances _____
st.title('Bank Balances')
# Set dataholders
total_balance = 0
balances = {}
oldest_update = 99999999

  
doc = mongo.get_monthly_balances(month_offset=0)
for account in doc:
    balance = account['balance']
    institution = account['institution']
    last_updated = account['last_updated']
    total_balance += balance
    balances[f"{institution}"] = balance
    time_val = utils.time.timestamp_to_int(account['last_updated'])
    if time_val < oldest_update:
        oldest_update = time_val

            
balances['total_balance'] = total_balance
st.table(balances)
st.write(f"Oldest update: {utils.time.int_to_timestamp(oldest_update)}")


# _____ Refresh Bank Balances _____
refresh = st.button("refresh balances")
if refresh:
    # Setup progress bar
    progress_text = "Gathering Bank Information"
    progress = 0
    progress_bar = st.progress(progress, text=progress_text)

    progress_bar.progress(progress + 5, text=f"{progress_text}\n\nLoading First Bank")
    for bank in [b for b in banks if b['working']]:
        try:
            resp = requests.get('http://plaid:5000/api/get_balance', params={"access_token":bank['access_token']})
            progress_bar.progress(progress + 5, text=f"{progress_text}\n\nLoading {bank['bank_name']}")

            # Update progress bar
            progress += int((1/len(banks))*100)
            if progress >= 100: progress = 100
            progress_bar.progress(progress, text=f"{progress_text}\n\nCompleted {bank['bank_name']}")
        except Exception as e:
            st.error(f"Failed bank: {bank['bank_name']}")
            st.error(e)
            st.write(e)
            sys.exit()
    progress_bar.progress(progress, text='Finished Refreshing Bank Balances') 
