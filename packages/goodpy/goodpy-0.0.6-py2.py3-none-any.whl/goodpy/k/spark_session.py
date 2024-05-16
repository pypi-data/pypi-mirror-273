from pyspark.sql import SparkSession as Session
from goodpy.f.dirpath.mkdir import f as mkdir
from .spark_context import SparkContext
from .spark_conf import SparkConf
from typing import Callable
from shutil import rmtree
from os import getcwd

class SparkSession(Session):
  def __init__(self, spark_context: SparkContext = None, config: SparkConf=None):
    config = SparkConf() if config is None else config
    sc = SparkContext(config=config)
    Session.__init__(self, sc)

f : Callable[[dict], Session] = lambda x={}: SparkSession(**x)

def t()->bool:
  spark = f()
  spark = f()
  x = [(1, 1), (2, 2), (3, 3)]
  x = spark.sparkContext.parallelize(x)
  df = spark.createDataFrame(x)
  tmp_dir = mkdir(getcwd() + '/test_spark.parquet')
  df.write.parquet(tmp_dir, mode='overwrite')
  df2 = spark.read.parquet(tmp_dir)
  df2.count()
  rmtree(tmp_dir)
  return True
