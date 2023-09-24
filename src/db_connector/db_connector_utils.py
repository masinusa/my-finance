import logging
import sys

# Add base container path
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from lib.utils.logger import setup_logger as _set_log

def setup_logger(name):
  return _set_log(name, 'db_connector')

    
