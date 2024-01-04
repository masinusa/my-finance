from abc import ABC, abstractmethod
import sys
from pathlib import Path

if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from src.gui.categories.category import Category

class Transportation(Category):
    
    def __init__(self):
      self.name = self.__class__.__name__
      self.keywords = (
        'CAPBIKE*1 RIDE',
        'CAPBIKE*TEMP HOLD',
        'CAPBIKE*2 RIDES',
        'LIM*RIDE COST',
        'Uber',
        'METRO 095-FRNCNIA-SPRING'
        )
      self.omit_keywords = (
         ('Uber Eats',)
      )
      self.additional_checks = None