from models import TimeSheet, Employee, Weekday
from utils import pos_processor_workload
from datetime import datetime

default_workload = [{'workload_in_minutes': 540, 'minimum_rest_interval_in_minutes': 60,
                'days': ['mon', 'tue','wed','thu']},
              {'workload_in_minutes': 480, 'minimum_rest_interval_in_minutes': 60,
                'days': ['fri']}]
  
def default_processor(minutes, date):
  return minutes

def test_map_timesheet():
  entries = ['2018-04-10T05:43:00', '2018-04-10T09:28:00', '2018-04-10T09:46:00', '2018-04-10T11:05:00',
      '2018-04-12T02:26:00','2018-04-12T05:42:00','2018-04-12T05:56:00','2018-04-12T07:42:00',
      '2018-04-13T09:43:00','2018-04-13T10:30:00',]

  timesheet = TimeSheet(entries)

  assert len(timesheet.entry_by_day['2018-04-10']) == 4
  assert len(timesheet.entry_by_day['2018-04-13']) == 2
  assert timesheet.entry_by_day['2018-04-13'][0] == '2018-04-13T09:43:00'
  assert timesheet.entry_by_day['2018-04-13'][1] == '2018-04-13T10:30:00'

def test_get_clock_in():
  entries = ['2018-04-10T05:43:00', '2018-04-10T09:28:00', '2018-04-10T09:46:00', '2018-04-10T11:05:00',
      '2018-04-12T02:26:00','2018-04-12T05:42:00','2018-04-12T05:56:00','2018-04-12T07:42:00',
      '2018-04-13T09:43:00','2018-04-13T10:30:00', '2018-04-14T10:00:00', '2018-04-14T09:00:00']

  timesheet = TimeSheet(entries)

  assert str(timesheet.clock_in('2018-04-10')) == '2018-04-10 05:43:00'
  assert str(timesheet.clock_in('2018-04-12')) == '2018-04-12 02:26:00'
  assert str(timesheet.clock_in('2018-04-14')) == '2018-04-14 09:00:00'

def test_get_interval_clock_in():
  entries = ['2018-04-10T05:43:00', '2018-04-10T09:28:00', '2018-04-10T09:46:00', '2018-04-10T11:05:00',
      '2018-04-12T02:26:00','2018-04-12T05:42:00','2018-04-12T05:56:00','2018-04-12T07:42:00',
      '2018-04-13T09:43:00','2018-04-13T10:30:00', '2018-04-14T10:00:00', '2018-04-14T09:00:00']

  timesheet = TimeSheet(entries)

  assert str(timesheet.interval_clock_in('2018-04-10')) == '2018-04-10 09:46:00'
  assert str(timesheet.interval_clock_in('2018-04-12')) == '2018-04-12 05:56:00'
  assert timesheet.interval_clock_in('2018-04-14') == None

def test_get_interval_clock_out():
  entries = ['2018-04-10T05:43:00', '2018-04-10T09:28:00', '2018-04-10T09:46:00', '2018-04-10T11:05:00',
      '2018-04-12T02:26:00','2018-04-12T05:42:00','2018-04-12T05:56:00','2018-04-12T07:42:00',
      '2018-04-13T09:43:00','2018-04-13T10:30:00', '2018-04-14T10:00:00', '2018-04-14T09:00:00']

  timesheet = TimeSheet(entries)

  assert str(timesheet.interval_clock_out('2018-04-10')) == '2018-04-10 09:28:00'
  assert str(timesheet.interval_clock_out('2018-04-12')) == '2018-04-12 05:42:00'
  assert timesheet.interval_clock_out('2018-04-14') == None

def test_get_clock_out():
  entries = ['2018-04-10T05:43:00', '2018-04-10T09:28:00', '2018-04-10T09:46:00', '2018-04-10T11:05:00',
      '2018-04-12T02:26:00','2018-04-12T05:42:00','2018-04-12T05:56:00','2018-04-12T07:42:00',
      '2018-04-13T09:43:00','2018-04-13T10:30:00', '2018-04-14T10:00:00', '2018-04-14T09:00:00']

  timesheet = TimeSheet(entries)

  assert str(timesheet.clock_out('2018-04-10')) == '2018-04-10 11:05:00'
  assert str(timesheet.clock_out('2018-04-12')) == '2018-04-12 07:42:00'
  assert str(timesheet.clock_out('2018-04-14')) == '2018-04-14 10:00:00'

def test_map_week_workload():
  
  employee = Employee(None, default_workload, default_processor)
  
  assert employee.workload[Weekday.mon]['workload_in_minutes'] == 540
  assert employee.workload[Weekday.fri]['workload_in_minutes'] == 480
  assert employee.workload[Weekday.sat]['workload_in_minutes'] == 0
  assert employee.workload[Weekday.sun]['workload_in_minutes'] == 0

def test_interval_timesheet():
  entries = ['2018-04-10T05:43:00', '2018-04-10T09:28:00', '2018-04-10T09:46:00', '2018-04-10T11:05:00',
      '2018-04-12T02:26:00','2018-04-12T05:42:00','2018-04-12T05:56:00','2018-04-12T07:42:00',
      '2018-04-13T09:43:00','2018-04-13T10:30:00',]

  timesheet = TimeSheet(entries)
  interval_duration = timesheet.interval_duration('2018-04-10')

  assert str(interval_duration) == '0:18:00'

def test_total_interval_duration_without_entry():
  entries = ['2018-04-12T08:00:00','2018-04-12T12:00:00','2018-04-12T13:00:00','2018-04-12T20:00:00',]
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  assert str(employee.total_interval_duration('2018-04-14')) == '0:00:00'

def test_total_interval_duration_without_interval():
  entries = ['2018-04-12T08:00:00', '2018-04-12T20:00:00',]
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  assert str(employee.total_interval_duration('2018-04-12')) == '0:00:00'

def test_total_interval_duration_with_incomplete_workday():
  entries = ['2018-04-16T08:00:00','2018-04-16T09:00:00','2018-04-16T13:00:00','2018-04-16T14:00:00',]
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  assert str(employee.total_interval_duration('2018-04-16')) == '0:00:00'

def test_total_interval_duration_with_1_min():
  entries = ['2018-04-12T08:00:00','2018-04-12T12:00:00','2018-04-12T12:01:00','2018-04-12T21:01:00']
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  assert str(employee.total_interval_duration('2018-04-12')) == '0:01:00'

def test_total_interval_duration():
  entries = ['2018-04-10T05:43:00', '2018-04-10T09:28:00', '2018-04-10T09:46:00', '2018-04-10T11:05:00',
    '2018-04-12T08:00:00','2018-04-12T12:00:00','2018-04-12T13:00:00','2018-04-12T20:00:00',
    '2018-04-16T08:00:00','2018-04-16T09:00:00','2018-04-16T13:00:00','2018-04-16T14:00:00',]
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  assert str(employee.total_interval_duration('2018-04-10')) == '0:18:00'
  assert str(employee.total_interval_duration('2018-04-12')) == '1:00:00'

def test_workedtime_completed_workday():
  entries = ['2018-04-12T08:00:00','2018-04-12T12:00:00','2018-04-12T13:00:00','2018-04-12T18:00:00']
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  assert str(employee.total_day_worked_time('2018-04-12')) == '9:00:00'

def test_workedtime_completed_workday_1_min_interval():
  entries = ['2018-04-12T08:00:00','2018-04-12T12:00:00','2018-04-12T12:01:00','2018-04-12T18:00:00']
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  assert str(employee.total_day_worked_time('2018-04-12')) == '9:59:00'

def test_workedtime_without_interval():
  entries = ['2018-04-12T08:00:00','2018-04-12T20:00:00']
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  assert str(employee.total_day_worked_time('2018-04-12')) == '12:00:00'

def test_workedtime_incomplete_workday():
  entries = ['2018-04-12T08:00:00','2018-04-12T12:00:00','2018-04-12T12:10:00','2018-04-12T12:11:00']
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  assert str(employee.total_day_worked_time('2018-04-12')) == '4:01:00'

def test_employee_invalid_interval():
  entries = ['2018-04-12T08:00:00','2018-04-12T12:00:00','2018-04-12T12:10:00','2018-04-12T12:11:00']
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  assert employee.is_invalid_interval('2018-04-12') is True

def test_employee_valid_interval():
  entries = ['2018-04-12T08:00:00','2018-04-12T12:00:00','2018-04-12T12:10:00','2018-04-12T20:11:00']
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  assert employee.is_invalid_interval('2018-04-12') is False

def test_balance_zero():
  entries = ['2018-04-12T08:00:00','2018-04-12T12:00:00','2018-04-12T13:00:00','2018-04-12T18:00:00']
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  assert employee.balance_in_minutes('2018-04-12') == 0

def test_balance_with_credit():
  entries = ['2018-04-12T08:00:00','2018-04-12T12:00:00','2018-04-12T13:00:00','2018-04-12T19:00:00']
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  assert employee.balance_in_minutes('2018-04-12') == 60

def test_balance_with_debit():
  entries = ['2018-04-12T08:00:00','2018-04-12T12:00:00','2018-04-12T13:00:00','2018-04-12T16:59:00']
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  assert employee.balance_in_minutes('2018-04-12') == -61

def test_balance_without_interval():
  entries = ['2018-04-12T08:00:00', '2018-04-12T09:00:00']
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  assert employee.balance_in_minutes('2018-04-12') == -480

def test_history_just_one_day():
  entries = ['2018-04-12T08:00:00','2018-04-12T12:00:00','2018-04-12T13:00:00','2018-04-12T19:00:00']
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  history = employee.history(datetime(2018, 4,12), datetime(2018, 4,12))
  assert len(history) == 1
  assert history[0]['day'] == '2018-04-12'
  assert history[0]['balance'] == 60

def test_history_between_two_days():
  entries = ['2018-04-12T08:00:00','2018-04-12T12:00:00','2018-04-12T13:00:00','2018-04-12T19:00:00']
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  history = employee.history(datetime(2018, 4,12), datetime(2018, 4,16))
  assert len(history) == 5
  assert history[0]['day'] == '2018-04-12'
  assert history[0]['balance'] == 60
  assert history[1]['day'] == '2018-04-13'
  assert history[1]['balance'] == -480
  assert history[2]['day'] == '2018-04-14'
  assert history[2]['balance'] == 0
  assert history[3]['day'] == '2018-04-15'
  assert history[3]['balance'] == 0
  assert history[4]['day'] == '2018-04-16'
  assert history[4]['balance'] == -540

def test_balance_summary():
  entries = ['2018-04-12T08:00:00','2018-04-12T12:00:00','2018-04-12T13:00:00','2018-04-12T19:00:00']
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  history = employee.history(datetime(2018, 4,12), datetime(2018, 4,16))
  balance_summary = employee.balance_summary_in_minutes(history)
  assert (balance_summary.total_seconds() / 60) == -960

def test_response():
  entries = ['2018-04-12T08:00:00','2018-04-12T12:00:00','2018-04-12T13:00:00','2018-04-12T18:00:00',
            '2018-04-13T08:00:00','2018-04-13T12:00:00','2018-04-13T13:00:00','2018-04-13T19:00:00',
            '2018-04-17T08:00:00','2018-04-17T12:00:00','2018-04-17T13:00:00','2018-04-17T19:00:00',
            '2018-04-18T08:00:00','2018-04-18T20:00:00',
            '2018-04-19T10:00:00','2018-04-19T12:00:00','2018-04-19T12:30:00','2018-04-19T13:30:00',
            
  ]
  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, default_processor)
  
  response = employee.response(datetime(2018, 4,12), datetime(2018, 4,19), '123456')
  
  assert response['pis_number'] == '123456'
  assert response['summary']['balance'] == '-09:00'
  assert response['history'][0]['day'] == '2018-04-12'
  assert response['history'][0]['balance'] == '00:00'
  assert response['history'][1]['balance'] == '02:00'
  assert response['history'][2]['balance'] == '00:00'
  assert response['history'][3]['balance'] == '00:00'
  assert response['history'][4]['balance'] == '-09:00'
  assert response['history'][5]['balance'] == '01:00'
  assert response['history'][6]['balance'] == '03:00'
  assert response['history'][7]['balance'] == '-06:00'

def test_with_holydays():
  entries = ['2018-04-12T08:00:00','2018-04-12T12:00:00','2018-04-12T13:00:00','2018-04-12T18:00:00',
            '2018-04-13T08:00:00','2018-04-13T12:00:00','2018-04-13T13:00:00','2018-04-13T19:00:00',
            '2018-04-17T08:00:00','2018-04-17T12:00:00','2018-04-17T13:00:00','2018-04-17T19:00:00',
            '2018-04-18T08:00:00','2018-04-18T20:00:00',
            '2018-04-19T10:00:00','2018-04-19T12:00:00','2018-04-19T12:30:00','2018-04-19T13:30:00',
            
  ]

  holydays_processor = lambda minutes, workload_date: pos_processor_workload(minutes, workload_date, ['2018-04-19', '2018-04-13'])

  timesheet = TimeSheet(entries)
  employee = Employee(timesheet, default_workload, holydays_processor)
  
  response = employee.response(datetime(2018, 4,12), datetime(2018, 4,19), '123456')
  
  assert response['pis_number'] == '123456'
  assert response['summary']['balance'] == '08:00'
