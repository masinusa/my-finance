from abc import ABC, abstractmethod
import sys
from pathlib import Path

if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from src.gui.categories.category import Category

class Ignore(Category):
    
    def __init__(self):
      self.name = self.__class__.__name__
      self.keywords = ('Withdrawal Ach Type: Transfer Id: Discover Bank Dfi Acct: Xx99096 Ach Web Xfer',)
      self.omit_keywords = None
      self.additional_checks = (self.if_payment,)

    def if_payment(self, transact):
       checks = (
          transact['account'] == 'Alliant Credit Union' and transact['name'] == 'Venmo',
          transact['account'] == 'Aidvantage' and transact['name'] == 'Payment',
          transact['account'] == 'Chase' and transact['name'] == 'Payment Thank You - Web',
          transact['account'] == 'Chase' and transact['name'] == 'AUTOMATIC PAYMENT - THANK'
          )
       return any(checks)