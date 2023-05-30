import logging

from . import mongo

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler=logging.FileHandler("/finapp/logs/mongo_debug.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)




category_keywords = {
    'Income': ('Deposit Ach Deloitte Consult Type: Payrll Dep Id: 1061454513 Data: Employees Co: Deloitte Consult',
               'Deposit Dividend Annual Percentage Yield Earned'),
    'Transportation': ('Uber',),
    'Utilities': ('ACH Withdrawal PEPCO PAYMENTUS BILLPAY',
                  'VERIZON*RECURRI'),
    'The Rounds': ('THE ROUNDS REFI',)
}


def sort_uncategorized():
  transactions = mongo.get_transactions(category='N/A', month_offset=0)
  for t in transactions:
      for category, keywords in category_keywords.items():
        if any([(keyword in t['name']) for keyword in keywords]):
          t['category'] = category
          mongo.set_transaction(t, month_offset=0)

def reset_categories():
    transactions = mongo.get_transactions(category={ "$ne": 'N/A' }, month_offset=0)
    for t in transactions:
      t['category'] = 'N/A'
      mongo.set_transaction(t, month_offset=0)