

# Standard Library Imports
import os
from dotenv import load_dotenv

# 3rd Pary Imports
import openpyxl as xl

# Local Imports
import cookbook
from cookbook.categorize import categorize
from cookbook.plaid_retrievals import squeeze_transaction
from cookbook import secrets


# +------------------------------+
# | Initialize Helpful Variables |
# +------------------------------+---------------------------------------------

# Load Environment Variables
load_dotenv('.env')
CURRENT_TEMPLATE= os.environ.get("CURRENT_TEMPLATE")
WORKBOOK = os.environ.get("WORKBOOK")

# Load Secrets
PLAID_CLIENT_ID = secrets.PLAID_CLIENT_ID
PLAID_SECRET = secrets.PLAID_SECRET
access_tokens = secrets.access_tokens

# Initalize Helpful Variables
workbook_path = '/finapp/' + WORKBOOK


# +---------------+
# | Load Workbook |
# +---------------+------------------------------------------------------------

# Create workbook object
workbook = cookbook.Workbook(workbook_path, CURRENT_TEMPLATE)


# +---------------+
# | Load Context |
# +---------------+-------------------------------------------------------------

# Set workbooks active sheet to this month
ws = cookbook.curr_month_year()
workbook.active = workbook[ws]


# +------------------+
# | Enforce Template |
# +------------------+-------------------------------------------------------------

# Save all current sheet values
curr_values = workbook.sheet_values(ws)

# Enforce the sheet template
workbook.copy_template(workbook._load_sheet(ws), workbook._load_template(CURRENT_TEMPLATE))

# Write values back into the sheet
for key, value in curr_values.items():
  workbook.update_value(key, value, workbook._load_sheet(ws), workbook._load_template(CURRENT_TEMPLATE))

# +----------------------------+
# | Update Total Balance       |
# +----------------------------+-------------------------------------------------------------

# Calculate balance total
balance = cookbook.calculate_total(access_tokens)

# Write balance to sheet
workbook.update_value('{total}', balance, workbook.active)
# print(workbook.sheet_values(ws))

# +-------------------------------------------------+
# | Aggregate and Write Transactions  |
# +-------------------------------------------------+-------------------------------------

# Retrieve all of this month's transactions
transactions = cookbook.get_saved_transactions()

totals = {}
category = ''
amount = 0
for transaction in transactions:
  category = transaction['category']
  amount = transaction['amount']
  if category in totals.keys():
    totals[category] += amount
  else:
    totals[category] = amount

for category, aggregate in totals.items():
  # print("CAT: ", category)
  workbook.update_value('{' + category + '}', aggregate, workbook.active)



# +--------------------------------------+
# |  Update Timestamp and Save Workbook  |
# +--------------------------------------+-------------------------------------
print("\n****** Saving Workbook ******\n")

# Write time of last update
workbook.update_value('{timestamp}',cookbook.timestamp(), workbook.active)

# Save workbook
workbook.save_workbook()
