from pyspark.sql.dataframe import DataFrame as PySparkDataFrame
from goodpy.f.iterable_and_seperator.concat import f as concat
from pyspark.sql.functions import collect_list as collect
from pyspark.ml.feature import VectorAssembler as V
from pyspark.testing import assertDataFrameEqual
from sklearn.preprocessing import StandardScaler
from pyspark.ml.linalg import DenseMatrix as DM
from pyspark.ml.linalg import DenseVector as DV
from goodpy.k.spark_session import SparkSession
from sklearn.preprocessing import RobustScaler
from pyspark.sql.types import BooleanType
from pyspark.sql.functions import explode
from pyspark.sql.functions import struct
from pyspark.sql.functions import array
from numpy import array as numpy_array
from pyspark.sql.types import ArrayType
from pyspark.ml.linalg import MatrixUDT
from pyspark.sql.types import LongType
from pyspark.sql.functions import udf
from pyspark.sql.functions import lit
from pyspark.sql.functions import col
from typing_extensions import Self
from pyspark.sql import Column
from functools import partial
from pyspark.sql import Row
from typing import Union
from typing import List

shift = udf(lambda x, n: x + n, LongType())
gen_window = udf(lambda x, n: [x + i for i in range(n)], ArrayType(LongType()))
check_len  = udf(lambda x, n: len(x) == n, BooleanType())
c = partial(concat, seperator='-')

@udf(returnType=MatrixUDT())
def to_dense_matrix(x: list[list[float]]):
  x = numpy_array(x)
  return DM(x.shape[0], x.shape[1], x.T.flatten().tolist())

class DataFrame(PySparkDataFrame):
  def __init__(
    self,
    data: Union[list, tuple, dict, PySparkDataFrame, 'DataFrame'],
    spark_session: SparkSession):
    if type(data) in [PySparkDataFrame, DataFrame]: df = data
    else: df = spark_session.createDataFrame(data)
    super().__init__(df._jdf, df.sparkSession)
    
  def add_vector_col(
    s: Self,
    in_cols: List[Union[Column, str]],
    out_col_name: str
  ) -> 'DataFrame':
    return DataFrame(
      V(inputCols=in_cols, outputCol=out_col_name).transform(s),
      s.sparkSession
    )
  
  def add_col(s: Self, col_name: str, col: Column ) -> 'DataFrame':
    return DataFrame(super().withColumn(col_name, col), s.sparkSession)

  def add_array_col(
    s: Self,
    in_cols: List[Union[Column, str]],
    out_col_name: str
  ) -> 'DataFrame':
    return DataFrame(s.add_col(out_col_name, array(*in_cols)), s.sparkSession)
  
  def add_struct_col(
    s: Self,
    in_cols: List[Union[Column, str]],
    out_col_name: str
  ) -> 'DataFrame':
    return DataFrame(s.add_col(out_col_name, struct(*in_cols)), s.sparkSession)
  
  def add_shifted_col(
    s: Self,
    in_col: List[Union[Column, str]],
    shift_size: int,
    out_col_name: str
  ) -> 'DataFrame':
    shifted_df = s.add_col('id', shift('id', lit(shift_size)))
    shifted_df = shifted_df.select('id', col(in_col).alias(out_col_name))
    return DataFrame(s.join(shifted_df, on='id', how='inner'), s.sparkSession)
  
  def add_ts_col(
    s: Self,
    in_col: Union[str, Column],
    window_size: int,
    out_col_name: str
  ) -> 'DataFrame':
    df = s.add_vector_col([in_col], 'vector')
    df_flatmap = df.add_col('id', explode(gen_window('id', lit(window_size))))
    df_ts = df_flatmap.groupBy('id').agg(collect('vector').alias(out_col_name))
    df_ts = DataFrame(df_ts.filter(check_len(out_col_name, lit(window_size))), s.sparkSession)
    df_ts = df_ts.add_col(out_col_name, to_dense_matrix(out_col_name))
    return DataFrame(s.join(df_ts, on='id', how='inner'), s.sparkSession)
  
  add_time_series_col = add_ts_col
  
  def add_shifted_cols(
    s: Self,
    in_cols: list[Union[str, Column]],
    shift_size: int,
    out_col_names: list[str]
  ) -> 'DataFrame':
    
    cols = s.columns
    array_col_name = c(in_cols)
    s = s.add_array_col(in_cols, array_col_name)
    shifted_array_col_name = c([array_col_name] + ['shift', str(shift_size)])
    s = s.add_shifted_col(array_col_name, shift_size, shifted_array_col_name)
    shifted_col = col(shifted_array_col_name)
    cols += [shifted_col[i].alias(out_col_names[i]) for i in range(len(in_cols))]
    return DataFrame(s.select(cols), s.sparkSession)

  # def add_ts_cols(
  #   s: Self,
  #   in_cols: list[Union[str, Column]],
  #   shift_size: int,
  #   out_col_names: list[str]
  # ) -> 'DataFrame':
  #   cols = s.columns
  #   array_col_name = c(in_cols)
  #   s = s.add_array_col(in_cols, array_col_name)
  #   ts_array_col_name = c([array_col_name] + ['ts', str(shift_size)])
  #   s = s.add_ts_col(array_col_name, shift_size, ts_array_col_name)
  #   ts_col = col(ts_array_col_name)
  #   cols += [ts_col[i].alias(out_col_names[i]) for i in range(len(in_cols))]
  #   return DataFrame(s.select(cols), s.sparkSession)
  

def f(x: dict): return DataFrame(**x)

def t_add_vector_col(x: DataFrame) -> bool:
  z = x.add_vector_col(['o', 'o_and_c'], 'o_and_o_and_c')
  y = DataFrame(
    data=[
      Row(id=1, o=1, c=4, o_and_c=DV([1, 4]), o_and_o_and_c = DV([1, 1, 4])),
      Row(id=2, o=2, c=5, o_and_c=DV([2, 5]), o_and_o_and_c = DV([2, 2, 5])),
      Row(id=3, o=3, c=6, o_and_c=DV([3, 6]), o_and_o_and_c = DV([3, 3, 6])),
      Row(id=4, o=4, c=7, o_and_c=DV([4, 7]), o_and_o_and_c = DV([4, 4, 7]))
    ],
    spark_session=SparkSession()
  )
  assertDataFrameEqual(z, y)
  return True

def t_add_array_col(x: DataFrame) -> bool:
  z = x.add_array_col(['id', 'o'], 'array')
  y = DataFrame(
    [
      Row(id=1, o=1, c=4, o_and_c=DV([1, 4]), array=[1, 1]),
      Row(id=2, o=2, c=5, o_and_c=DV([2, 5]), array=[2, 2]),
      Row(id=3, o=3, c=6, o_and_c=DV([3, 6]), array=[3, 3]),
      Row(id=4, o=4, c=7, o_and_c=DV([4, 7]), array=[4, 4]),
    ],
    x.sparkSession
  )
  assertDataFrameEqual(z, y)
  return True

def t_add_struct_col(x: DataFrame) -> bool:
  z = x.add_struct_col(['id', 'o'], 'struct')
  y = DataFrame(
    [
      Row(id=1, o=1, c=4, o_and_c=DV([1, 4]), struct=Row(id=1, o=1)),                      
      Row(id=2, o=2, c=5, o_and_c=DV([2, 5]), struct=Row(id=2, o=2)),
      Row(id=3, o=3, c=6, o_and_c=DV([3, 6]), struct=Row(id=3, o=3)),
      Row(id=4, o=4, c=7, o_and_c=DV([4, 7]), struct=Row(id=4, o=4))
    ],
    x.sparkSession
  )
  assertDataFrameEqual(z, y)
  return True

def t_add_shifted_col_shift_up(x: DataFrame) -> bool:
    z = x.add_shifted_col('o', 2, 'shifted_o').sort('id')
    y = DataFrame(
      [
        Row(id=3, o=3, c=6, o_and_c=DV([3, 6]), shifted_o=1),
        Row(id=4, o=4, c=7, o_and_c=DV([4, 7]), shifted_o=2)
      ],
      x.sparkSession
    )
    assertDataFrameEqual(z, y)
    return True
  
def t_add_shifted_col_shift_down(x: DataFrame) -> bool:
  z = x.add_shifted_col('o', -2, 'shifted_o').sort('id')
  y = DataFrame(
    [
      Row(id=1, o=1, c=4, o_and_c=DV([1, 4]), shifted_o=3),                      
      Row(id=2, o=2, c=5, o_and_c=DV([2, 5]), shifted_o=4)
    ],
    x.sparkSession
  )
  assertDataFrameEqual(z, y)
  return True
  
def t_add_shifted_col(x: DataFrame) -> bool:
  return all([t_add_shifted_col_shift_up(x), t_add_shifted_col_shift_down(x)])

def t_add_ts_col_1(x: DataFrame) -> bool:
  y = DataFrame(
    [
      Row(id=2, o=2, c=5, o_and_c=DV([2, 5]), ts_o=DM(2, 1, [1, 2])),                                        
      Row(id=3, o=3, c=6, o_and_c=DV([3, 6]), ts_o=DM(2, 1, [2, 3])),
      Row(id=4, o=4, c=7, o_and_c=DV([4, 7]), ts_o=DM(2, 1, [3, 4]))
    ],
    x.sparkSession
  )
  z = x.add_ts_col('o', 2, 'ts_o')
  assertDataFrameEqual(z, y)
  return True

def add_ts_col_2(x: DataFrame) -> bool:
  z = x.add_ts_col('o_and_c', 2, 'ts_o_and_c')
  y = DataFrame(
    [
      Row(id=2, o=2, c=5, o_and_c=DV([2, 5]), ts_o_and_c=DM(2, 2, [1, 2, 4, 5])),                                        
      Row(id=3, o=3, c=6, o_and_c=DV([3, 6]), ts_o_and_c=DM(2, 2, [2, 3, 5, 6])),
      Row(id=4, o=4, c=7, o_and_c=DV([4, 7]), ts_o_and_c=DM(2, 2, [3, 4, 6, 7]))
    ],
    x.sparkSession
  )
  assertDataFrameEqual(y, z)
  return True
  
def t_add_ts_col(x: DataFrame) -> bool:
  return all([t_add_ts_col_1(x), add_ts_col_2(x)])

def t_single_column_tests(x):
  return all(
    [
      t_add_vector_col(x),
      t_add_array_col(x),
      t_add_struct_col(x),
      t_add_shifted_col(x),
      t_add_ts_col(x)
    ]
  )
  
def t_add_shifted_cols(x: DataFrame):
  z = x.add_shifted_cols(['o', 'c'], 2, ['shifted_o', 'shifted_c'])
  y = DataFrame(
    data=[
      Row(id=3, o=3, c=6, o_and_c = DV([3, 6]), shifted_o=1, shifted_c=4),
      Row(id=4, o=4, c=7, o_and_c = DV([4, 7]), shifted_o=2, shifted_c=5)
    ],
    spark_session=SparkSession()
  )
  assertDataFrameEqual(z, y)
  return True

def t_add_ts_cols(x: DataFrame):
  z = x.add_ts_cols(['o', 'c'], 2, ['ts_o', 'ts_c'])
  y = DataFrame(
    data=[
      Row(id=2, o=2, c=3, ts_o=[1, 2], ts_c=[2, 3]),
      Row(id=3, o=3, c=4, ts_o=[2, 3], ts_c=[3, 4]),
      Row(id=4, o=4, c=5, ts_o=[3, 4], ts_c=[4, 5])
    ],
    spark_session=SparkSession()
  )
  assertDataFrameEqual(z, y)
  return True
  
def t_multi_columns_tests(x):
  return all(
    [
      t_add_shifted_cols(x),
      # t_add_ts_cols(x)
    ]
  )
  
def t():
  x = DataFrame(
    data=[
      Row(id=1, o=1, c=4, o_and_c=DV([1, 4])),
      Row(id=2, o=2, c=5, o_and_c=DV([2, 5])),
      Row(id=3, o=3, c=6, o_and_c=DV([3, 6])),
      Row(id=4, o=4, c=7, o_and_c=DV([4, 7]))
    ],
    spark_session=SparkSession()
  )
  return all(
    [
      t_single_column_tests(x),
      t_multi_columns_tests(x)
    ]
  )
