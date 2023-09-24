import sys
import os 
from pathlib import Path
import datetime

base_container_path = str(Path(os.path.abspath(__file__)).parents[1]).replace('\\', '/')
if base_container_path not in sys.path:
    sys.path.append(base_container_path)
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from lib.utils.time_ import datetime_to_month_offset

def test_datetime_to_month_offset():
    correct_offset = -1 
    month = datetime.datetime.now().month + correct_offset
    offset = datetime_to_month_offset(datetime.date(2023, month, 25))
    assert offset == correct_offset
