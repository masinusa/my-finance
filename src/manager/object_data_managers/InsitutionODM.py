from typing import Optional, List, Any
import sys
from lib.data_models.Transaction import Transaction

from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime, date

from bunnet import Document, init_bunnet

from lib.data_models import Institution, TimeStamp

class InsitutionODM(Institution, Document):

    class Settings:
        name = 'Institutions'
        bson_encoders = {
          date: str
        }
