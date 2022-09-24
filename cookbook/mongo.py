# Import 3rd Party
import pymongo

# Import Local
from . import utils

# Establish connection
client = pymongo.MongoClient("mongodb://mongo_db:27017/")
print("Connection to local database established")

# Save helpful paths
db = client['finapp']
c_meta = db['meta'] # collection 'meta'
c_month = db[utils.curr_month_year()] # collection of current month

# Enforce prev_transaction_cursor
if not c_meta.find_one(filter={"_id": "prev_transaction_cursor"}):
  print("prev_transaction_cursor not found... Initializing now...")
  c_meta.insert_one({"_id": 'prev_transaction_cursor', "value": ''})
# Enforce curr_transaction_cursor
if not c_meta.find_one(filter={"_id": "curr_transaction_cursor"}):
  print("curr_transaction_cursor not found... Initializing now...")
  c_meta.insert_one({"_id": 'curr_transaction_cursor', "value": ''})

def get_transaction_cursors():
  prev_cursor = c_meta.find_one(filter={"_id": "prev_transaction_cursor"})
  curr_cursor = c_meta.find_one(filter={"_id": "curr_transaction_cursor"})
  return prev_cursor['value'], curr_cursor['value']

def update_transaction_cursor(new_cursor):
  print("updating Transaction Cursor...")
  # Get Current Cursor
  cursor = c_meta.find_one(filter={"_id": "curr_transaction_cursor"})['value']
  if cursor == new_cursor:
    print("Cursor is already updated")
    return False

  # Update previous Cursor
  prev_cursor = cursor
  update_prev = { "$set": { "value": prev_cursor}}
  c_meta.update_one({ '_id':'prev_transaction_cursor'}, update_prev , upsert=True)
  # Update Current Cursor
  update_curr = { "$set": { "value": new_cursor }}
  c_meta.update_one({'_id':'curr_transaction_cursor'}, update_curr , upsert=True)
  return True

def log_transaction(squeezed_transaction):
  if c_month.find_one(filter={"_id": squeezed_transaction['_id']}):
    print("Transaction Already Logged: ", squeezed_transaction)
  else:
    c_month.insert_one(squeezed_transaction)

def print_meta():
  print("Printing Meta Collection...")
  # print(utils.pretty_print_response(c_month.find()))
  cursor = c_meta.find()
  for i, record in enumerate(cursor):
    print("record", i, ": ", record)

def remove_meta_document(filter):
  return c_meta.delete_one(filter)

def rm_month_documents():
  c_month.delete_many({})

def print_collection_month():
  print(f"Printing '{utils.curr_month_year()}' Collection...")
  # print(utils.pretty_print_response(c_month.find()))
  cursor = c_month.find()
  for i, record in enumerate(cursor):
    print("record", i, ": ", record)


