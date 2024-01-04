import sys
import os 
from pathlib import Path
import json

import requests
import flask
from flask import Blueprint, current_app

# Add base container path
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')


from lib.utils import time_

# Create Flask Blueprint
plaiddb_blueprint = Blueprint('plaiddb', __name__)

@plaiddb_blueprint.route('/database/transaction_cursors/', methods=['GET'])
def get_t_cursors():
    """  Returns stored transaction cursors """
    result = [bank for bank in current_app.client.plaidDB.transactionCursors.find({})]
    for cursor in result:
        cursor['_id'] = str(cursor['_id'])
    current_app.logger.debug(f"Returning: {type(result)}")
    current_app.logger.info(f"Returning: {result}")
    if result:
        return flask.jsonify(result)
    else:
        return ''
    
@plaiddb_blueprint.route('/database/transaction_cursors/', methods=['PUT'])
def set_t_cursors():
    """  Returns stored transaction cursors """
    json_data = flask.request.json
    institution = json_data['institution']
    t_cursor = json_data['transaction_cursor']
    current_app.client.plaidDB.transactionCursors.update_one(
        {'bank_name': institution},
        {"$set":{'transaction_cursor': t_cursor, 
                 'last_updated': time_.timestamp()}},
        upsert = True)
    return "Success", 200
    # for cursor in result:
    #     cursor['_id'] = str(cursor['_id'])
    # current_app.logger.debug(f"Returning: {type(result)}")
    # current_app.logger.info(f"Returning: {result}")
    # if result:
    #     return flask.jsonify(result)
    # else:
    #     return ''

@plaiddb_blueprint.route('/database/access_tokens/', methods=['GET'])
def get_accesstokens():
    """  Returns stored access tokens """
    result = [bank for bank in current_app.client.plaidDB.itemTokens.find({})]
    for token_dict in result:
        token_dict['_id'] = str(token_dict['_id'])
    current_app.logger.debug(f"Returning: {type(result)}")
    current_app.logger.info(f"Returning: {result}")
    if result:
        return flask.jsonify(result)
    else:
        return ''

@plaiddb_blueprint.route('/database/access_tokens/', methods=['POST'])
def set_accesstokens():
    """ Set item's access token """
    json_data = flask.request.json
    item = json_data['item']
    access_token = json_data['access_token']
    current_app.client.plaidDB.itemTokens.update_one(
        {'institution': item},
        {"$set":{"access_token": access_token,  
                 'working': True, 
                 'last_updated': time_.timestamp()}},
        upsert = True)
    return "Success", 200
    
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