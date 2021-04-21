from abc import ABCMeta, abstractmethod
from typing import List


class Ai(metaclass=ABCMeta):

    @abstractmethod
    def calculateMove(self, gameGrid: List[ List ] = [[]]) -> int:
        """
        This funcion takes the game grid and calculates the move to make. Then returns a number to be translated by the game.
        """
        pass
