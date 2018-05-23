from models import TimeSheet, Employee, Weekday
  
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

  assert timesheet.clock_in('2018-04-10') == '2018-04-10T05:43:00'
  assert timesheet.clock_in('2018-04-12') == '2018-04-12T02:26:00'
  assert timesheet.clock_in('2018-04-14') == '2018-04-14T09:00:00'
  
def test_get_clock_out():
  entries = ['2018-04-10T05:43:00', '2018-04-10T09:28:00', '2018-04-10T09:46:00', '2018-04-10T11:05:00',
      '2018-04-12T02:26:00','2018-04-12T05:42:00','2018-04-12T05:56:00','2018-04-12T07:42:00',
      '2018-04-13T09:43:00','2018-04-13T10:30:00', '2018-04-14T10:00:00', '2018-04-14T09:00:00']

  timesheet = TimeSheet(entries)

  assert timesheet.clock_out('2018-04-10') == '2018-04-10T11:05:00'
  assert timesheet.clock_out('2018-04-12') == '2018-04-12T07:42:00'
  assert timesheet.clock_out('2018-04-14') == '2018-04-14T10:00:00'

def test_map_week_workload():
  workload = [{'workload_in_minutes': 540, 'minimum_rest_interval_in_minutes': 60,
                'days': ['mon', 'tue','wed','thu']},
              {'workload_in_minutes': 480, 'minimum_rest_interval_in_minutes': 60,
                'days': ['fri']}]
  employee = Employee(None, workload)
  
  assert employee.workload[Weekday.mon]['workload_in_minutes'] == 540
  assert employee.workload[Weekday.fri]['workload_in_minutes'] == 480
  assert employee.workload[Weekday.sat]['workload_in_minutes'] == 0
  assert employee.workload[Weekday.sun]['workload_in_minutes'] == 0