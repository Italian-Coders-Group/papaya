import os
from core.abc.games.player import Player
from PIL import Image
from discord import Member


class Player(Player):

    def __init__(self, user: Member, symbol: Image, sign: str):
        super().__init__(user, symbol, sign)

    def getUser( self ):
        return self.user