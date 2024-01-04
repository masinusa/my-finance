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
# | Globals       |
# +---------------+---------------------------------
YEARLY = 112000 # Yearly Gross Income

def dollars(val, omit_sign=False):
    result = f"{'{:,.2f}'.format(val)}"
    if omit_sign: 
        return  result
    else: 
        return '$' + result

def percentage(val, omit_sign=True):
    result = f"{'{:.0%}'.format(val)}"
    if omit_sign: 
        return  result.split('%')[0]
    else: 
        return result
    
def _construct_table_and_total(deductions):
    """ Converts deductions to a table and returns total amount"""
    df = pd.DataFrame()
    total = 0
    for d in deductions:
        if '%' in d:
            amount = d['%'] * d['of']
            row = {"Taxes": d['name'], "%": percentage(d['%']), "$": dollars(amount, omit_sign=True)}
            total += amount
        elif '$' in d:
            row = {"Taxes": d['name'], "%": "--", "$": dollars(d['$'])}
            total += d['$']
        else:
            raise Exception("Deduction must have '%' or $")
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df = df.set_index(["Taxes"])
    return df, total

# +---------------+
# | Setup Sidebar |
# +---------------+---------------------------------

# Choose month
with st.sidebar:
    month_offset = gui_utils.choose_month_widget()
    show_uncategorized = st.checkbox("Show Uncategorized Transactions", value=True)

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
    if name in ('Groceries', 'Athletics','Transportation', 'Bills', 'Quality_of_Life', 'Clothing'):
        living_expenses[name] = '{:,.2f}'.format(total)
        le_total += total
    elif name in ('Takeout', 'Indulgence_Gift', 'Personal_Travel', 'Clothing_Indulgence', 'Fun_Clothing'):
        indulgences[name] = '{:,.2f}'.format(total)
        in_total += total
    elif name in ('Income',):
        actual_income += total
    elif name in ('Ignore',):
        pass
    else:
        others[name] = dollars(total, omit_sign=True)
        ot_total += total
if show_uncategorized:
    na_total = 0
    trans = mongo.get_transactions('N/A', month_offset=month_offset)
    # Tally total
    for i, t in enumerate(trans):
        amount = f"{float(t['amount']):.2f}"
        name = t['name']
        date = t['date_authorized']
        na_total += float(amount)
    others['N/A'] = dollars(na_total, omit_sign=True)
    ot_total += na_total
# +-------------------+
# | Gross Income |
# +-------------------+---------------------------------
gi_monthly = YEARLY/12
gi_biweekly = gi_monthly/2
net_monthly = gi_monthly


# +-------------------+
# | Pre-tax Deductions |
# +-------------------+---------------------------------
pre_tax_deductions = [
    {'name': '401(k) Contribution', '%': .04, 'of': gi_monthly},
    {'name': 'HSA Contribution', '$': 25},
    {'name': 'Aetna High Deductible', '%': .034, 'of': gi_monthly},
    {'name': 'Metlife Preferred Dental', '%': .01, 'of': gi_monthly}
]
df, total = _construct_table_and_total(pre_tax_deductions)

taxable = gi_monthly - total
# +-------------------+
# | Tax Deductions |
# +-------------------+---------------------------------

# Declare taxes
taxes = [
    {'name': "FED TX Witholding Tax", '%': .146, 'of': taxable},
    {'name': "FED TX EE Social Security", '%': .064, 'of': taxable},
    {'name': "FED TX EE Medicare Tax", '%': .015, 'of': taxable},
    {'name': "DC TX Witholding Tax", '%': .0697, 'of': taxable}
]
# Create Tables
df, total = _construct_table_and_total(taxes)
net_monthly = taxable - total
# +-------------------+
# | Other Deductions |
# +-------------------+---------------------------------
# Calculate Insurance
deductions = [
    {'name': "Roth 401(k)", '%': .07, 'of': gi_monthly},
    {'name': "Drip Acount", '$': 500}
]

df, total = _construct_table_and_total(deductions)

net_monthly = net_monthly - total
# +-------------------+
# | Net Income |
# +-------------------+---------------------------------
l, r = st.columns(2)
l.title(f"Predicted")
r.title(f"{dollars(net_monthly)}")
l.title("Recieved")
r.title(str(dollars(actual_income * -1)))
st.divider()

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
st.title(f"Spent: {dollars(total)}")
st.title(f"Remaining: {dollars(net_monthly - total)}")
# st.subheader(f"Expected: ${exp_income - total}")
# st.subheader(f"Actual: ${abs(actual_income) - total}")