from types import FunctionType
from typing import List, Union, Awaitable

Event = str
Coroutine = Union[FunctionType, Awaitable]
ListenerList = List[Coroutine]
