import sys
import os 
from pathlib import Path
import requests

from flask import Blueprint, request, current_app

# Add base container path
if "/finapp/" not in sys.path:
    sys.path.append('/finapp')

from balances.get_balances import get_balances
from balances.update_balances import update_balances

# Create Flask Blueprint
balances_blueprint = Blueprint('balances_blueprint', __name__)

@balances_blueprint.route('/balances/', methods=['GET'])
def _get_balances():
    """  Gives a month's last recorded total balances. 
    
    See get_balances()
    """
    month = request.args.get('month_offset')
    month = int(month)
    return get_balances(month)

@balances_blueprint.route('/balances/update', methods=['PUT'])
def _update_balances():
    month = request.args.get('month_offset')
    month = int(month)
    return update_balances(month)

