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
  workload = [{'workload_in_minutes': 540, 'minimum_rest_interval_in_minutes': 60,
                'days': ['mon', 'tue','wed','thu']},
              {'workload_in_minutes': 480, 'minimum_rest_interval_in_minutes': 60,
                'days': ['fri']}]
  employee = Employee(None, workload)
  
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

def test_total_day_worked_time():
  pass

def test_total_interval_duration():
  entries = ['2018-04-10T05:43:00', '2018-04-10T09:28:00', '2018-04-10T09:46:00', '2018-04-10T11:05:00',
    '2018-04-12T08:00:00','2018-04-12T12:00:00','2018-04-12T13:00:00','2018-04-12T20:00:00',
    '2018-04-13T09:43:00','2018-04-13T10:30:00',]

  timesheet = TimeSheet(entries)
  workload = [{'workload_in_minutes': 540, 'minimum_rest_interval_in_minutes': 60,
                'days': ['mon', 'tue','wed','thu']},
              {'workload_in_minutes': 480, 'minimum_rest_interval_in_minutes': 60,
                'days': ['fri']}]
  employee = Employee(timesheet, workload)

  assert str(employee.total_interval_duration('2018-04-10')) == '0:18:00'
  assert str(employee.total_interval_duration('2018-04-12')) == '1:00:00'
  assert str(employee.total_interval_duration('2018-04-13')) == '0'
  assert str(employee.total_interval_duration('2018-04-14')) == '0'
