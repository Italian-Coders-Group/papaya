from io import BytesIO
from typing import List, Tuple, Dict, Union, Iterator

from discord import Member

from .TicTacToePlayer import TicTacToePlayer
from .TicTacToeAi import TicTacToeAI
from random import choice
from itertools import cycle
from games.abc.baseGame import BaseGame
import io
import os
from PIL import Image, ImageDraw
from .Grid import Grid
from core import utils
from core.dataclass.PapGame import PapGame
from core.abc.games.TwoPlayersGame import TwoPlayersGame
from .gameUtils import check_for_win, from1Dto2D, from2Dto1D, positionToPixel


# from core.database import get_game_id


class TicTacToe(TwoPlayersGame):

	def __init__(self, player1: Member or None, player2: Member or None, gameID: str, data: PapGame = None):
		if data is None:
			self.player1 = TicTacToePlayer(player1.id, Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/x.png'), 'x')
			self.player2 = TicTacToePlayer(player2.id, Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/o.png'), 'o') if player2 is not None \
							else TicTacToeAI('AI',
			                                                                                                                                                    Image.open(
				                                                                                                                                                    f'{os.getcwd()}/modules/tic_tac_toe/src/o.png'),
			                                                                                                                                                    'o')
			self.grid = [['', '', ''], ['', '', ''], ['', '', '']]
			self.turn = self.player2 if self.player2.user != 'AI' else self.player1
		else:
			self.parseData(data)

		self.players = iter([self.player1, self.player2])
		self.gameID = gameID

	def get_vs(self):
		"""
		This method is useless
		:return:
		"""
		return f'{self.player1.getUser()} vs {self.player2.getUser()}'

	def nextTurn(self):
		"""
		This function returns the next player in the cycle.
		:return:
		"""
		if self.turn.user == self.player1.user:
			self.turn = self.player2
		else:
			self.turn = self.player1

		# raise NotImplementedError('turn error')

	def drawImage(self, cells: List[ int ] = None):
		"""
		This funcions saves the image drawn
		"""

		positions = []

		if not cells:
			pass
		else:
			for cell in cells:
				positions.append(positionToPixel(from1Dto2D(cell)))

		base_grid = Image.new('RGBA', (156, 156), (255, 255, 255, 255))
		draw = ImageDraw.Draw(base_grid)

		draw.line([51, 0, 51, 155], fill=(0, 0, 0), width=3)
		draw.line([104, 0, 104, 155], fill=(0, 0, 0), width=3)
		draw.line([0, 51, 155, 51], fill=(0, 0, 0), width=3)
		draw.line([0, 104, 155, 104], fill=(0, 0, 0), width=3)

		x = self.player1.symbol
		o = self.player2.symbol

		for i, row in enumerate(self.grid):
			for j, cell in enumerate(row):
				posX, posY, *args = positionToPixel((i, j))
				if cell == 'x':
					base_grid.paste(x, (posX, posY), x)

				if cell == 'o':
					base_grid.paste(o, (posX, posY), o)

		if not positions:
			pass
		else:
			winBoxOverlay = Image.new('RGBA', size=(156, 156), color=(0, 0, 0, 0))
			winBoxDraw = ImageDraw.Draw(winBoxOverlay)

			for position in positions:
				x, y, x1, y1 = position
				winBoxDraw.rectangle(xy=[(x, y), (x1, y1)],
				                     fill=(0, 255, 0) + (150,))

			base_grid = Image.alpha_composite(base_grid, winBoxOverlay)

		base_grid.save(f'{os.getcwd()}/modules/tic_tac_toe/src/tictactoe_images/{self.gameID}.png', format='PNG')
		# /var/www/papaya/papayabot/games/imagesToSend -> path on remote
		# {os.getcwd()}/modules/tic_tac_toe/src/imagesToSend -> path on windows
		return

	def makeMove(self, coordinates: str) -> int:
		"""
		This funcions takes in the coordinates of the move, transaltes them
		and returns a bytes buffer and a code.
		:param coordinates:
		:return:
		"""
		dataToPlayer = {
			'grid': self.grid,
			'coords': coordinates
		}

		self.grid, code = self.turn.makeMove(data=dataToPlayer)

		if code == 2:
			# This indicates that the position is not valid, as it's already been taken
			return code
		if code == 3:
			# indicates that the position is invalid, both as parameters or space available on the grid
			return code

		hasWon, cells = check_for_win(self.grid, self.turn.sign)

		if hasWon:
			self.drawImage(cells=cells)
			return 1

		v = []

		for row in self.grid:
			for cell in row:
				if cell == '':
					v.append(cell)

		if len(v) == 0:
			tied = True
		else:
			tied = False

		if tied:
			self.drawImage()
			return 100

		self.nextTurn()

		if self.turn.user == 'AI':
			dataToAI = {
				'grid': self.grid
			}

			aiMove = self.player2.makeMove(dataToAI)
			y, x = from1Dto2D(aiMove)
			self.grid[y][x] = self.turn.sign

			aiWon, cells = check_for_win(self.grid, self.turn.sign)
			if aiWon:
				self.drawImage(cells=cells)
				return 10
			else:
				self.nextTurn()
				code = 0
		self.drawImage()
		return code

	def getData(self) -> Dict:
		"""
		This function makes a dict with the useful info about the game.
		:return:
		"""
		# TODO: MAKE THIS RETURN DIRECTLY THE PAPGAME OBJECT
		data = {
			'player1ID': self.player1.user,
			'player2ID': self.player2.user,
			'currentTurn': self.turn.user,
			'grid': self.grid
		}
		return data

	def parseData(self, data: PapGame):
		"""
		If data is passed the init is from this instead of passed args.
		:param data:
		:return:
		"""
		gameData = PapGame.deserializeGameData(data.gameData)
		gameID = data.gameID

		self.gameID = gameID
		self.player1 = TicTacToePlayer(gameData['player1ID'], Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/x.png'), 'x')
		if gameData['player2ID'] == 'AI':
			self.player2 = TicTacToeAI('AI', Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/o.png'), 'o')
		else:
			self.player2 = TicTacToePlayer(gameData['player2ID'], Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/o.png'), 'o')

		if gameData['currentTurn'] == gameData['player1ID']:
			self.turn = self.player1
		else:
			self.turn = self.player2
		# else:
		#     self.turn = AI(Image.open(f"{os.getcwd()}\\modules\\tic_tac_toe\\src\\o.png"), "o")

		self.grid = gameData['grid']
