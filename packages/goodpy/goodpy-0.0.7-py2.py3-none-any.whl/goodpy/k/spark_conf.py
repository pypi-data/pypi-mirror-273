from goodpy.f.iterable_and_seperator.concat import f as concat
from goodpy.f.dirpath.mkdir import f as mkdir
from pyspark.conf import SparkConf as Conf
from typing_extensions import Self as S
from os.path import expanduser as e
from typing import Callable

c = concat
m = mkdir
p = property
C = Callable

class SparkConf(Conf):
  def __init__(
    s: S,
    app_name='n',
    num_cores: str='*',
    executor_memory: str ='20g',
    driver_memory: str='20g',
    dir: str=None
  ):
    Conf.__init__(s)
    
    s._dir = dir = m(c([m(e('~/.data')), 'spark'], '/')) if dir is None else dir
    s.setMaster('local[{}]'.format(num_cores))
    s.setAppName(app_name)
    s.set('spark.sql.warehouse.dir', s.dir_warehouse)
    s.set('spark.driver.bindAddress', '127.0.0.1')
    s.set('spark.driver.extraJavaOptions', s.d_o)
    s.set('spark.executor.memory', executor_memory)
    s.set('spark.driver.memory', driver_memory)
    s.set('spark.executor.allowSparkContext', 'true')
    s.set('spark.sql.catalogImplementation', 'hive')
    

  dir           : C[[S], str] = p(lambda s: s._dir)
  dir_warehouse : C[[S], str] = p(lambda s: m(c([s.dir, 'warehouse'], '/')))
  dir_derby     : C[[S], str] = p(lambda s: m(c([s.dir, 'derby'], '/')))
  setting       : C[[S], str] = p(lambda s: '-Dderby.system.home')
  d_o           : C[[S], str] = p(lambda s: c([s.setting, s.dir_derby], '='))
  
def f(x: dict={})->SparkConf: return SparkConf(**x)
def t(): return f(
  {
    'num_cores': '4',
    'executor_memory': '2g',
    'driver_memory': '2g'
  }
)
