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
from lib.mongo import transactions
from lib import utils


banks = mongo.get_institutions()

categories = list(transactions.category_keywords.keys())
categories.append('N/A')

# _____ Transactions _____
# https://discuss.streamlit.io/t/drop-down-list-in-table/19662
with st.sidebar:
    option = st.selectbox(
    'Category',
    categories)


    # _____ Refresh Bank Balances _____
    update = st.button("Update Transactions")
    if update:
        # Setup progress bar
        progress_text = "Updating Transaction Information"
        progress = 0
        progress_bar = st.progress(progress, text=progress_text)

        progress_bar.progress(progress + 5, text=f"{progress_text}\n\nLoading First Institution")
        for bank in [b for b in banks if b['working']]:
              try:
                  progress_bar.progress(progress + 5, text=f"{progress_text}\n\nLoading {bank['bank_name']}")
                  resp = requests.get('http://plaid:5000/api/get_transactions', params={"access_token":bank['access_token']})

                  # Update progress bar
                  progress += int((1/len(banks))*100)
                  if progress >= 100: progress = 100
                  progress_bar.progress(progress, text=f"{progress_text}\n\nCompleted {bank['bank_name']}")
              except Exception as e:
                  st.error(f"Failed bank: {bank['bank_name']}")
                  st.error(e)
                  st.write(e)
        progress_bar.progress(progress, text=f"Finished Updating Transaction Information\n\n{resp.text}") 




st.title('Transactions')
categorize = st.button("Re-Categorize")
if categorize:
    transactions.sort_uncategorized()


trans = mongo.get_transactions(option)
show = []
total = 0   
for t in trans:
    show_t = {
        'amount': t['amount'],
        'name': t['name'],
        'date': t['date_authorized']
    }
    show.append(show_t)
    total += show_t['amount']
st.write(f"Total Spending: {total}")
st.table(show)

reset = st.button('Reset Categorizations')
if reset:
    transactions.reset_categories()