from typing import Any

from pydantic import BaseModel

from .TimeStamp import TimeStamp

# class Key(BaseModel):
#     value: str
#     last_updated: str

class Account(BaseModel):
    name: str
    subtype: str  
    balance: int
    last_updated: TimeStamp = TimeStamp()