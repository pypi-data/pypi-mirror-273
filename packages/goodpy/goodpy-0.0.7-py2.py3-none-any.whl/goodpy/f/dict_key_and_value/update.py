def f(x: dict, key: str, value: str):
  x[key] = value
  return x

def t()->bool: return f({'a': 'a'}, 'a', 'b') == {'a': 'b'}
