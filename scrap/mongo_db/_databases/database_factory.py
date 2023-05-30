
import pymongo

class Mongo_Database(pymongo.database.Database):

  def __init__(self, client: pymongo.MongoClient, name: str):
    super().__init__(client, name)
    self.name = name
    self.collections= []
    self.__post_init__()

  def __post_init__(self):
    # for c_name in self.list_collection_names():
    #   self.collections.append(load_Collection(c_name))
    pass

  # def list_collections(self):
  #   result = {}
  #   db_names = self.list_database_names()
  #   for db_name in db_names:
  #     names = self[db_name].list_collection_names()
  #     result[db_name] = names
  #   pass



DATABASES = {
  'transactions': None,
  'admin': None, 
  'config': None,
  'finapp': None,
  'local': None
}

def load_Database(name: str):
  return DATABASES[name]
    