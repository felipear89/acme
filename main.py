from collections import namedtuple
from datetime import timedelta, date, datetime
import argparse, json, itertools

def handle_arguments():
  parser = argparse.ArgumentParser(description='Return the workload balance.')
  parser.add_argument('--config', dest='config', help='The config path')
  parser.add_argument('--timeclock', dest='timeclock', help='The timeclock entries path')
  return vars(parser.parse_args())

def fill_empty_values(dictionary, fill):
  new_dict = dictionary.copy()
  for key, value in dictionary.items():
    if value is None:
      new_dict[key] = fill(key)
  return new_dict

def transform_filled_values(dictionary, transform):
  new_dict = dictionary.copy()
  for key, value in dictionary.items():
    if value is not None:
      new_dict[key] = transform(value)
  return new_dict

def load_to_json(path):
  file = open(path, 'r')
  with file as f:
    data = json.load(f)
  return data

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)

def find_by_pis_number(employees, pis):
  for employee in employees:
    if employee['pis_number'] == pis:
      return employee

def main():
  
  args = handle_arguments()
  json_args = transform_filled_values(args, load_to_json)
  ask_input = lambda param : json.load(input(f'Enter the {param} param input: '))
  user_input = fill_empty_values(json_args, ask_input)
  
  pis = input('Retrieve balance from pis number: ')

  config = user_input['config']
  timeclock = user_input['timeclock']

  employee_config = find_by_pis_number(config['employees'], pis)
  employee_timeclock = find_by_pis_number(timeclock, pis)

  employee = Employee(employee_config['workload'], employee_timeclock['entries'])


  today = datetime.strptime(config['today'], '%Y-%m-%d')
  period_start = datetime.strptime(config['period_start'], '%Y-%m-%d')
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