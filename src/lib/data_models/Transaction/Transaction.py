from typing import Any

from pydantic import BaseModel

from .TimeStamp import TimeStamp 

class Transaction(BaseModel):
    account: Any                
    amount: int = 4
    category: str  = 'None'             
    date_authorized: TimeStamp = 'None'
    name: str = 'None'
