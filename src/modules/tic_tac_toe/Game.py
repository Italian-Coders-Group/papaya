from io import BytesIO
from typing import List, Tuple

from discord import Member
from .Player import Player
from .AI import AI
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


def get_coords(inputValue: str):

	possible_coords = {
		'tl': (0, 0),
		'11': (0, 0),
		'topleft': (0, 0),
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
			self.player1 = Player(player1.id, Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/x.png'), 'x')
			self.player2 = Player(player2.id, Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/o.png'), 'o') if player2 is not None else AI(
				Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/o.png'), 'o')
			self.grid = [['', '', ''], ['', '', ''], ['', '', '']]
			self.turn = self.player2 if self.player2.user != 'AI' else self.player1
		else:
			self.parseData(data)

		self.players = cycle([self.player1, self.player2])
		self.gameID = gameID if gameID is not None else ''

	async def get_vs(self):
		return f'{self.player1} vs {self.player2}'

	async def nextTurn(self) -> Player:
		"""
		This function returns the next player in the cycle.
		:return: Player
		"""
		return next(self.players)

	async def drawImage(self) -> BytesIO:
		"""
		This function returns a byte buffer containing the new image
		and saves it for URL
		:return: BytesIO
		"""
		buffer = io.BytesIO()

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

		base_grid.save(buffer, format='PNG')
		base_grid.save(f'/var/www/papaya/papayabot/games/imagesToSend/{self.gameID}.png', format='PNG')
		# /var/www/papaya/papayabot/games/imagesToSend -> path on remote
		# {os.getcwd()}/modules/tic_tac_toe/src/imagesToSend -> path on windows

		buffer.seek(0)
		return buffer

	async def makeMove(self, coordinates: List) -> Tuple[BytesIO, int]:
		"""
		This funcions takes in the coordinates of the move, transaltes them
		and returns a bytes buffer and a code.
		:param coordinates:
		:return:
		"""
		old_board = self.compile_image()
		posX, posY = get_coords(pos)
		tied = False
		v = []
		if self.grid[posY][posX] == '':
			self.grid[posY][posX] = self.turn.sign
		else:
			return old_board, 3

		for row in self.grid:
			for cell in row:
				if cell == '':
					v.append(cell)

		if len(v) == 0:
			tied = True

		if tied:
			new_board = self.compile_image()
			return new_board, 100

		hasWon = check_for_win(self.grid, self.turn.sign)
		if not hasWon:
			self.turn = self.player2
			if self.turn.user == 'AI':
				y, x = self.compMove()

				self.grid[y][x] = self.turn.sign
				new_board = self.compile_image()
				aiWon = check_for_win(self.grid, 'o')
				if aiWon:
					code = 10
				else:
					self.turn = self.player1
					code = 0
			return new_board, code
		else:
			code = 1
		new_board = self.compile_image()
		return new_board, code

	async def compMove(self):
		"""
		This function returns a move made by the AI.
		:return:
		"""
		possibleMoves = []
		for i, row in enumerate(self.grid):
			for j, cell in enumerate(row):
				if cell == '':
					possibleMoves.append(from2Dto1D((i, j)))
		move = 0

		# Check for possible winning move to take or to block opponents winning move
		for sign in ['o', 'x']:
			for possibleMove in possibleMoves:
				boardCopy = [[],
				             [],
				             []]
				for y, row in enumerate(self.grid):
					for x, cell in enumerate(row):
						boardCopy[y].append(cell)
				posY, posX = from1Dto2D(possibleMove)
				boardCopy[posY][posX] = sign
				if check_for_win(boardCopy, sign):
					move = possibleMove
					return from1Dto2D(move)

		# Try to take one of the corners
		cornersOpen = []
		for i in possibleMoves:
			if i in ['1', '3', '7', '9']:
				cornersOpen.append(i)
		if len(cornersOpen) > 0:
			move = choice(cornersOpen)
			return from1Dto2D(move)

		# Try to take the center
		if 5 in possibleMoves:
			move = 5
			return from1Dto2D(move)

		# Take any edge
		edgesOpen = []
		for i in possibleMoves:
			if i in ['2', '4', '6', '8']:
				edgesOpen.append(i)

		if len(edgesOpen) > 0:
			move = choice(edgesOpen)

		return from1Dto2D(move)

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

	async def parseData(self, data: dict):
		"""
		If data is passed the init is from this instead of passed args.
		:param data:
		:return:
		"""
		gameData: PapGame = data.gameData
		gameID: PapGame = data.gameID
		self.gameID = gameID
		self.player1 = Player(gameData['player1ID'], Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/x.png'), 'x')
		if gameData['player2ID'] == 0:
			self.player2 = AI(Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/o.png'), 'o')
		else:
			self.player2 = Player(gameData['player2ID'], Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/o.png'), 'o')

		if gameData['currentTurn'] == gameData['player1ID']:
			self.turn = Player(gameData['player1ID'], Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/x.png'), 'x')
		else:
			self.turn = Player(gameData['player2ID'], Image.open(f'{os.getcwd()}/modules/tic_tac_toe/src/o.png'),
			                   'o')
		# else:
		#     self.turn = AI(Image.open(f"{os.getcwd()}\\modules\\tic_tac_toe\\src\\o.png"), "o")

		self.grid = gameData['grid']