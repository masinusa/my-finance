
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
# TODO: Only update certain things when a file was modified
# TODO: Check what happens if more than 26 columns and ASCII diverges from excel column names

# +------+
# | Prep |
# +------+-------------------------------------------------------------
# Load Environment Variables
load_dotenv('.env')
CURRENT_TEMPLATE= os.environ.get("CURRENT_TEMPLATE")
PLAID_CLIENT_ID = secrets.PLAID_CLIENT_ID
PLAID_SECRET = secrets.PLAID_SECRET
WORKBOOK = os.environ.get("WORKBOOK")

# Initalize Helpful Variables
_workbook_path = '/finapp/' + WORKBOOK

access_tokens = secrets.access_tokens

# +---------------+
# | Load Workbook |
# +---------------+-------------------------------------------------------------

workbook = cookbook.Workbook(_workbook_path, CURRENT_TEMPLATE)

# +---------------+
# | Load Context |
# +---------------+-------------------------------------------------------------
# Set current worksheet to this month by default
ws = cookbook.curr_month_year()
workbook.active = workbook[ws]


# +------------------+
# | Enforce Template |
# +------------------+-------------------------------------------------------------
# Save all current values
curr_values = workbook.sheet_values(ws)
# Enforce the template
workbook.copy_template(workbook._load_sheet(ws), workbook._load_template(CURRENT_TEMPLATE))
# Repopulate values with enforced template
for key, value in curr_values.items():
  workbook.update_value(key, value, workbook._load_sheet(ws), workbook._load_template(CURRENT_TEMPLATE))

# +------------------+
# | Update Timestamp |
# +------------------+-------------------------------------------------------------
workbook.update_value('{timestamp}',cookbook.timestamp(), workbook.active)
# +----------------------------+
# | Update Total Balance |
# +----------------------------+-------------------------------------------------------------
# print(workbook.sheet_values(ws))
workbook.update_value('{total}', cookbook.calculate_total(access_tokens), workbook.active)
# print(workbook.sheet_values(ws))

# +----------------------------+
# | Update Monthly Categories  |
# +----------------------------+-------------------------------------------------------------
print("****** Updating Monthly Categories ******")
print("--- Categorizing and Saving Recent Transactions ---")
cookbook.print_meta()
new_cursor, raw_transactions = cookbook.get_transactions(
                                         access_tokens['Discover'], 
                                         cookbook.get_transaction_cursors()[1])
cookbook.update_transaction_cursor(new_cursor)
# print("transactions: ", transactions)
for i, raw_transaction in enumerate(raw_transactions):
  print(f"Logging transaction {i}:")
  transaction = cookbook.squeeze_transaction(raw_transaction)
  cookbook.categorize(transaction)
  cookbook.log_transaction(transaction)
cookbook.print_collection_month()
# cookbook.print_curr_collection()
# cookbook.update_transaction_cursor(cursor)
# cookbook.print_curr_collection()

print("--- Tallying Category Totals ---")



# cookbook.log_transaction(transactions)
# print(curr_cursor)
# cursor, transactions = cookbook.get_transactions()

# Update Living Expenses
# Update Indulgences
# Update Other

# +--------------------------------------+
# |  Update Timestamp and Save Workbook  |
# +--------------------------------------+-------------------------------------------------------------

# TODO: update timestamp
workbook.save_workbook()
