from enum import Enum
from pprint import pprint
from collections import namedtuple
from datetime import timedelta, date, datetime
import argparse, json

class Weekday(Enum):
  mon = 0
  tue = 1
  wed = 2
  thu = 3
  fri = 4
  sat = 5
  sun = 6

def handle_arguments():
  parser = argparse.ArgumentParser(description='Return the workload balance.')
  parser.add_argument('--config', dest='config', help='The config path')
  parser.add_argument('--timeclock', dest='timeclock', help='The timeclock entries path')
  return vars(parser.parse_args())

def fill_empty_values(dictionary, m):
  new_dict = dictionary.copy()
  for key, value in dictionary.items():
    if value is None:
      new_dict[key] = m(key)
  return new_dict

def transform_filled_values(dictionary, m):
  new_dict = dictionary.copy()
  for key, value in dictionary.items():
    if value is not None:
      new_dict[key] = m(value)
  return new_dict

def load_to_json(path):
  file = open(path, 'r')
  with file as f:
    data = json.load(f)
  return data

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)

def find_employee(employees, pis):
  for employee in employees:
    if employee['pis_number'] == pis:
      return employee

def map_week_workload(employee):
  default_workload = {
        'workload_in_minutes': 0,
        'minimum_rest_interval_in_minutes': 0,
      }
  
  week_workload = {Weekday.mon: default_workload, Weekday.tue: default_workload, Weekday.wed: default_workload, \
        Weekday.thu: default_workload, Weekday.fri: default_workload, Weekday.sat: default_workload,\
        Weekday.sun: default_workload}

  for workload in employee['workload']:
      for day in workload['days']:
        week_workload[Weekday[day]] = {
          'workload_in_minutes': workload['workload_in_minutes'],
          'minimum_rest_interval_in_minutes': workload['minimum_rest_interval_in_minutes'],
        }
  return week_workload

def main():
  
  args = handle_arguments()
  json_args = transform_filled_values(args, load_to_json)
  ask_input = lambda param : json.load(input(f'Enter the {param} param input: '))
  user_input = fill_empty_values(json_args, ask_input)
  user_input['requested_pis'] = input('Retrieve balance from pis number: ')

  config = user_input['config']
  today = datetime.strptime(config['today'], '%Y-%m-%d')
  period_start = datetime.strptime(config['period_start'], '%Y-%m-%d')
  employee = find_employee(config['employees'], user_input['requested_pis'])
  week_workload = map_week_workload(employee)
  
  for date in daterange(period_start, today):
    pass#
    




if __name__ == '__main__':
    main()