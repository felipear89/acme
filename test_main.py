from main import fill_empty_values, transform_filled_values, find_by_pis_number
from models import Weekday
from datetime import date

def test_fill_empty_values():
  my_dict = {'config': None, 'timeclock': 'timeclock path'}
  ask_input = lambda key : 'config path'
  filled_input = fill_empty_values(my_dict, ask_input)
  assert filled_input['config'] == 'config path'
  assert filled_input['timeclock'] == 'timeclock path'

def test_transform_filled_values():
  my_dict = {'config': None, 'timeclock': 'timeclock path'}
  ask_input = lambda key : 'new timeclock path'
  filled_input = transform_filled_values(my_dict, ask_input)
  assert filled_input['config'] is None
  assert filled_input['timeclock'] == 'new timeclock path'
  
def test_find_by_pis_number():
  employees = [{'pis_number': '123'}, {'pis_number': '456'}]
  employee = find_by_pis_number(employees, '456')
  assert employee['pis_number'] == '456'
  