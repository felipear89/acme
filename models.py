import itertools

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
