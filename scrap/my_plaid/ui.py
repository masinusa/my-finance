import streamlit as st
import configparser
import streamlit.components.v1 as components

from my_plaid import plaid_actions, plaid_link

def _state_check():
  if ('accessible_banks' not in st.session_state
     or 'inaccessible_banks' not in st.session_state):
    st.session_state['accessible_banks'] = []
    st.session_state['inaccessible_banks'] = []

# def _initiate_link(bank):
#   st.title(f"Initialize Link with {bank}")
#   Link_HTML_Javascript = '<script src="https://cdn.plaid.com/link/v2/stable/link-initialize.js"></script>'
#   st.write("Loading")
#   practice_js="""
#   <html>
#   <body>

#   <h2>Demo JavaScript in Body</h2>

#   <p id="demo">A Paragraph</p>

#   <button type="button" onclick="myFunction()">Try it</button>

#   <script src="https://cdn.plaid.com/link/v2/stable/link-initialize.js">
#   </script>

#   </body>
#   """

def initiate_link(bank):
  st.write("hello")

  st.title('Initiating Bank: ', bank)
  link_token = plaid_link.create_link_token()['link_token']
  st.write("Public Link Token: ", link_token)
  st.write("Access Token: ", plaid_link.get_access_token(link_token))
  st.write("Doing Javascript")
  practice=f"""
  <html>
  <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.3/jquery.min.js"></script>
  </head>
  <body>
    <script src="https://cdn.plaid.com/link/v2/stable/link-initialize.js"></script>
    <script>
      (($) => {{
        
        const linkToken = {link_token};

        const handler = Plaid.create({{
          token: linkToken,
          receivedRedirectUri: window.location.href,
          onSuccess: async (publicToken, metadata) => {{
            await fetch("/api/exchange_public_token", {{
              method: "POST",
              body: JSON.stringify({{ public_token: publicToken }}),
              headers: {{
                "Content-Type": "application/json",
              }},
          }});
            const response = await fetch('/api/data', {{
              method: 'GET',
            }});
            const data = await response.json();
            window.location.href = "http://localhost:8080";          
          }},
          onEvent: (eventName, metadata) => {{
            console.log("Event:", eventName);
            console.log("Metadata:", metadata);
          }},
          onExit: (error, metadata) => {{
            console.log(error, metadata);
          }},
        }});

        handler.open();
      }})(jQuery);
    </script>
  </body>
  </html>
  """
  practice1=f"""
  <html>
  <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.3/jquery.min.js"></script>
  </head>
  <body>
    <script src="https://cdn.plaid.com/link/v2/stable/link-initialize.js"></script>
    <script>
      (($) => {{
        
        const linkToken = {link_token};S

        const handler = window.open("https://www.w3schools.com");
        handler.open();
      }})(jQuery);
    </script>
  </body>
  </html>
  """
  components.html(practice1)


def update_state():
  _state_check()
  config = configparser.ConfigParser()
  config.read('my_plaid/secrets.ini')
  
  st.session_state['accessible_banks'] = []
  st.session_state['inaccessible_banks'] = [] 

  for bank, access_token in config['PLAID_ACCESS_TOKENS'].items():
    try:
      plaid_actions.get_balance(access_token)
      st.session_state['accessible_banks'].append(bank)
    except:
      st.session_state['inaccessible_banks'].append(bank)

def show():
  

  # Check which banks are currently logged in
  _state_check()
  left_col, right_col = st.columns(2)
  left_col.header("Already Logged In")
  right_col.header("Need to Update Credentials")

  # List what banks are already logged in
  for bank in st.session_state['accessible_banks']:
    left_col.write(bank)

  # Create a button for banks not currently logged in
  for bank in st.session_state['inaccessible_banks']:
    url = 'http://localhost:5000'
    st.markdown(f'''
    <a href={url}><button style="background-color:GreenYellow;">Plaid Link</button></a>
    ''',
    unsafe_allow_html=True)
    right_col.button(bank, on_click=initiate_link, args=(bank,) )







