from utils import daterange, pretty_timedelta
from datetime import date, timedelta

def test_daterange():
  start_date = date(2018, 5, 30)
  end_date = date(2018, 6, 1)
  interval = daterange(start_date, end_date)
  assert date(2018, 5, 30) == interval.__next__()
  assert date(2018, 5, 31) == interval.__next__()
  assert date(2018, 6, 1) == interval.__next__()

