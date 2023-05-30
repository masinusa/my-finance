

class Transaction():
  """
  {
    "_id": self.transaction["transaction_id"],
    "date_authorized": date_time,
    "name": self.transaction["name"],
    "amount": self.transaction["amount"],
    "category": "N/A
  }
  """
  def __init__(self, plaid_transact: str):
    self._id = plaid_transact['transaction_id']
    self.name = plaid_transact['name']
    self.amount = plaid_transact['amount']
    self.category = 'N/A'
    date_time = plaid_transact['authorized_datetime']
    self.date_authorized = date_time if None else date_time.strftime("%m/%d/%Y(%H:%M)")