import discord
import os
from .Player import Player
from itertools import cycle


class Game:

    def __init__(self, player1: discord.Member, player2: discord.Member):
        self.player1 = Player(player1.id, player1.display_name, "x")
        self.player2 = Player(player2.id, player2.display_name, "o")
        self.players = cycle([self.player1, self.player2])
        self.turn = self.cycle_turn()

    def cycle_turn(self):

        return next(self.players)



