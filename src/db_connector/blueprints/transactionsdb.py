import sys
import os 
from pathlib import Path
import json

import requests
import flask
from flask import Blueprint, current_app, request

# Add base container path
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')


from lib.utils import time_


def _cur_month_collection(offset: int = 0):
    curr_m_y = time_.curr_month_year_int(relative_month=offset)
    return current_app.client.transactionsDB[curr_m_y]

# Create Flask Blueprint
transactionsdb_blueprint = Blueprint('transactionsdb', __name__)

@transactionsdb_blueprint.route('/database/transactions/', methods=['GET'])
def get_transactions():
    """  Gets Logged Transactions """
    month_offset = int(request.args.get('month_offset'))
    result = [t for t in _cur_month_collection(offset = month_offset).find({})]
    current_app.logger.debug(f"Returning: {result}")
    return flask.jsonify(result)

@transactionsdb_blueprint.route('/database/transactions/', methods=['PUT'])
def set_transactions():
    """ Set transactions into database 
    
    Params: 
        month_offset, int describing month to log transactions under
        transactions, JSON list containing transaction json string
    """
    transactions = json.loads(flask.request.json)
    col = _cur_month_collection(offset = int(request.args['month_offset']))
    current_app.logger.debug(f"Recieved: {transactions}")
    current_app.logger.debug(type(transactions))
    for t in transactions:
        col.update_one(
            {"_id": t['_id']},
            {"$set":t},
            upsert = True)
    return "Success", 200

# @balancesdb_blueprint.route('/database/balances/', methods=['GET'])
# def get_balancesdb():
#     """  Gives a month's last recorded total balances. 

#     """
#     month_offset = request.args.get('month_offset')
#     month_offset = int(month_offset)
#     cursor = _cur_month_collection(offset = month_offset).find({'institution': {"$exists":True}})
#     # Parse result for each document returned
#     results = []
#     for document in cursor:
#         doc_dict = {"_id": str(document["_id"]),
#                     "balance": document["balance"],
#                     "institution": document["institution"],
#                     "last_updated": document["last_updated"],
#                     "subtype": document["subtype"],
#         }
#         results.append(doc_dict)
#     return json.dumps(results)


# @balancesdb_blueprint.route('/database/balances/update', methods=['PUT'])
# def update_balancesdb():
#     json_data = json.loads(request.json)
#     current_app.logger.debug(f"Received JSON: {json_data}")
#     current_app.logger.debug(f"of type: {type(json_data)}")
#     current_app.logger.debug(f"of type: {int(request.args['month_offset'])}")
#     current_app.logger.debug(f"of type: {type(int(request.args['month_offset']))}")
#     _cur_month_collection(offset = int(request.args['month_offset'])).update_one(
#         {"institution": json_data['institution']},
#         {"$set":{
#             # "_id": id,
#             "institution": json_data['institution'],
#             "account": json_data['account'],
#             "balance": json_data['balance'],
#             "subtype": json_data['subtype'],
#             'last_updated': time_.timestamp()}},
#         upsert = True)

#     return '', 200