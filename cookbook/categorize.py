
def categorize(transaction):
  name = transaction['name']
  date = transaction['date_authorized']
  amount = transaction['amount']
  category = ''
  if 'THE ROUNDS REFI' in name:
    category = 'the_rounds'
  else:
    category = 'unkown'
  transaction['category'] = category
  return category