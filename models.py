import itertools
from enum import Enum

class TimeSheet:
  
  def __init__(self, entries):
    self.entries_list = entries
    self.entry_by_day = self.map_timesheet()
  
  def clock_in(self, date):
    return self.entry_by_day[date][0]
  
  def clock_out(self, date):
    day_timeclock = self.entry_by_day[date]
    size = len(day_timeclock)
    return day_timeclock[size-1]

  def map_timesheet(self):
    timesheet = {}
    for key, group in itertools.groupby(self.entries_list, key=lambda e: e.split('T')[0]):
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

class Weekday(Enum):
  mon = 0
  tue = 1
  wed = 2
  thu = 3
  fri = 4
  sat = 5
  sun = 6