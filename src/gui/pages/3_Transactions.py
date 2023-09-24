import requests
import sys
import os 
from pathlib import Path
from datetime import datetime
import logging

import streamlit as st
from streamlit_modal import Modal
import streamlit.components.v1 as components

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
        logger.info("Updating Transactions")
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
    modal_cols = st.columns((1, 1, 2, 2, 1))
    for col, header in zip(modal_cols, col_headers):
        col.write(header)
    
    # parse transaction data
    amount = f"{float(transaction['amount']):.2f}"
    account = transaction['account']
    name = transaction['name']
    date = transaction['date_authorized']
    category = transaction['category']
    
    # print transaction data
    for col, val in zip(modal_cols, (amount, account, name, date, category)):
                        col.write(val)
    
    # Show Edit Options
    cat_dropdown, _, apply_but, cancel_but = st.columns((1,2,1,1))
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
modal = Modal(key="Transaction Modal", title="Transaction")
total = 0   

# Pring Headers
title = st.empty()

cols_size_1 = (1, 3, 2, 2) # numbers represent width
col_headers = ['Amount', 'Name', "Date", "Action"]
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
    with cols[3]:
        view, edit = st.columns(2, gap="small")
        view_phold = view.empty()
        edit_phold = edit.empty()
        view = view_phold.button("View", key=f"view_{i}")
        edit = edit_phold.button("Edit", key=f"edit_{i}")

    # Keep Editin if already editing
    if st.session_state.edit_view:
        if (name == st.session_state.edit_transaction['name'] and 
            t['amount'] == st.session_state.edit_transaction['amount']):
            _open_edit_view(st.session_state.edit_transaction)
    
    # Detailed View popup (modal popup)
    if view:
            with modal.container():
                cols_size_2 = (1, 1, 2, 2, 1) # numbers represent width
                col_headers = ['ID', 'Amount', 'Account', 'Name', "Date Authorized", "Category"]
                modal_cols = st.columns(cols_size_2)
                # print headers
                for col, header in zip(modal_cols, col_headers):
                    col.write(header)
                # print detailed transaciton
                for col, val in zip(modal_cols, (t['_id'],amount, t['account'], name, date, t['category'])):
                    col.write(val)
    # Open Edit view
    if edit:
        _open_edit_view(t)

with title.container():
    cat = 'Uncategorized' if category == 'N/A' else category
    st.title(f"{cat}: ${total:,}")

                # manual_category = st.selectbox(
                #     'Manual Category',
                #     categories, on_change=_keep_state)
                # apply = st.button("Apply Category")
                # if apply:
                #     t['category'] = manual_category
                #     logger.info(f"Categorizing transaction ({t['_id']}): {manual_category}")
                #     mongo.set_transaction(t)
                
            # modal.open()
            # button_phold.empty()  #  remove button
    