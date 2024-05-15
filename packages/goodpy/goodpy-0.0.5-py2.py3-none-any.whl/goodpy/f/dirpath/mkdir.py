from goodpy.f.iterable_and_seperator.concat import f as c
from typing import Callable as T
from os.path import exists as e
from os import mkdir as m
from os import getcwd
from os import rmdir

f   : T[[str], str] = lambda path: [m(path) if not e(path) else None, path][1]
up  : T[[], str] = lambda: c([getcwd(), '__file__' + 'test'], '/')
dn  : T[[], None] = lambda: rmdir(c([getcwd(), '__file__' + 'test'], '/'))
t   : T[[], bool] = lambda: [e(f(up())), dn()][0]
