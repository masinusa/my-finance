
import sys
from pathlib import Path
import os
from collections import OrderedDict
import logging

import streamlit as st

base_container_path = str(Path(os.path.abspath(__file__)).parents[1]).replace('\\', '/')
if base_container_path not in sys.path:
    sys.path.append(base_container_path)
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from lib import utils


def choose_month_widget(m_range: int = 5):
    m_range = (-1*m_range +1, 1)
    months = dict([(utils.time_.curr_month_year(relative_month=offset), offset) for offset in range(*m_range)])
    month_keys = []
    for key in months.keys():
        month_keys.append(key)
    month_keys.reverse()

    month = st.selectbox('Month', month_keys)
    month_offset = months[month]
    return month_offset
    
def setup_logger(name):
    logger = logging.getLogger(name)
    if sum([isinstance(handler, logging.FileHandler) for handler in logger.handlers]):
        logger.setLevel(logging.DEBUG)
        handler=logging.FileHandler("/finapp/logs/gui.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def dollars(val, omit_sign=False):
    result = f"{'{:,.2f}'.format(val)}"
    if omit_sign: 
        return  result
    else: 
        return '$' + result