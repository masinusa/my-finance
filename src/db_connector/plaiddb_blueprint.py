import sys
import os 
from pathlib import Path
import json

import requests
from flask import Blueprint, request, current_app, jsonify

# Add base container path
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')


from lib.utils import time_

# Create Flask Blueprint
plaiddb_blueprint = Blueprint('plaiddb_blueprint', __name__)

@plaiddb_blueprint.route('/database/access_tokens/', methods=['GET'])
def get_accesstokens():
    """  Returns stored access tokens """
    result = [bank for bank in current_app.client.plaidDB.bankTokens.find({})]
    for token_dict in result:
        token_dict['_id'] = str(token_dict['_id'])
    current_app.logger.debug(f"Returning: {type(result)}")
    current_app.logger.info(f"Returning: {result}")
    if result:
        return jsonify(result)
    else:
        return ''
    


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