import requests
import sys
import os 
from pathlib import Path
import logging
from urllib3.exceptions import NewConnectionError

import pandas as pd

import streamlit as st

base_container_path = str(Path(os.path.abspath(__file__)).parents[1]).replace('\\', '/')
if base_container_path not in sys.path:
    sys.path.append(base_container_path)
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')


from lib.mongo import mongo
from lib import utils
from breakdown import Breakdown
import gui_utils
from categories.directory import load_categories




# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler=logging.FileHandler("/finapp/logs/gui.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# +---------------+
# | Setup Sidebar |
# +---------------+---------------------------------

# Choose month
with st.sidebar:
    month_offset = gui_utils.choose_month_widget()
    update = st.button("update balances")
    # +----------------------------+
    # | Update Balances (in sidebar) |
    # +----------------------------+---------------------------------
    if update:
        with st.spinner('Updating Balances...'):
            try:
                resp_status = requests.put('http://manager:5000/balances/update', 
                                       params={"month_offset": month_offset}, timeout=30)
                resp_status = resp_status.json()
            except requests.exceptions.JSONDecodeError as e:
                try: st.warning(resp_status.text)
                except:
                    st.error(f"No JSON or text recieved. Status Code: {resp_status.status_code}")
                    st.error(e)
                    sys.exit()
                sys.exit()
        
        success_count = len([x for x in resp_status['institutions'] if x['code'] == 200 ])
        st.success(f"Updated {success_count}/{len(resp_status['institutions'])}")
        if resp_status != 200:
            for institution in [x for x in resp_status['institutions'] if x['code'] != 200]:
                st.write(f"Failed to retrieve {institution['institution']}")
        # st.write('resp_status:')
        # st.write(resp_status)

    
# +------------------+
# | Request Balances |
# +------------------+------------------------------------------------
# Request balances
try: 
    logger.info("Requesting Balances")
    balances = requests.get('http://manager:5000/balances/', params={"month_offset": month_offset}, timeout=10)
except requests.exceptions.ConnectionError as e:
    st.error("Connection Error: check requesting url")
    sys.exit(e)
except Exception as e:
    st.error(f"Unkown Error: {type(e)}")
    sys.exit()

if balances.status_code == 200:
    try: 
        balances = balances.json()
    except requests.exceptions.JSONDecodeError as e:
        st.error("Did not receive JSON decodable object. Check Manager")
        st.write("Recieved: ")
        st.write(balances)
        sys.exit()
    except Exception as e:
        st.error(f"Unkown Error: {type(e)}")
        sys.exit()
    logger.info("Received Balances: {balances}")
else:
    st.error(f"Recieved non-200 response code: {balances.status_code}")

# +------------------+
# |  Show Balances   |
# +------------------+---------------------------------------------------
# Tally total balance
total = 0
for balance in balances:
    total += float(balance['balance'])
total = '{:,.2f}'.format(total)

# Print Total Balance
st.title(f"Balance: ${total}")

# Print Individual Balances
st.table(balances)

