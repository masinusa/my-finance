import sys
import os 
from pathlib import Path
import json

import requests
from flask import Blueprint, request, current_app

# Add base container path
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')


from lib.utils import time_

# Create Flask Blueprint
balancesdb_blueprint = Blueprint('balancesdb', __name__)

def _cur_month_collection(offset: int = 0):
    curr_m_y = time_.curr_month_year_int(relative_month=offset)
    return current_app.client.balancesDB[curr_m_y]

@balancesdb_blueprint.route('/database/balances/', methods=['GET'])
def get_balancesdb():
    """  Gives a month's last recorded total balances. 

    """
    month_offset = request.args.get('month_offset')
    month_offset = int(month_offset)
    cursor = _cur_month_collection(offset = month_offset).find({'institution': {"$exists":True}})
    # Parse result for each document returned
    results = []
    for document in cursor:
        doc_dict = {"_id": str(document["_id"]),
                    "balance": document["balance"],
                    "account": document['account'],
                    "institution": document["institution"],
                    "last_updated": document["last_updated"],
                    "subtype": document["subtype"],
        }
        results.append(doc_dict)
    return json.dumps(results)


@balancesdb_blueprint.route('/database/balances/update', methods=['PUT'])
def update_balancesdb():
    json_data = json.loads(request.json)
    current_app.logger.debug(f"Received JSON: {json_data}")
    current_app.logger.debug(f"of type: {type(json_data)}")
    current_app.logger.debug(f"of type: {int(request.args['month_offset'])}")
    current_app.logger.debug(f"of type: {type(int(request.args['month_offset']))}")
    _cur_month_collection(offset = int(request.args['month_offset'])).update_one(
        {"institution": json_data['institution'],
         'account': json_data['account']},
        {"$set":{
            # "_id": id,
            "institution": json_data['institution'],
            "account": json_data['account'],
            "balance": json_data['balance'],
            "subtype": json_data['subtype'],
            'last_updated': time_.timestamp()}},
        upsert = True)

    return '', 200