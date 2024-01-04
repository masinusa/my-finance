from abc import ABC, abstractmethod
import sys
from pathlib import Path

if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from src.gui.categories.category import Category

class Takeout(Category):
    
    def __init__(self):
      self.name = self.__class__.__name__
      self.keywords = (
        'TST* LITTLE WILD THINGS F',
        'TST* Lucky Buns - Union M',
        'Uber Eats',
        'Cafe', 
        'Food', 
        'FOOD',
        "GLORIA'S",
        'TST* Call Your Mother - L',
        'BIG BEAR CAFE',
        'TST* The Red Hen',
        'SYLVAN CAFE',
        'SETTE OSTERIA - DUPONT',
        'COMMISSARY',
        'Potbelly Sandwich Shop',
        'CAFE 1919',
        'GOOD STUFF BURGERS',
        'UBER *GHOSTBURGER',
        'DC VEGAN',
        'SWEETGREEN LG',
        'TST* Taqueria Xochi',
        'STORE*EL CAMINO',
        'UBER * EATS PENDING'
        )
      self.omit_keywords = None
      self.additional_checks = None