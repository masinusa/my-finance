from abc import ABC, abstractmethod
import sys
from pathlib import Path

if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from src.gui.categories.category import Category

class Income(Category):
    
    def __init__(self):
      super().__init__()
      self.name = self.__class__.__name__
      self.keywords = (
         'Deposit Ach Deloitte Consult Type: Payrll Dep Id: 1061454513 Data: Employees Co: Deloitte Consult',
          'Deposit Dividend Annual Percentage Yield Earned',)
      self.omit_keywords = None