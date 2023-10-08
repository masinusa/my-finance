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
YEARLY = 112000

def dollars(val, omit_sign=False):
    result = f"{'{:,.2f}'.format(val)}"
    if omit_sign: 
        return  result
    else: 
        return '$' + result

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
# | Gross Income |
# +-------------------+---------------------------------
st.title("Gross Income")
st.divider()
monthly = YEARLY/12
biweekly = monthly/2
l, m, r = st.columns(3)
m.subheader(f"Monthly: ${'{:,.2f}'.format(monthly)}")
l.subheader(f"Yearly: ${'{:,}'.format(YEARLY)}")

r.subheader(f"Bi-Weekly: ${'{:,.2f}'.format(biweekly)}")
net_monthly = monthly

# +-------------------+
# | Show Monthly Taxes |
# +-------------------+---------------------------------
st.divider()
header = st.container()

# Declare taxes
taxes = {
    "Federal Income": .1572,
    "State Income": .0609,
    "FICA": .0765
}
# Create Tables
tax_df = pd.DataFrame()
tax_total = 0
for k, v in taxes.items():
    row = {"Taxes": k, "%": "{:.0%}".format(v), "$":'{:,.2f}'.format(v * monthly)}
    tax_total += v * monthly
    tax_df = pd.concat([tax_df, pd.DataFrame([row])], ignore_index=True)
    # taxes[k] = f"- {'{:,.2f}'.format(v)}"
tax_df = tax_df.set_index(["Taxes"])
net_monthly -= tax_total
st.subheader(f"Monthly Taxes:")
st.table(tax_df)
st.subheader(f"Monthly - {dollars(tax_total, omit_sign=True)} = {dollars(net_monthly)}")
# +-------------------+
# | Show Deductions |
# +-------------------+---------------------------------
st.divider()
insurance_col, contributions_col = st.columns(2)
# Calculate Insurance
insurance = {
    "health": 1000,
    "vision": 200,
    "dental": 100
}
# Calculate Insurance
contributions = {
    "Traditional 401 (k)": .03,
    "Roth 401 (K)": .06,
    "drip account": 500
}

# Cleanup Insurance
ins_df = pd.DataFrame()
ins_total = 0
for k, v in insurance.items():
    row = {"Insurance": k, "$":'{:,.2f}'.format(v)}
    ins_total += v
    ins_df = pd.concat([ins_df, pd.DataFrame([row])], ignore_index=True)
ins_df = ins_df.set_index(["Insurance"])
# Cleanup Contributions
contrib_df = pd.DataFrame()
contrib_total = 0
for k, v in contributions.items():
    if k == 'drip account':
        row = {"Contributions": k, "%": "--", "$":'{:,.2f}'.format(v)}
        contrib_total += v
    else:
        row = {"Contributions": k, "%": "{:.0%}".format(v), "$":'{:,.2f}'.format(v * monthly)}
        contrib_total += v * monthly
    contrib_df = pd.concat([contrib_df, pd.DataFrame([row])], ignore_index=True)
contrib_df = contrib_df.set_index(["Contributions"])
# Display Tables

insurance_col.subheader(f"Insurance: ${'{:,.2f}'.format(ins_total)}")
insurance_col.table(ins_df)
contributions_col.subheader(f"Contributions: ${'{:,.2f}'.format(contrib_total)}")
contributions_col.table(contrib_df)

arithmetic_pt1 = f"${'{:,.2f}'.format(net_monthly)}"
net_monthly -= ins_total + contrib_total
pt2 = f"- ${'{:,.2f}'.format(ins_total)} - ${'{:,.2f}'.format(contrib_total)}= ${'{:,.2f}'.format(net_monthly)}"
st.subheader(f"Remaining Monthly - {dollars(ins_total, omit_sign=True)} - {dollars(contrib_total, omit_sign=True)} =  {dollars(net_monthly)}")

# header.header(f"Monthly Deductions: $ {'{:,.2f}'.format(tax_total + contrib_total + ins_total)}")
# +-------------------+
# | Net Income |
# +-------------------+---------------------------------
st.divider()
st.title(f"Net Monthly Income: ${'{:,.2f}'.format(net_monthly)}")
st.subheader(f"Actual Net Income: $--")

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