
import pymongo
import pandas as pd

from mongo_db._databases.database_factory import load_Database



# _______________ Init ___________________

""" PyMongo Client """
client = pymongo.MongoClient("mongodb://rootuser:rootpass@mongo:27017/")

""" Load Databases """
_databases = []
for db in client.list_databases():
  _databases.append(db)

# __________________ Methods ___________________
def list_databases():
  return client.list_databases