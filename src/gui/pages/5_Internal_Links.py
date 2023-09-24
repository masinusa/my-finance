import streamlit as st


st.markdown(f'''
    <a href='http://localhost:5000/plaid_link'><button style="background-color:Gray;">Plaid Re-Auth</button></a>
    ''',
    unsafe_allow_html=True)


st.markdown(f'''
    <a href='http://localhost:8081'><button style="background-color:Gray;">DB Admin</button></a>
    ''',
    unsafe_allow_html=True)