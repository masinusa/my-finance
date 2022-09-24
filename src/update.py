
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
  print(f"Logging transaction {i}:")
  transaction = cookbook.squeeze_transaction(raw_transaction)
  # cookbook.categorize(transaction)
  cookbook.log_transaction(transaction)

cookbook.print_collection_month()
