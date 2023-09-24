import logging

import pymongo

from .. import utils



# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler=logging.FileHandler("/finapp/logs/mongo_debug.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# Initialize Mongo DB Client
client = pymongo.MongoClient("mongodb://rootuser:rootpass@mongo:27017/")

# +----------+
# | PlaidDB |
# +----------------------------------------------------------------------------
bankTokens = client.plaidDB.bankTokens
transactionCursors = client.plaidDB.transactionCursors

def get_access_token(bank_name: str) -> str:
    doc = bankTokens.find_one({"bank_name": bank_name})
    return doc['access_token']

def set_access_token(access_token: str, bank_name: str, working: bool = True) -> None:
    bankTokens.update_one(
        {'bank_name': bank_name},
        {"$set":{"access_token": access_token,  
                 'working': working, 
                 'last_updated': utils.time_.timestamp()}},
        upsert = True)

def get_access_tokens() -> list:
    """ Retrieves all access_tokens from PlaidDB database"""
    result = [bank for bank in bankTokens.find({})]
    return result

def get_transaction_cursor(bank_name: str):
    doc = transactionCursors.find_one({'bank_name': bank_name})
    if doc:
        return doc['transaction_cursor']
    else:
        return ''

def set_transaction_cursor(bank_name: str, cursor:str):
    transactionCursors.update_one(
    {"bank_name":bank_name},
    {"$set":{"transaction_cursor": cursor,  
             'last_updated': utils.time_.timestamp()}},
    upsert = True)

# +------------+
# | balancesDB |
# +----------------------------------------------------------------------------
def cur_month_collection(offset: int = 0):
    curr_m_y = utils.time_.curr_month_year_int(relative_month=offset)
    return client.balancesDB[curr_m_y]

def set_institution_balance(institution: str, account: str, balance: int, subtype: str, month_offset: int = 0):
    cur_month_collection(offset = month_offset).update_one(
    {"institution": institution},
    {"$set":{"id_": id,
             "institution": institution,
             "account": account,
             "balance": balance,
             "subtype": subtype,
             'last_updated': utils.time_.timestamp()}},
    upsert = True)

def get_balances(month_offset: int = 0):
    return cur_month_collection(offset = month_offset).find({'institution': {"$exists":True}})

def get_total_month_balance(month_offset: int = 0):
    return cur_month_collection(offset = month_offset).find_one({'total_balance': {"$exists":True}})

# +----------------+
# | transactionsDB |
# +----------------------------------------------------------------------------
def _cur_transactions_collection(offset: int = 0):
    curr_m_y = utils.time_.curr_month_year_int(relative_month=offset)
    return client.transactionsDB[curr_m_y]

def get_transactions(category: str = None, month_offset: int = 0):
    try:
        if category:
            return _cur_transactions_collection(offset = month_offset).find({'category': category})
        else:
            return _cur_transactions_collection(offset = month_offset).find({})

    except Exception as e:
        logger.debug(f"Set Transaction failed: {str(e)}")
        raise Exception(e)

def set_transaction(transaction):
    try:
        month_offset = utils.time_.month_offset(transaction['date_authorized'])
        _cur_transactions_collection(offset = month_offset).update_one(
        {'_id': transaction['_id']},
        {"$set":transaction},
        upsert = True)
    except Exception as e:
        logger.debug(f"Set Transaction failed: {str(e)}")
        raise Exception(e)
