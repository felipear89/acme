from enum import Enum
from collections import namedtuple
from datetime import timedelta, date, datetime
import argparse, json, itertools

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

def map_week_workload(employee_workload):
  default_workload = {
        'workload_in_minutes': 0,
        'minimum_rest_interval_in_minutes': 0,
      }
  
  week_workload = {Weekday.mon: default_workload, Weekday.tue: default_workload, Weekday.wed: default_workload, \
        Weekday.thu: default_workload, Weekday.fri: default_workload, Weekday.sat: default_workload,\
        Weekday.sun: default_workload}

  for workload in employee_workload:
      for day in workload['days']:
        week_workload[Weekday[day]] = {
          'workload_in_minutes': workload['workload_in_minutes'],
          'minimum_rest_interval_in_minutes': workload['minimum_rest_interval_in_minutes'],
        }
  return week_workload

def map_timesheet(entries):
  timesheet = {}
  for key, group in itertools.groupby(entries, key=lambda e: e.split('T')[0]):
    timesheet[key] = list(group)
  return timesheet

def main():
  
  args = handle_arguments()
  json_args = transform_filled_values(args, load_to_json)
  ask_input = lambda param : json.load(input(f'Enter the {param} param input: '))
  user_input = fill_empty_values(json_args, ask_input)
  pis = input('Retrieve balance from pis number: ')

  config = user_input['config']
  timeclock = user_input['timeclock']

  today = datetime.strptime(config['today'], '%Y-%m-%d')
  period_start = datetime.strptime(config['period_start'], '%Y-%m-%d')
  
  employee = find_employee(config['employees'], pis)
  week_workload = map_week_workload(employee['workload'])
  employee_entries = find_employee(timeclock, pis)

  timesheet = map_timesheet(employee_entries['entries'])

  for d in daterange(period_start, today):
    day_workload = week_workload[Weekday(d.weekday())]
    try:
      day_entries = timesheet[d.strftime('%Y-%m-%d')]
      print(day_entries)
    except KeyError as err:
      # Employee doesn't work at this date :( 
      pass
    
if __name__ == '__main__':
    main()