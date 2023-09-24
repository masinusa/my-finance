from abc import ABC, abstractmethod
import sys
from pathlib import Path

if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from src.gui.categories.category import Category

class Other(Category):
    
    def __init__(self):
      super().__init__()
      self.name = self.__class__.__name__
      self.keywords = None
      self.omit_keywords = None