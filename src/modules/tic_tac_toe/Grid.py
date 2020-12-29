from core.gridsystem.UnorderedGrid import BaseGrid


class Grid(BaseGrid):

    def __init__(self, width: int, height: int):
        self.grid = [[None for _ in range(width)] for _ in range(height)]


