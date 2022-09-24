from cookbook import plaid_retrievals

def calculate_total(access_tokens):
  total = 0
  for account, token in access_tokens.items():
    try: 
      response = plaid_retrievals.get_balance(token)
      response = response['accounts'][0]['balances']['current']
      total += response
    except:
      error = response['error']
      print(f"***{account}***")
      print(error['error_code'])
      print(error['display_message'])
  return total