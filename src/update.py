
# Standard Library Imports
import os
import re
from dotenv import load_dotenv
import calendar

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

# Load access tokens for each bank
access_tokens = secrets.access_tokens

# +----------------------------+
# | Update Transactions        |
# +----------------------------+-------------------------------------------------------------
print("\n****** Saving New Transactions ******\n")
# print("--- Saving Recent Transactions ---")
# cookbook.print_meta()

# Get most recent transactions
new_cursor, raw_transactions = cookbook.get_transactions(
                                         access_tokens['Discover'], 
                                         cookbook.get_transaction_cursors()[1])

# Save new transaction cursor
cookbook.update_transaction_cursor(new_cursor)

# Log each transaction in the database
for i, raw_transaction in enumerate(raw_transactions):
  print(f"Logging transaction {i}: ", end = '')
  transaction = cookbook.squeeze_transaction(raw_transaction)
  date = transaction['date_authorized']
  if date == None:
    cookbook.log_transaction(transaction)
  else:
    split_date = re.split("/|\(", date)
    month = calendar.month_abbr[int(split_date[0])]
    year = split_date[2]
    date = f"{month} {year}"
    cookbook.log_transaction(transaction, collection_name=date)
  print(f" in {date}")
cookbook.print_collection_month()
