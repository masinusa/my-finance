from abc import ABC, abstractmethod
import sys
from pathlib import Path

if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from src.gui.categories.category import Category

class Groceries(Category):
    
    def __init__(self):
      self.name = self.__class__.__name__
      self.keywords = (
        "Trader Joe's",
        "Harris Teeter Supermarkets, Inc.",
        "DC MINI SUPERMARKET"
        )
      self.omit_keywords = None