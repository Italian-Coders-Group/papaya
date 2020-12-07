import os
import math
from typing import List, Mapping


class BaseGrid:

    def __init__(self, width: int, height: int):
        self.grid = [[None for _ in range(width)] for _ in range(height)]