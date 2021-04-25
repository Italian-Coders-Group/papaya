from io import BytesIO
from typing import List, Tuple

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
from core.dataclass import PapGame
from core.abc.games.TwoPlayersGame import TwoPlayersGame


# from core.database import get_game_id


def check_for_win(grid, sign):
	"""
	Questo dovrebbe essere la ricerca per i punti dato il segno che ha il giocatore.

	dovrebbe essere chiamata tipo Game.check_for_win(player1.sign) o qualcosa del genere
	:param grid:
	:param sign:
	:return:
	"""
	return ((grid[0][0] == sign and grid[0][1] == sign and grid[0][2] == sign) or
	        (grid[1][0] == sign and grid[1][1] == sign and grid[1][2] == sign) or
	        (grid[2][0] == sign and grid[2][1] == sign and grid[2][2] == sign) or
	        (grid[0][2] == sign and grid[1][2] == sign and grid[2][2] == sign) or
	        (grid[0][1] == sign and grid[1][1] == sign and grid[2][1] == sign) or
	        (grid[0][0] == sign and grid[1][0] == sign and grid[2][0] == sign) or
	        (grid[0][0] == sign and grid[1][1] == sign and grid[2][2] == sign) or
	        (grid[0][2] == sign and grid[1][1] == sign and grid[2][0] == sign))


def from1Dto2D(move: int):
	table = {
		'1': (0, 0),
		'2': (0, 1),
		'3': (0, 2),
		'4': (1, 0),
		'5': (1, 1),
		'6': (1, 2),
		'7': (2, 0),
		'8': (2, 1),
		'9': (2, 2)
	}
	return table[str(move)]


def from2Dto1D(pos: tuple):
	positions = {
		(0, 0): '1',
		(0, 1): '2',
		(0, 2): '3',
		(1, 0): '4',
		(1, 1): '5',
		(1, 2): '6',
		(2, 0): '7',
		(2, 1): '8',
		(2, 2): '9'
	}
	return positions[pos]


class TicTacToe(TwoPlayersGame):

	def __init__(self, player1: Member, player2: Member, gameID: str = None, data: dict = None):
		if data is None:
			self.player1 = TicTacToePlayer(player1.id, Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/x.png'), 'x')
			self.player2 = TicTacToePlayer(player2.id, Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/o.png'), 'o') if player2 is not None else AI(
				Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/o.png'), 'o')
			self.grid = [['', '', ''], ['', '', ''], ['', '', '']]
			self.turn = self.player2 if self.player2.user != 'AI' else self.player1
		else:
			self.parseData(data)

		self.players = cycle([self.player1, self.player2])
		self.gameID = gameID if gameID is not None else ''

	async def get_vs(self):
		"""
		This method is useless
		:return:
		"""
		return f'{self.player1.getUser()} vs {self.player2.getUser()}'

	async def nextTurn(self):
		"""
		This function returns the next player in the cycle.
		:return:
		"""
		return next(self.players)

	async def drawImage(self):
		"""
		This function saves the current state of
		:return:
		"""

		base_grid = Image.new('RGB', (156, 156), (255, 255, 255))
		draw = ImageDraw.Draw(base_grid)

		draw.line([50, 0, 50, 155], fill=(0, 0, 0), width=3)
		draw.line([103, 0, 103, 155], fill=(0, 0, 0), width=3)
		draw.line([0, 50, 155, 50], fill=(0, 0, 0), width=3)
		draw.line([0, 103, 155, 103], fill=(0, 0, 0), width=3)

		x = self.player1.symbol
		o = self.player2.symbol
		spacer = 53

		for i, row in enumerate(self.grid):
			for j, cell in enumerate(row):

				if cell == 'x':
					base_grid.paste(x, (i * spacer, j * spacer), x)
					print(f'Cell [{i}][{j}] is X')

				if cell == 'o':
					base_grid.paste(o, (i * spacer, j * spacer), o)
					print(f'Cell [{i}][{j}] is O')

		base_grid.save(f'{os.getcwd()}/modules/tic_tac_toe/src/tictactoe_images/{self.gameID}.png', format='PNG')
		# /var/www/papaya/papayabot/games/imagesToSend -> path on remote
		# {os.getcwd()}/modules/tic_tac_toe/src/imagesToSend -> path on windows
		return

	async def makeMove(self, coordinates: str) -> Tuple[BytesIO, int]:
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
		self.drawImage()
		self.grid, code = self.turn.makeMove(data=dataToPlayer)

		if code == 3:
			# indicates that the position is invalid, both as parameters or space available on the grid
			return code

		hasWon = check_for_win(self.grid, self.turn.sign)

		if hasWon:
			return self.drawImage(), 1

		for row in self.grid:
			for cell in row:
				if cell == '':
					v.append(cell)

		if len(v) == 0:
			tied = True

		if tied:
			self.drawImage()
			return 100

		self.turn = self.nextTurn()

		if self.turn.user == 'AI':
			dataToAI = {
				'grid': self.grid
			}

			aiMove = self.turn.makeMove(dataToAI)
			x, y = from1Dto2D(aiMove)

			self.grid[y][x] = self.turn.sign

			self.drawImage()

			aiWon = check_for_win(self.grid, self.turn.sign)
			if aiWon:
				code = 10
			else:
				self.turn = self.nextTurn()
				code = 0
		return code

	async def getData(self) -> dict:
		"""
		This function makes a dict with the useful info about the game.
		:return:
		"""
		data = {
			'player1ID': self.player1.user,
			'player2ID': self.player2.user,
			'currentTurn': self.turn.user,
			'grid': self.grid
		}
		return data

	async def parseData(self, data: PapGame):
		"""
		If data is passed the init is from this instead of passed args.
		:param data:
		:return:
		"""
		gameData = data.gameData
		gameID = data.gameID

		self.gameID = gameID
		self.player1 = TicTacToePlayer(gameData['player1ID'], Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/x.png'), 'x')
		if gameData['player2ID'] == 0:
			self.player2 = AI(Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/o.png'), 'o')
		else:
			self.player2 = TicTacToePlayer(gameData['player2ID'], Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/o.png'), 'o')

		if gameData['currentTurn'] == gameData['player1ID']:
			self.turn = TicTacToePlayer(gameData['player1ID'], Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/x.png'), 'x')
		else:
			self.turn = TicTacToePlayer(gameData['player2ID'], Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/o.png'),
			                            'o')
		# else:
		#     self.turn = AI(Image.open(f"{os.getcwd()}\\modules\\tic_tac_toe\\src\\o.png"), "o")

		self.grid = gameData['grid']
