import requests
import sys
import os 
from pathlib import Path
import logging

import streamlit as st

base_container_path = str(Path(os.path.abspath(__file__)).parents[1]).replace('\\', '/')
if base_container_path not in sys.path:
    sys.path.append(base_container_path)
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from lib.mongo import mongo
from lib import utils
# from breakdown.breakdown import Breakdown
import gui_utils

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler=logging.FileHandler("/finapp/logs/gui.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# Set up Sidebar
st.title('Welcome To Your Financial Cookbook')
