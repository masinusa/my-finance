from abc import ABC, abstractmethod
import requests
import sys
import os 
from pathlib import Path
from typing import Union

if "/finapp/" not in sys.path:
    sys.path.append('/finapp')


from src.gui.categories import index

def load_categories():
    return [val()  for key, val in index.__dict__.items() if key[0:2] != '__']

if __name__ == '__main__':
    load_categories()