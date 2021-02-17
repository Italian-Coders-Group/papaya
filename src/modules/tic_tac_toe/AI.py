import os
from PIL import Image
from random import random, choice
import platform
from math import inf as infinity
import time


conversionChart = {
            (0, 0): 1,
            (0, 1): 2,
            (0, 2): 3,
            (1, 0): 4,
            (1, 1): 5,
            (1, 2): 6,
            (2, 0): 7,
            (2, 1): 8,
            (2, 2): 9
        }

corners = [1, 3, 7, 9]
edges = [2, 4, 6, 8]


class AI:

    def __init__(self, symbol, sign: str):
        """
        Sarebbe utile storare nel db un Player_ID con un Guild_ID così da poter sperimentare con ledearboards o altro.

        Anche per vedere la storia dei game di un giocatore, anche questo forse è meglio metterlo in BasePlayer



        :param user:
        :param symbol:
        """

        self.user = "AI"
        self.sign = sign

        self.symbol = symbol
        self.simpleBoard = []

    def getUser(self):
        return "AI"

    def get_board_status(self, board):
        simpleBoard = []
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == self.sign:
                    simpleBoard.append(conversionChart[(i, j)])
                else:
                    simpleBoard.append(0)
        self.simpleBoard = simpleBoard
        return simpleBoard

    def choose_move(self):
        return

    def randomGen(self):
        return