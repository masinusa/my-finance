from flask import Flask, render_template, jsonify, request
import configparser

import sys
import pymongo

sys.path.append("/finapp/lib/")
import my_plaid

app = Flask(__name__)

# Initialize Mongo DB Client
""" PyMongo Client """
client = pymongo.MongoClient("mongodb://rootuser:rootpass@mongo:27017/")


config = configparser.ConfigParser()
configsrc = '/finapp/src/secrets.ini'
config.read(configsrc)


# Get latest Public Link token
token = my_plaid.plaid_link.create_link_token()['link_token']
config['PUBLIC_LINK_TOKEN'] = {'token': token}


# Check previously logged in banks
accessible_banks = []
inaccessible_banks = []
for bank, access_token in config['PLAID_ACCESS_TOKENS'].items():
    response = my_plaid.plaid_actions.get_balance(access_token)
    if 'error' in response:
      config.remove_option('PLAID_ACCESS_TOKENS', bank)
      config['OUT_OF_DATE'] = {bank: 'None'}
    else:
        accessible_banks.append(bank)
for bank in config['OUT_OF_DATE'].keys():
    inaccessible_banks.append(bank)

# Save Config File
with open(configsrc, 'w') as configfile:
  config.write(configfile)

@app.route('/')
def hello_geek():
    return render_template('index.html', token = token, acc_banks=accessible_banks, inacc_banks=inaccessible_banks)



@app.route('/token', methods=['GET', 'POST'])
def token_api():
    # GET request
    if request.method == 'GET':
        message = {'token':token}
        return jsonify(message)  # serialize and use JSON headers
    # POST request
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return 'Sucesss', 200


if __name__ == "__main__":
    app.run(debug=True)