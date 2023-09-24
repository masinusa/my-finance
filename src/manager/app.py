import os
import sys
from pathlib import Path
import logging

from flask import Flask, jsonify, request, Response

# Add base container path
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from lib.utils import time_
from transactions.transactions_blueprint import transactions_blueprint
from balances.balances_blueprint import balances_blueprint

# +---------------------+
# | Initialize App      |
# +---------------------+------------------------------------------------------

def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(transactions_blueprint)
    app.register_blueprint(balances_blueprint)
    # Setup logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler=logging.FileHandler("/finapp/logs/manager.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    app.logger = logger

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
    app.logger.execption(e)
    # return a custom error page or message
    return "Error Occured"

@app.route('/')
def exists() -> Response:
    message = 'Manager Container is Running'
    app.logger.info(f"Returning: {message}")
    return message

if __name__ == "__main__":
    app.run(debug=True)