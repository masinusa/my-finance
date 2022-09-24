
def categorize(transaction):
  name = transaction['name']
  date = transaction['date_authorized']
  amount = transaction['amount']
  category = ''
  if 'THE ROUNDS REFI' in name:
    category = 'the_rounds'
  elif 'Uber Eats' in name:
    category = 'takeout'
  elif 'UBER BUSBOYSA' in name:
    category = 'takeout'
  elif 'TOTAL SOURCE FI' in name:
    category = 'gym'
  elif 'ACH Withdrawal PEPCO PAYMENTUS BILLPAY' in name:
    category = 'electricity'
  elif 'VOLO SPORT* SPO' in name:
    category = 'volo'
  elif 'NNT MICROSOFT*X'in name:
    category = 'videogames'
  else:
    category = 'unknown'
  transaction['category'] = category
  return category