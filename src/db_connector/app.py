import os
import sys
from pathlib import Path
import logging

from flask import Flask, jsonify, request, Response
import pymongo

# Add base container path
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from lib.utils import time_
from balancesdb_blueprint import balancesdb_blueprint
from plaiddb_blueprint import plaiddb_blueprint
# +---------------------+
# | Initialize App      |
# +---------------------+------------------------------------------------------

def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(balancesdb_blueprint)
    app.register_blueprint(plaiddb_blueprint)
    # Setup logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler=logging.FileHandler("/finapp/logs/db_connector.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    app.logger = logger

    # Initialize Mongo DB Client
    app.client = pymongo.MongoClient("mongodb://rootuser:rootpass@mongo:27017/")

    return app

app = create_app()
app.logger.info(f"--- Starting DB Connector ---")

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
    app.logger.exception(f'Exception occurred in Controller')
    # return a custom error page or message
    return "Error Occured", 500

@app.route('/')
def exists() -> Response:
    return 'DB_Connector Container is Running'

if __name__ == "__main__":
    app.run(debug=True)
