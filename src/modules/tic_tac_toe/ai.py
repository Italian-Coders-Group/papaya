from core.abc.games.Player import player
from typing import List, Tuple, Dict


class TicTacToeAI(player):

    def __init__(self):
        self.ai = True

    def makeMove(self, gameData: Dict) -> Dict:
        pass
