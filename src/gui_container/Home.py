
import os
from dotenv import load_dotenv

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

import sys
sys.path.append("/finapp/lib/")

from utils.time import curr_month_year
import my_plaid


from mongo_db import Mongo_Client

# +------------------------------+
# | Initialize Helpful Variables |
# +------------------------------+---------------------------------------------

# +-----------------------+
# | Load Landing Page     |
# +-----------------------+----------------------------------------------------

# Set up Sidebar
st.title('Welcome To Your Financial Cookbook')
show_curr_month = st.sidebar.button(f"Show Last Month's Finances: {curr_month_year()}")
show_last_month = st.sidebar.button(f"Show Last Month's Finances: {curr_month_year(-1)}")


# +---------------+
# | This Month    |
# +---------------+------------------------------------------------------------

  # st.write('this aint ritght')
  # month = curr_month_year(-4)
  # st.write(month)
  # transactions = Transactions(month)
  # db_names = transactions.client.list_database_names()
  # st.write(type(db_names))
  # collections = transactions.client.list_collection_names()
  # st.write(type(transactions.client['meta'].list_collection_names()))
  # st.write(transactions.client['meta'].list_collection_names())
  # st.write(collections)
  # st.table(collections)
# +---------------+
# | Last Month    |
# +---------------+------------------------------------------------------------
# if show_last_month:
#   # Set workbooks active sheet to this month
#   ws_month = utils.curr_month_year(-1)
#   workbook.active = workbook[ws_month]
#   # Convert active sheet to dataframe
#   st.write(workbook_path)
#   df = pd.DataFrame(workbook.active.values)
#   st.dataframe(df)

# +-------------------------+
# | 'Clothes Sizing' Button |
# +-------------------------+--------------------------------------------------
# if show_clothing_sizes:
#   list = mongo.print_collection("clothing_sizes")
#   st.write(list)
#   edit = st.button("Edit")
