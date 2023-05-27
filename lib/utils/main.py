
import json
from datetime import datetime
import calendar


def pretty_print_response(response):
  print(json.dumps(response, indent=2, sort_keys=True, default=str))

def swap_dict_keys_values(dict):
  return {v: k for k, v in dict.items()}


def format_error(e):
    response = json.loads(e.body)
    return {'error': {'status_code': e.status, 'display_message':
                      response['error_message'], 'error_code': response['error_code'], 'error_type': response['error_type']}}