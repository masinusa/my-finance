from abc import ABC, abstractmethod
import sys
from pathlib import Path

if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from src.gui.categories.category import Category

class Athletics(Category):
    
    def __init__(self):
      self.name = self.__class__.__name__
      self.keywords = (
        'VOLO* SPORTS LEAGUES',
        'TOTAL SOURCE FITNESS',
        'VOLO* SPORTS LEAGUES',
        'VOLO PASS SUBSCRIPTION'
        )
      self.omit_keywords = None