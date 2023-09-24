import requests

import streamlit as st


# --- Plaid Container ---

st.title('PLAID CONTAINER')

def plaid_endpoint(path):
   return f'http://plaid:5000/{path}'

def _check_plaid_api_container():
    try:
      response = requests.get(plaid_endpoint(''), timeout=5)
      return response.text
    except Exception as e:
       return e

table = {"Plaid API Container": _check_plaid_api_container()}
st.table(table)

# Check Plaid Container is Running
plaid_get_token = st.button("Plaid - Get Public Token")
if plaid_get_token:
   st.write(f"Getting Plaid Public Token from: {plaid_endpoint('link_token')}")
   response = requests.get(plaid_endpoint('link_token'))
   st.write(response.text)

# Check Plaid Link re-authentication is working
st.markdown(f'''
<a href='http://localhost:5000/plaid_link'>
  <button style="background-color:Gray;">Plaid Re-Auth</button>
</a>''', unsafe_allow_html=True)

