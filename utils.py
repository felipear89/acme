from datetime import timedelta

def daterange(start_date, end_date):
  for n in range(int ((end_date - start_date).days + 1)):
    yield start_date + timedelta(n)

def hours_minutes(td):
  days = td.days
  hours = td.seconds//3600
  minutes = (td.seconds//60)%60
  hours = hours + (days * 24)
  if hours < 0:
    return '%03d:%02d' % (hours, minutes)
  return '%02d:%02d' % (hours, minutes)

def transform(array, key, apply):
  response = []
  for i in array:
    array_value = i.copy()
    array_value[key] = apply(array_value[key])
    response.append(array_value)
  return response