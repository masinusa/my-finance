import requests
import sys
import os 
from pathlib import Path
from datetime import datetime
import logging

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
# +-----------------+
# | Initialize Page |
# +-----------------+-----------------------------------------------
# Setup logger
logger = logging.getLogger(__name__)
if sum([isinstance(handler, logging.FileHandler) for handler in logger.handlers]):
    logger.setLevel(logging.DEBUG)
    handler=logging.FileHandler("/finapp/logs/gui.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


banks = mongo.get_access_tokens()

categories = [cat.name for cat in load_categories()]
categories.append('N/A')

if "edit_view" not in st.session_state or "edit_transaction" not in st.session_state:
    st.session_state.edit_view = False
    st.session_state.edit_transaction = None

SESSION_STATE = st.session_state
# +---------------+
# | Load Sidebar |
# +---------------+-----------------------------------------------
with st.sidebar:
    # Show Configuration Options
    month_offset = gui_utils.choose_month_widget()
    category = st.selectbox('Category', categories, index=(len(categories)-1))
    categorize = st.button("Re-Categorize")
    if categorize:
        st.write(transactions.sort(month_offset=month_offset))
    update = st.button("Update Transactions")

    # +--------------------------------------+
    # | Update Transactions (inside sidebar) |
    # +--------------------------------------+---------------------------------
    if update:
        with st.spinner('Updating Transactions...'):
            try:
                resp_status = requests.put('http://manager:5000/transactions', timeout=30)
                resp_status = resp_status.json()['status']
            except requests.exceptions.JSONDecodeError as e:
                try: st.warning(resp_status.text)
                except:
                    st.error(f"No JSON or text recieved. Status Code: {resp_status.status_code}")
                    st.error(e)
                    sys.exit()
                sys.exit()
        # st.write(resp_status)
        success_count = len([x for x in resp_status if x['code'] == 200 ])
        st.success(f"Updated {success_count}/{len(resp_status)}")
        for item in [x for x in resp_status if x['code'] != 200]:
            st.write(f"Failed to retrieve {item['institution']}")

# +-----------------------+
# | Edit Transaction View |
# +-----------------------+---------------------------------
def _open_edit_view(transaction):
    # persist edit view
    st.session_state.edit_view = True
    st.session_state.edit_transaction = transaction

    # Print Information
    st.write('---')
    st.title("Edit Transaction")
    # print headers
    col_headers = ['Amount', 'Account', 'Name', "Date Authorized", "Category"]
    cols = st.columns((1, 1, 2, 2, 1))
    for col, header in zip(cols, col_headers):
        col.write(header)
    
    # parse transaction data
    amount = f"{float(transaction['amount']):.2f}"
    account = transaction['account']
    name = transaction['name']
    date = transaction['date_authorized']
    category = transaction['category']
    
    # print transaction data
    for col, val in zip(cols, (amount, account, name, date, category)):
                        col.write(val)
    
    # Show Edit Options
    cat_dropdown, _, apply_but, cancel_but = st.columns((2,1,1,1))
    manual_cat = cat_dropdown.selectbox( 'Change Category to:', categories, args = (transaction,))
    apply_but.button("Apply", on_click=_apply_edit, args=(transaction, manual_cat))
    cancel_but.button("Cancel", on_click=_cancel_edit)
    st.write('---')


def _cancel_edit():
    st.session_state.edit_view = False  
    st.session_state.edit_transaction = None

def _apply_edit(transaction, category):
    transaction['category'] = category
    logger.info(f"Categorizing transaction ({transaction['_id']}:{transaction['name']}:{transaction['name']}): {category}")
    mongo.set_transaction(transaction)
    _cancel_edit()

# +---------------------------------------+
# | Show Transactions (category specific) |
# +---------------------------------------+---------------------------------
# Setup 
total = 0   

# Pring Headers
title = st.empty()

cols_size_1 = (1, 3, 2, 2) # numbers represent width
col_headers = ['Amount', 'Name', "Date", ""]
for col, header in zip(st.columns(cols_size_1), col_headers):
    col.write(header)

# List each transaction
trans = mongo.get_transactions(category, month_offset=month_offset)
for i, t in enumerate(trans):
    cols = st.columns(cols_size_1)
    amount = f"{float(t['amount']):.2f}"
    name = t['name']
    date = t['date_authorized']
    for col, val in zip(cols, (amount, name, date)):
        col.write(val)
    total += float(amount)
    edit = cols[3]
    with edit:
        edit_phold = edit.empty()
        edit = edit_phold.button("Edit", key=f"edit_{i}")

    # Keep Editin if already editing
    if st.session_state.edit_view:
        if (name == st.session_state.edit_transaction['name'] and 
            t['amount'] == st.session_state.edit_transaction['amount']):
            _open_edit_view(st.session_state.edit_transaction)
    # Open Edit view
    if edit:
        _open_edit_view(t)

with title.container():
    cat = 'Uncategorized' if category == 'N/A' else category
    st.title(f"{cat}: $ {total:,.2f}")
