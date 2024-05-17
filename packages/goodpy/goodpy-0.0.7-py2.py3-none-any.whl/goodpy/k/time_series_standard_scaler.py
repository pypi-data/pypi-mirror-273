from goodpy.f.iterable_and_seperator.concat import f as concat
from sklearn.preprocessing import StandardScaler as SS
from pyspark.sql.functions import map_from_arrays
from pyspark.testing import assertDataFrameEqual
from goodpy.k.spark_session import SparkSession
from pyspark.ml.linalg import DenseMatrix as DM
from pyspark.sql.types import BooleanType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import StructField
from goodpy.k.dataframe import DataFrame
from pyspark.sql.types import StructType
from pyspark.ml.linalg import MatrixUDT
from pyspark.sql.types import ArrayType
from pyspark.sql.types import FloatType
from pyspark.sql.functions import udf
from pyspark.sql.functions import lit
from typing_extensions import Self
from dataclasses import dataclass
from dataclasses import field
from pyspark.sql import Row
from typing import Union
from numpy import array

schema = StructType(
  [
    StructField('with_mean', BooleanType(), nullable=False),
    StructField('with_std', BooleanType(), nullable=False),
    StructField('copy', BooleanType(), nullable=False),
    StructField('n_features_in_', IntegerType(), nullable=True),
    StructField('n_samples_seen_', IntegerType(), nullable=True),
    StructField('mean_', ArrayType(FloatType()), nullable=False),
    StructField('scale_', ArrayType(FloatType()), nullable=True),
    StructField('var_', ArrayType(FloatType()), nullable=True),
  ]
)

@udf(returnType=schema)
def fit_ts(x: DM, with_mean: bool, with_std: bool)->SS:
  scaler = SS(with_mean=with_mean, with_std=with_std)
  scaler.fit(x.toArray())
  dict_params = scaler.__dict__
  dict_params['n_features_in'] = int(scaler.n_features_in_)
  dict_params['n_samples_seen_'] = int(scaler.n_samples_seen_)
  dict_params['mean_'] = scaler.mean_.tolist()
  dict_params['var_'] = scaler.var_.tolist()
  dict_params['scale_'] = scaler.scale_.tolist()
  return dict_params

@udf(returnType=MatrixUDT())
def transform_ts(x: DM, scaler_dict: Row):
  scaler = SS(
    copy=True,
    with_mean=scaler_dict['with_mean'],
    with_std=scaler_dict['with_std']
  )
  scaler.n_features_in_ = array(scaler_dict['n_features_in_'])
  scaler.n_samples_seen_ = array(scaler_dict['n_samples_seen_'])
  scaler.mean_ = array(scaler_dict['mean_'])
  scaler.var_ = array(scaler_dict['var_'])
  scaler.scale_ = array(scaler_dict['scale_'])
  z = DM(x.numRows, x.numCols, scaler.transform(x.toArray()).T.flatten().tolist())
  return z

@udf(returnType=MatrixUDT())
def inverse_transform_ts(x: DM, scaler_dict: dict):
  scaler = SS(
    copy=True,
    with_mean=scaler_dict['with_mean'],
    with_std=scaler_dict['with_std']
  )
  scaler.n_features_in_ = array(scaler_dict['n_features_in_'])
  scaler.n_samples_seen_ = array(scaler_dict['n_samples_seen_'])
  scaler.mean_ = array(scaler_dict['mean_'])
  scaler.var_ = array(scaler_dict['var_'])
  scaler.scale_ = array(scaler_dict['scale_'])
  z_numpy = scaler.inverse_transform(x.toArray())
  z = DM(x.numRows, x.numCols, z_numpy.T.flatten().tolist())
  return z

@udf(returnType=MatrixUDT())
def fit_transform_ts(x: DM, with_mean: bool, with_std: bool) -> SS:
  scaler = SS(with_mean=with_mean, with_std=with_std)
  z_numpy = scaler.fit_transform(x.toArray())
  return DM(x.numRows, x.numCols, z_numpy.T.flatten().tolist())
  
@dataclass 
class TimeSeriesStandardScaler:
  in_col      : str
  out_col     : str
  with_mean   : bool = True
  with_std    : bool = True
   
  wm = property(lambda s: lit(s.with_mean))
  ws = property(lambda s: lit(s.with_std))
  
  def fit(s: Self, df: DataFrame):
    x = df.select('id', s.in_col)
    s.parameters = df.add_col('parameters', fit_ts(s.in_col, s.wm, s.ws))
    s.parameters = s.parameters.select('id', 'parameters')
    s.parameters = DataFrame(s.parameters, s.parameters.sparkSession)
    return s
  
  def transform(s: Self, df: DataFrame):
    df = DataFrame(df.join(s.parameters, on='id', how='inner'), df.sparkSession)
    df = df.add_col(s.out_col, transform_ts(s.in_col, 'parameters'))
    df = df.drop('parameters')
    return DataFrame(df, df.sparkSession)
  
  def fit_transform(s: Self, df: DataFrame):
    return df.add_col(s.out_col, fit_transform_ts(s.in_col, s.wm, s.ws))
  
  def inverse_transform(s: Self, df: DataFrame):
    df = DataFrame(df.join(s.parameters, on='id', how='inner'), df.sparkSession)
    inverse_name = concat([s.in_col, 'recreated'], '_')
    df = df.add_col(
      inverse_name,
      inverse_transform_ts(s.out_col, 'parameters')
    )
    df = df.drop('parameters')
    return DataFrame(df, df.sparkSession)

def f(x: dict): return TimeSeriesStandardScaler(**x)

def t_fit(x: DataFrame, scaler: TimeSeriesStandardScaler): return scaler.fit(x)

def t_transform(x: DataFrame, scaler: TimeSeriesStandardScaler):
  z = scaler.transform(x)
  y = DataFrame(
    [
      Row(id=2, ts=DM(2, 2, [1, 2, 4, 5]), s_ts=DM(2, 2, [-1, 1, -1, 1])),                                        
      Row(id=3, ts=DM(2, 2, [2, 3, 5, 6]), s_ts=DM(2, 2, [-1, 1, -1, 1])),
      Row(id=4, ts=DM(2, 2, [3, 4, 6, 7]), s_ts=DM(2, 2, [-1, 1, -1, 1]))
    ],
    SparkSession()
  )
  assertDataFrameEqual(y, z)
  return True

def t_inverse_transform(x: DataFrame, scaler: TimeSeriesStandardScaler):
  z = scaler.inverse_transform(x)
  y = DataFrame(
    [
      Row(id=2, s_ts=DM(2, 2, [-1, 1, -1, 1]), ts_recreated=DM(2, 2, [1, 2, 4, 5])),                                        
      Row(id=3, s_ts=DM(2, 2, [-1, 1, -1, 1]), ts_recreated=DM(2, 2, [2, 3, 5, 6])),
      Row(id=4, s_ts=DM(2, 2, [-1, 1, -1, 1]), ts_recreated=DM(2, 2, [3, 4, 6, 7]))
    ],
    SparkSession()
  )
  assertDataFrameEqual(y, z)
  
def t_fit_transform(x: DataFrame, scaler: TimeSeriesStandardScaler):
  z = scaler.fit_transform(x)
  y = DataFrame(
    [
      Row(id=2, ts=DM(2, 2, [1, 2, 4, 5]), s_ts=DM(2, 2, [-1, 1, -1, 1])),                                        
      Row(id=3, ts=DM(2, 2, [2, 3, 5, 6]), s_ts=DM(2, 2, [-1, 1, -1, 1])),
      Row(id=4, ts=DM(2, 2, [3, 4, 6, 7]), s_ts=DM(2, 2, [-1, 1, -1, 1]))
    ],
    SparkSession()
  )
  assertDataFrameEqual(y, z)
  return True

def t():
  x1 = DataFrame(
    [
      Row(id=2, ts=DM(2, 2, [1, 2, 4, 5])),                                        
      Row(id=3, ts=DM(2, 2, [2, 3, 5, 6])),
      Row(id=4, ts=DM(2, 2, [3, 4, 6, 7]))
    ],
    SparkSession()
  )
  x2 = DataFrame(
    [
      Row(id=2, s_ts=DM(2, 2, [-1, 1, -1, 1])),                                        
      Row(id=3, s_ts=DM(2, 2, [-1, 1, -1, 1])),
      Row(id=4, s_ts=DM(2, 2, [-1, 1, -1, 1]))
    ],
    SparkSession()
  )
  
  scaler = t_fit(x1, TimeSeriesStandardScaler('ts', 's_ts'))
  t_transform(x1, scaler)
  t_inverse_transform(x2, scaler)
  t_fit_transform(x1, scaler)
  return True

