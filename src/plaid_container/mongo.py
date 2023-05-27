import pymongo

# Initialize Mongo DB Client
client = pymongo.MongoClient("mongodb://rootuser:rootpass@mongo:27017/")

def get_access_token(bank_name: str) -> str:
    collection = client.plaidDB.bankTokens
    doc = collection.find_one({"bank_name": bank_name})
    return doc['access_token']

def set_access_token(access_token: str, bank_name: str) -> None:
    collection = client.plaidDB.bankTokens
    collection.update_one(
        {'bank_name': bank_name},
        {"$set":{"access_token": access_token,  'working': True}},
        upsert = True)