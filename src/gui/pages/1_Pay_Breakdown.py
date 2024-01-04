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

# +---------------+
# | Helpers    |
# +---------------+---------------------------------

def dollars(val, omit_sign=False):
    result = f"{'{:,.2f}'.format(val)}"
    if omit_sign: 
        return  result
    else: 
        return '$ ' + result

def percentage(val, omit_sign=True):
    result = f"{'{:.2%}'.format(val)}"
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
# | setup     |
# +---------------+---------------------------------
time_ranges = ['Yearly', 'Monthly', 'Bi-Weekly']
time_range = st.sidebar.selectbox('Breakdown', time_ranges)

# +-------------------+
# | Gross Income |
# +-------------------+---------------------------------
gi_monthly = YEARLY/12 # Monthly Gross Income
gi_biweekly = gi_monthly/2 # Bi-Weekly Gross Income
gross_switch = {'Yearly': YEARLY, 'Monthly': gi_monthly, 'Bi-Weekly': gi_biweekly}
amount_multiplier = 1 # bi-weekly
if time_range == 'Yearly':
    amount_multiplier = 26
elif time_range == 'Monthly':
    amount_multiplier = 2
gross = gross_switch[time_range]
l, r = st.columns(2)
l.title(f"{time_range} Gross")
r.title(f"{dollars(gross)}")

# +-------------------+
# | Pre-tax Deductions |
# +-------------------+---------------------------------
st.divider()
header = st.container()
pre_tax_deductions = [
    {'name': '401(k) Contribution', '%': .04, 'of': gross},
    {'name': 'HSA Contribution', '$': 25 * amount_multiplier},
    {'name': 'Aetna High Deductible', '%': .034, 'of': gross},
    {'name': 'Metlife Preferred Dental', '%': .01, 'of': gross}
]
df, total = _construct_table_and_total(pre_tax_deductions)

taxable = gross - total
l, r = st.columns(2)
l.header('Pre-Tax Deductions')
l.subheader(f"{dollars(total)} ({percentage(total/gross, omit_sign=False)}) ")
st.table(df)
st.divider()
l, r = st.columns(2)
l.title(f"Taxable")
r.title(f"{dollars(taxable)}")
# +-------------------+
# | Tax Deductions |
# +-------------------+---------------------------------
st.divider()
header = st.container()
# Declare taxes
taxes = [
    {'name': "FED TX Witholding Tax", '%': .146, 'of': taxable},
    {'name': "FED TX EE Social Security", '%': .064, 'of': taxable},
    {'name': "FED TX EE Medicare Tax", '%': .015, 'of': taxable},
    {'name': "DC TX Witholding Tax", '%': .0697, 'of': taxable}
]
# Create Tables
df, total = _construct_table_and_total(taxes)
net = taxable - total
l, r = st.columns(2)
l.header('Taxes')
l.subheader(f"{dollars(total)} ({percentage(total/taxable, omit_sign=False)}) ")
st.table(df)
st.divider()
l, r = st.columns(2)
l.title("Net Earnings")
r.title(f"{dollars(net)}")
# +-------------------+
# | Other Deductions |
# +-------------------+---------------------------------
st.divider()
# Calculate Insurance
deductions = [
    {'name': "Roth 401(k)", '%': .07, 'of': gross},
    {'name': "Student Loans", '$': 175.03 * amount_multiplier}
]

df, total = _construct_table_and_total(deductions)

net = net - total
l, r = st.columns(2)
l.subheader(f"Other Deductions")
l.subheader(f"{dollars(total)}")
st.table(df)
st.divider()
l, r = st.columns(2)
l.title(f"Net Income")
r.title(f"{dollars(net)}")


# +-------------------+
# | Spending   |
# +-------------------+---------------------------------
st.divider()
# Calculate Insurance
required_spending = [
    {'name': "Rent", '$': 1125 * amount_multiplier},
    {'name': "Wifi", '$': 45 * amount_multiplier},
    {'name': "Electricity", '$': 50 * amount_multiplier}
]

df, total = _construct_table_and_total(required_spending)

discretionary = net - total
l, r = st.columns(2)
l.subheader(f"Bills & Utilities")
l.subheader(f"{dollars(total)}")
st.table(df)
st.divider()
l, r = st.columns(2)
l.title(f"Discretionary Income")
r.title(f"{dollars(discretionary)}")