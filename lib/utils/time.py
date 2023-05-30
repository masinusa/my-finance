import json
from datetime import datetime
import calendar
import math

import numpy as np


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


# _____ TIME STAMP _____
def timestamp():
  return str(datetime.now()).split()[0]

def timestamp_to_int(timestamp):
  split = timestamp.split('-')
  return int(split[0])*1000 + int(split[1])*100 + int(split[2])

def int_to_timestamp(val):
  year, remainder = divmod(val, 1000)
  month, remainder = divmod(remainder, 100)
  day = remainder
  if month < 10:
    month = f"0{month}"
  if day < 10:
    day = f"0{day}"
  return f"{year}-{month}-{day}"

def datetime_to_timestamp(dt: datetime) -> str:
  return dt.strftime("%Y-%m-%d")




def curr_month_year(relative_month: int = 0) -> str:
  """
  Returns abbreviated month followed by the year
  """
  # Calculate Month
  curr_month = datetime.now().month -1 # Jan = 0, Dec = 11
  month_int = curr_month + relative_month
  normal_month_int = month_int % 12
  month = calendar.month_abbr[normal_month_int + 1]

  # Calculate Year
  relative_year = math.floor((curr_month + relative_month) / 12)
  year = datetime.now().year + relative_year

  return month + '_' + str(year)
  



if __name__ == '__main__':

  # Check curr_month_year
  for i in range(-15, 15):
    print(f"relative month: {i}, {curr_month_year(i)}")