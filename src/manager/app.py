import os
import sys
from pathlib import Path
import logging

from flask import Flask, jsonify, request, Response
from bunnet import init_bunnet
import pymongo
import markupsafe

# Add base container path
if "/finapp/src" not in sys.path:
    sys.path.append('/finapp/src')

# from lib.utils import time_
# from manager import blueprint_transactions
# from manager.balances import blueprint_balances
# from manager import data_connector
from .blueprint_accounts import accounts_blueprint
from .blueprint_institutions import institutions_blueprint
from .blueprint_transactions import transactions_blueprint

# +---------------------+
# | Initialize App      |
# +---------------------+------------------------------------------------------

def create_app() -> Flask:
    app = Flask(__name__)
    # app.register_blueprint(blueprint_transactions)
    # app.register_blueprint(blueprint_balances)
    # Setup logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler=logging.FileHandler("/finapp/logs/manager.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    app.logger = logger

    # Initialize MongoDB ORM: Bunnet
    client = pymongo.MongoClient("mongodb://rootuser:rootpass@mongo:27017/")
    init_bunnet(database=client.db_name, document_models=[]) # add documents here

    return app

app = create_app()
app.logger.info(f"--- Starting Manager ---")

@app.before_request 
def before_request_callback(): 
    app.logger.info(f"Recieved {request.method}: {request.url}")

@app.after_request 
def after_request_callback( response ): 
    app.logger.info(f"Completed {request.method}: {request.url}")
    return response 

@app.errorhandler(Exception)
def handle_exception(e):
    # log the exception
    app.logger.exception('Exception occurred')
    app.logger.exception(e)
    # return a custom error page or message
    return "Error Occured"

@app.route('/')
def exists() -> Response:
    message = 'Manager Container is Running'
    app.logger.info(f"Returning: {message}")
    return message

if __name__ == "__main__":
    app.run(debug=True)