import os
from core.abc.games.player import Player
from PIL import Image
from discord import Member
from typing import Dict


def convertCoords(inputValue: str):

	possible_coords = {
		'tl': (0, 0),
		'11': (0, 0),
		'topleft': (0, 0),
		'1': (0, 0),
		't': (0, 1),
		'top': (0, 1),
		'12': (0, 1),
		'tr': (0, 2),
		'topright': (0, 2),
		'13': (0, 2),
		'ml': (1, 0),
		'middleleft': (1, 0),
		'midleft': (1, 0),
		'21': (1, 0),
		'mid': (1, 1),
		'middle': (1, 1),
		'22': (1, 1),
		'mr': (1, 2),
		'middleright': (1, 2),
		'midright': (1, 2),
		'23': (1, 2),
		'bl': (2, 0),
		'bottomleft': (2, 0),
		'31': (2, 0),
		'bottom': (2, 1),
		'b': (2, 1),
		'32': (2, 1),
		'br': (2, 2),
		'bottomright': (2, 2),
		'33': (2, 2)
	}

	for key in possible_coords.keys():
		if inputValue == key:
			return possible_coords[key]

	return None, None


class TicTacToePlayer(Player):

	def __init__(self, user: int, symbol: Image, sign: str):
		self.user = user
		self.symbol = symbol
		self.sign = sign

	def makeMove(self, data: Dict):
		grid = data['grid']
		coords = data['coords']

		posY, posX = convertCoords(coords)

		if (posX is None) and (posY is None):
			return grid, 3

		if grid[posY][posX] == '':
			grid[posY][posX] = self.sign
		else:
			return grid, 2

		return grid, 0

	def getUser( self ):
		return self.user