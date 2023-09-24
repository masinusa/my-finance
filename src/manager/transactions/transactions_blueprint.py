from flask import Blueprint

transactions_blueprint = Blueprint('transactions_blueprint', __name__)

@transactions_blueprint.route('/transactions/')
def some2():
    return "This is an example app"