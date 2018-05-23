from utils import daterange, hours_minutes
from datetime import date, timedelta

def test_daterange():
  start_date = date(2018, 5, 30)
  end_date = date(2018, 6, 1)
  interval = daterange(start_date, end_date)
  assert date(2018, 5, 30) == interval.__next__()
  assert date(2018, 5, 31) == interval.__next__()
  assert date(2018, 6, 1) == interval.__next__()

def hours_minutes():
  assert hours_minutes(timedelta(minutes=1)) == '00:01'
  assert hours_minutes(timedelta(hour=1, minutes=1)) == '01:01'
  assert hours_minutes(timedelta(hour=24)) == '24:00'
  assert hours_minutes(timedelta(hour=25)) == '25:00'
  assert hours_minutes(timedelta(days=2)) == '48:00'
  assert hours_minutes(timedelta(days=-1)) == '-24:00'
  assert hours_minutes(timedelta(minutes=-4)) == '-00:04'