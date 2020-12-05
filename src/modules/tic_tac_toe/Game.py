import discord
from .Player import Player
from itertools import cycle
from games.abc.baseGame import BaseGame


class Game(BaseGame):

    def __init__(self, player1: discord.Member, player2: discord.Member):
        self.player1 = Player(player1, "x")
        self.player2 = Player(player2, "o")
        self.players = cycle([self.player1, self.player2])
        self.turn = self.processTurn("data")

    def processTurn( self, data ):

        return next(self.players)

    def get_vs(self):
        return f"{self.player1} vs {self.player2}"



