from typing import Callable
from typing import Iterable

f : Callable[[Iterable[str], str], str] = lambda iterable, seperator: seperator.join(iterable)
t : Callable[[], bool] = lambda: f(['1', '2', '3'], '_') == '1_2_3'
