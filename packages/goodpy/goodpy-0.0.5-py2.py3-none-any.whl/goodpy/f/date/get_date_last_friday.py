from datetime import datetime
from datetime import timedelta
from typing import Union
  
def f(date: Union[str, None]=None)->str:
  dt_date = datetime.fromisoformat(date) if date is not None else datetime.today()
  difference = {
    0: -1 - 2, #Monday
    1: -2 - 2, #Tuesday,
    2: -3 - 2, #Wednesday,
    3: -4 - 2, #Thursday,
    4: -5 - 2, #Friday,
    5: -6 - 2, #Saturday,
    6: -0 - 2, #Sunday
  }
  return str((dt_date + timedelta(days=difference[dt_date.weekday()])).date())
  
t_1 = lambda x: datetime.fromisoformat(x).weekday() == 4
def t():
  dates = [
    '2010-01-01',
    '2010-01-02',
    '2010-01-03',
    '2010-01-04',
    '2010-01-05',
    '2010-01-06',
    '2010-01-07',
    None
  ]
  list_z = list(map(f, dates))
  outs = list(map(t_1, list_z))
  return all(outs)
