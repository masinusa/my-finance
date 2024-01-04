# from typing import Optional, List, Any
# import sys

# from pymongo import MongoClient
# from pydantic import BaseModel
# from datetime import datetime, date

# from bunnet import Document, init_bunnet

# # Add base container path
# if "/finapp/" not in sys.path:
#     sys.path.append('/finapp')

# from lib.data_models import Balance, TimeStamp

# class BalanceODM(Balance, Document):


#     class Settings:
#         name = 'Balances'
#         bson_encoders = {
#           date: str
#         }


# if __name__ == '__main__':
#      # Initialize MongoDB ORM: Bunnet
#     client = MongoClient("mongodb://rootuser:rootpass@mongo:27017/")
#     init_bunnet(database=client.therealdeal, document_models=[BalanceODM]) # add documents here


#     chase = Account(name="Chase", parent_item= "chase_bank")
#     print(TimeStamp())
#     bal = BalanceODM(account=chase, amount=9, category= 'N/A', date_authorized=TimeStamp(dt="2024-10-17"), name='volo1')
#     print(datetime(2023, 1, 1, 12))
#     # t2.set_collection(collection)
#     # t2.set_collection_name("testing_moreasdf")
#     # print(t2.set_collection(collection))
#     t.save()
#     results = TransactionODM.find().to_list()
#     print(len(results))
#     for res in results:
#         print(res)
