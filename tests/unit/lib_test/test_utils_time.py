import sys
import os 
from pathlib import Path
from datetime import datetime, date

base_container_path = str(Path(os.path.abspath(__file__)).parents[1]).replace('\\', '/')
if base_container_path not in sys.path:
    sys.path.append(base_container_path)
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from lib.utils.time_ import datetime_to_month_offset, TimeStamp

def test_datetime_to_month_offset():
    correct_offset = -1 
    month = datetime.now().month + correct_offset
    offset = datetime_to_month_offset(date(2023, month, 25))
    assert offset == correct_offset

def test_TimeStamp_class():
    now = datetime.now().strftime("%Y-%m-%d")
    tstamp = TimeStamp()
    assert now == tstamp.str

    tstamp = TimeStamp(dt="2023-01-01")
    assert "2023-01-01" == str(tstamp)
    assert 1 == tstamp.month


if __name__ == '__main__': 
    test_TimeStamp_class()