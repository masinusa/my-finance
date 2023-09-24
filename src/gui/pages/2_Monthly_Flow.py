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
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler=logging.FileHandler("/finapp/logs/gui.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# +---------------+
# | Setup Sidebar |
# +---------------+---------------------------------

# Choose month
with st.sidebar:
    month_offset = gui_utils.choose_month_widget()


    


# +------------------------------------------------------+
# | Calculate High-level Categories (living expenses/indulgences/other) |
# +------------------------------------------------------+---------------------
# Load Categories
categories = load_categories()
cat_totals = {}
# Tally Category totals
for cat in categories:
    total = 0
    # Get filtered Transactions
    trans = mongo.get_transactions(cat.name, month_offset=month_offset)
    # Tally total
    for i, t in enumerate(trans):
        amount = f"{float(t['amount']):.2f}"
        name = t['name']
        date = t['date_authorized']
        total += float(amount)
    # Save category total
    cat_totals[cat] = total
    

# Group categories
actual_income = 0
living_expenses, indulgences, others = {}, {}, {}
le_total, in_total, ot_total = 0, 0, 0
for i, (cat, total) in enumerate(cat_totals.items()):
    name = cat.name
    if name in ('Groceries', 'Athletics','Transportation', ):
        living_expenses[name] = '{:,.2f}'.format(total)
        le_total += total
    elif name in ('Takeout', 'Indulgence_Gift', 'Personal_Travel', 'Clothing_Indulgence', 'Fun_Clothing'):
        indulgences[name] = '{:,.2f}'.format(total)
        in_total += total
    elif name in ('Income',):
        actual_income = total
    else:
        others[name] = '{:,.2f}'.format(total)
        ot_total += total


# +-------------------+
# | Show Income |
# +-------------------+---------------------------------
st.title("2023 Yearly: $110,500")
st.title("Monthly --")
exp_income = 9208.33
st.subheader(f"Expected: ${exp_income}")
st.subheader(f"Actual: {actual_income}")

# +---------------------------------------+
# | Show Category Sums |
# +---------------------------------------+---------------------------------
# totals
total = le_total + in_total + ot_total
le_total = '{:,.2f}'.format(le_total)
in_total = '{:,.2f}'.format(in_total)
ot_total = '{:,.2f}'.format(ot_total)

# Headers
header_row = st.empty()
with header_row.container():
    l, m, r = st.columns(3, gap='large')
    l.title(f"Living Expenses: {le_total}")
    m.title(f"Indulgences: {in_total}")
    r.title(f"Others: {ot_total}")

# Category Tables
le_column, i_column, o_column = st.columns(3, gap='large')
with le_column:
    df = pd.DataFrame(living_expenses.values(), index=living_expenses.keys(), columns=[le_total])
    st.table(df)
with i_column:
    df = pd.DataFrame(indulgences.values(), index=indulgences.keys(), columns=[in_total])
    st.table(df)
with o_column:
    df = pd.DataFrame(others.values(), index=others.keys(), columns=[ot_total])
    st.table(df)

# +---------------------------------------+
# | Show Final Expenses |
# +---------------------------------------+---------------------------------
st.title(f"Spent: {total}")
st.title(f"Amount Left --")
st.subheader(f"Expected: ${exp_income - total}")
st.subheader(f"Actual: ${abs(actual_income) - total}")