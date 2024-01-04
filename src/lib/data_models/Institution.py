from typing import Any, List

from pydantic import BaseModel

from .TimeStamp import TimeStamp
from .Account import Account

class _DataValue(BaseModel):
    value: str
    last_updated: str

class Institution(BaseModel):
    institution: str
    access_token: _DataValue
    transaction_cursor: _DataValue
    accounts = List[Account]
