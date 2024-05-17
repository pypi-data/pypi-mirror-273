from pyspark.sql import Row
from typing import List

def f(row: Row, keys: List[str])->Row: return Row(**{key: row[key] for key in keys})
def t(): return f(Row(a=1, b=2, c=3), ['a', 'b']) == Row(a=1, b=2)
