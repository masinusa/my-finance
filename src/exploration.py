

import os
from dotenv import load_dotenv
import yaml
import plaid
import openpyxl as xl
import pymongo



os.system('pwd')
os.system('ls')

import cookbook 
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
_workbook_path = os.getcwd() + '/' + WORKBOOK


workbook = cookbook.Workbook(_workbook_path, CURRENT_TEMPLATE)

# +---------------+
# | Helpers  |
# +---------------+-------------------------------------------------------------

def last_transaction(access_t):
  return cookbook.get_transactions(access_t)[-2]


def print_transaction(transaction):
  cookbook.pretty_print_response(transaction)

def print_transaction_filtered(transaction):
  pass

# +---------------+
# | explore |
# +---------------+-------------------------------------------------------------
print(cookbook.remove_meta_document({'_id': 'curr_transaction_cursor'}))
print(cookbook.remove_meta_document({'_id': 'prev_transaction_cursor'}))
cookbook.print_meta()

print("removing all monthly transactions")
cookbook.rm_month_documents()
cookbook.print_collection_month()

# last_transaction = last_transaction(access_tokens['Discover'])

# print_transaction(last_transaction)
# for key in last_transaction.keys():
#   # print(key)
#   pass
# client = pymongo.MongoClient("mongodb://mongo_db:27017/")
# client.drop_database('customersdb')
# print(client.list_database_names())


# print(workbook.get_balance('access-development-c7111519-5691-488f-91af-2abb32cdc219'))

# # +----------------------------+
# # | Update Monthly Categories  |
# # +----------------------------+-------------------------------------------------------------
# # Update Living Expenses
# # Update Indulgences
# # Update Other

# # +--------------------------------------+
# # |  Update Timestamp and Save Workbook  |
# # +--------------------------------------+-------------------------------------------------------------

# # TODO: update timestamp
workbook.save_workbook()
