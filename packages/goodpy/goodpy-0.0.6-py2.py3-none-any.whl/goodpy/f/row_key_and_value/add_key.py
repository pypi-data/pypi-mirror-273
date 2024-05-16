from pyspark.rdd import RDD
from pyspark.sql import Row
from typing import Any

def f(x: RDD, key: str, value: Any, add_to_front=False):
  if add_to_front:
    x = x.asDict()
    y = {key:value}
    y.update(x)
    return Row(**y)
  else:
    x = x.asDict()
    x[key] = value
    return Row(**x)

t = lambda: f(Row(a='a'), 'b', 'b') == Row(a='a', b='b')
