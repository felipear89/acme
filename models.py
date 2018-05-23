import itertools
from datetime import datetime, timedelta
from enum import Enum

class TimeSheet:
  
  def __init__(self, entries):
    self.entries_list = entries
    self.entry_by_day = self.map_timesheet(self.entries_list)
  
  def clock_in(self, date):
    if date not in self.entry_by_day:
      return None
    return datetime.strptime(self.entry_by_day[date][0], '%Y-%m-%dT%H:%M:%S')

  def interval_clock_in(self, date):
    if date in self.entry_by_day and len(self.entry_by_day[date]) == 4:
      return datetime.strptime(self.entry_by_day[date][2], '%Y-%m-%dT%H:%M:%S')

  def interval_clock_out(self, date):
    if date in self.entry_by_day and len(self.entry_by_day[date]) == 4:
      return datetime.strptime(self.entry_by_day[date][1], '%Y-%m-%dT%H:%M:%S')

  def interval_duration(self, date):
    leave = self.interval_clock_out(date)
    arrive = self.interval_clock_in(date)
    return arrive - leave
  
  def clock_out(self, date):
    if date not in self.entry_by_day:
      return None
    day_timeclock = self.entry_by_day[date]
    size = len(day_timeclock)
    return datetime.strptime(day_timeclock[size-1], '%Y-%m-%dT%H:%M:%S')

  def map_timesheet(self, entries_list):
    timesheet = {}
    for key, group in itertools.groupby(entries_list, key=lambda e: e.split('T')[0]):
      timesheet[key] = sorted(list(group))
    return timesheet

class Employee:

  def __init__(self, timesheet, workload):
    self.timesheet = timesheet
    self.workload = self.map_week_workload(workload)

  def map_week_workload(self, employee_workload):
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

  def total_interval_duration(self, date):
    clock_in = self.timesheet.clock_in(date)
    interval_clock_out = self.timesheet.interval_clock_out(date)
    interval_clock_in = self.timesheet.interval_clock_in(date)
    clock_out = self.timesheet.clock_out(date)

    workload_in_minutes = self.workload[Weekday(datetime.strptime(date, '%Y-%m-%d').weekday())]['workload_in_minutes']
    if None in (clock_in, clock_out, interval_clock_in, interval_clock_out,):
      return timedelta(0)
    
    worked_time = (clock_out - interval_clock_in) + (interval_clock_out - clock_in)
    worked_time_minutes = int(worked_time.total_seconds() / 60)
    
    if (worked_time_minutes >= workload_in_minutes / 2):
      return self.timesheet.interval_duration(date)
    return timedelta(0)

  def total_day_worked_time(self, date):
    total_interval_duration = self.total_interval_duration(date)
    clock_in = self.timesheet.clock_in(date)
    clock_out = self.timesheet.clock_out(date)
    if None in (clock_in, clock_out, total_interval_duration,):
      return 0
    
    invalid_interval = timedelta(0)
    if self.is_invalid_interval(date):
      interval_clock_out = self.timesheet.interval_clock_out(date)
      interval_clock_in = self.timesheet.interval_clock_in(date)
      invalid_interval = interval_clock_in - interval_clock_out
      
    return clock_out - clock_in - total_interval_duration - invalid_interval
  
  def is_invalid_interval(self, date):
    return self.total_interval_duration(date) == timedelta(0) and len(self.timesheet.entry_by_day[date]) == 4

class Weekday(Enum):
  mon = 0
  tue = 1
  wed = 2
  thu = 3
  fri = 4
  sat = 5
  sun = 6