from typing import Optional, List, Any
import sys

from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime, date

from bunnet import Document, init_bunnet

# Add base container path
if "/finapp/src" not in sys.path:
    sys.path.append('/finapp/src')

from lib.data_models import Account, TimeStamp

class AccountODM(Account, Document):
    class Settings:
        name = 'Accounts'
        bson_encoders = {
          date: str
        }


if __name__ == '__main__':
    
     # Initialize MongoDB ORM: Bunnet
    client = MongoClient("mongodb://rootuser:rootpass@mongo:27017/")
    init_bunnet(database=client.testing_accounts_odm, document_models=[AccountODM]) # add documents here


    chase = AccountODM(name="Chase", subtype='something', balance = 24, last_updated=TimeStamp())
    print(TimeStamp())
    # t = AccountODM(chase)
    print(datetime(2023, 1, 1, 12))
    # t2.set_collection(collection)
    # t2.set_collection_name("testing_moreasdf")
    # print(t2.set_collection(collection))
    chase.save()
    results = AccountODM.find().to_list()
    print(len(results))
    for res in results:
        print(res)
