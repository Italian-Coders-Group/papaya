from core.abc.games.AiPlayer import Ai
from typing import List, Tuple


class TicTacToeAI(Ai):

    def __init__(self):
        self.ai = True

    def calculateMove(self, gameGrid: List[ List ] = [[]]) -> int:
        """
        This funcion calculates a move and return a number to be transalted into a (x, y) value
        """
        # this is where the old compMove will take place.
