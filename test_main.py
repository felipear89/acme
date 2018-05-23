from main import handle_arguments, fill_empty_values, transform_filled_values, daterange, \
find_by_pis_number, map_timesheet
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

def test_daterange():
  start_date = date(2018, 5, 30)
  end_date = date(2018, 6, 1)
  interval = daterange(start_date, end_date)
  assert date(2018, 5, 30) == interval.__next__()
  assert date(2018, 5, 31) == interval.__next__()
  assert date(2018, 6, 1) == interval.__next__()
  
def test_find_by_pis_number():
  employees = [{'pis_number': '123'}, {'pis_number': '456'}]
  employee = find_by_pis_number(employees, '456')
  assert employee['pis_number'] == '456'
  
  def test_map_timesheet():
    entries = ['2018-04-10T05:43:00', '2018-04-10T09:28:00', '2018-04-10T09:46:00', '2018-04-10T11:05:00',
        '2018-04-12T02:26:00','2018-04-12T05:42:00','2018-04-12T05:56:00','2018-04-12T07:42:00',
        '2018-04-13T09:43:00','2018-04-13T10:30:00',]

    timesheet = map_timesheet(entries)

    assert len(timesheet['2018-04-10']) == 4
    assert len(timesheet['2018-04-13']) == 2
    assert timesheet['2018-04-13'][0] == '2018-04-13T09:43:00'
    assert timesheet['2018-04-13'][1] == '2018-04-13T10:30:00'