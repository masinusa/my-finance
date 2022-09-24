import json
from datetime import datetime



def pretty_print_response(response):
  print(json.dumps(response, indent=2, sort_keys=True, default=str))

def swap_dict_keys_values(dict):
  return {v: k for k, v in dict.items()}


def format_error(e):
    response = json.loads(e.body)
    return {'error': {'status_code': e.status, 'display_message':
                      response['error_message'], 'error_code': response['error_code'], 'error_type': response['error_type']}}

# https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
def curr_month():
  return datetime.now().strftime("%b")

#   return datetime.now().month
  #   currentSecond= datetime.now().second
  # currentMinute = datetime.now().minute
  # currentHour = datetime.now().hour

  # currentDay = datetime.now().day
  # currentMonth = datetime.now().month
  # currentYear = datetime.now().year

def curr_year():
  return str(datetime.now().year)

def timestamp():
  return str(datetime.now()).split()[0]

def curr_month_year():
  return curr_month() + ' ' + curr_year()



