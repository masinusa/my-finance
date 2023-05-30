
from mongo_db.collections_.Collection import Collection
from plaid_ import Transaction
from utils.time import curr_month_year


class Transactions():
  """
  Transactions Class
  """
  def __init__(self, month_year: str):
    self.collection = self.client[month_year]
    self.__post_init__()

  def __post_init__(self):
    # Save helpful paths
    db = self.client['finapp']
    c_meta = db['meta'] # collection 'meta'
    self.transactions_collection = db[curr_month_year()] # collection of current month

    # Enforce prev_transaction_cursor exists for plaid transaction API
    if not c_meta.find_one(filter={"_id": "prev_transaction_cursor"}):
      print("prev_transaction_cursor not found... Initializing now...")
      c_meta.insert_one({"_id": 'prev_transaction_cursor', "value": ''})
    # Enforce curr_transaction_cursor exists for plaid transaction API
    if not c_meta.find_one(filter={"_id": "curr_transaction_cursor"}):
      print("curr_transaction_cursor not found... Initializing now...")
      c_meta.insert_one({"_id": 'curr_transaction_cursor', "value": ''})

  def add_transaction(transaction: Transaction) -> None:
    pass

  def print_collection(self) -> list:
    result = []
    for document in self.transactions_collection.find({}, {"_id":0, "coursename": 1, "price": 1 }):
      result.append(document)
    return result