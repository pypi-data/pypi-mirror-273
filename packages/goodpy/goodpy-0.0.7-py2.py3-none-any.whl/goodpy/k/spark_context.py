from pyspark.context import SparkContext as Context
from pyspark.serializers import CPickleSerializer
from goodpy.k.spark_conf import SparkConf

class SparkContext(Context):
  def __init__(self, config: SparkConf=None):
    config = config if config is not None else SparkConf()
    with self._lock:
      if self._active_spark_context is None:
        Context.__init__(self, conf=config)
      else:
        self._do_init(
          self._active_spark_context.master,
          self._active_spark_context.appName,
          self._active_spark_context.sparkHome,
          None,
          self._active_spark_context.environment,
          self._active_spark_context._batchSize,
          CPickleSerializer(),
          config,
          self._active_spark_context._jsc,
        )
        
def f(x: dict={})->SparkContext: return SparkContext(**x)

def t():
  sc1 = f()
  sc1.parallelize([1, 2, 3]).collect()
  sc2 = f()
  sc2.parallelize([1, 2, 3]).collect()
  return True
