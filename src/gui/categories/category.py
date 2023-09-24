from abc import ABC, abstractmethod, abstractproperty
import requests
import sys
import os 
from pathlib import Path
from typing import Union
import logging

if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from lib.mongo import mongo
from lib import utils


# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler=logging.FileHandler("/finapp/logs/mongo_debug.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class Category(ABC):
    
    def __init__(self):
      self.name = None
      self._keywords = None
      self._omit_keywords = None

    @property
    def keywords(self):
       return self._keywords

    @property
    def omit_keywords(self):
       return self._omit_keywords

    @keywords.setter
    def keywords(self, value):
      if not (isinstance(value, (list, tuple)) or value is None):
          raise TypeError(f"keywords for {self.name} must be a iterable or None")
      else:
         self._keywords = value
      
    @omit_keywords.setter
    def omit_keywords(self, value):
      if not (isinstance(value, (list, tuple)) or value is None):
          raise TypeError(f"omit_keywords for {self.name} must be a iterable or None")
      else:
         self._omit_keywords = value

    def _keyword_match(self, transaction) -> bool:
      logger.debug(f"Inside Category: {self.name.__str__()}")
      logger.debug(f"Keywords: {self.keywords.__str__()}")
      # Check Keywords
      if_keyword = False
      if self.keywords is not None:
        if_keyword = any([(keyword in transaction['name']) for keyword in self.keywords])
      # Check Omit_Keywords
      if_omit_keyword = False
      if self.omit_keywords is not None:
          if_omit_keyword = any([(keyword in transaction['name']) for keyword in self.omit_keywords])
      if if_omit_keyword:
         logger.debug(f"Found Omitted Keyword in {transaction['name'].__str__()}")
      return (if_keyword and not if_omit_keyword)
         
    def check(self, transaction) -> bool:
      return self._keyword_match(transaction)