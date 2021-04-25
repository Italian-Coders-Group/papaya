from abc import ABCMeta, abstractmethod
from .player import Player
from itertools import cycle
from io import BytesIO
from typing import List, Tuple
from discord import Member


# First iteration with this type of abc.

class TwoPlayersGame(metaclass=ABCMeta):

	@abstractmethod
	async def nextTurn(self) -> Player:
		"""
		This function returns the next player in the cycle.
		:return: TicTacToePlayer
		"""
		pass

	@abstractmethod
	async def drawImage(self) -> BytesIO:
		"""
		This function returns a byte buffer containing the new image
		and saves it for URL
		:return: BytesIO
		"""
		pass

	@abstractmethod
	async def makeMove(self, coordinates: List) -> Tuple[BytesIO, int]:
		"""
		This funcions takes in the coordinates of the move, transaltes them
		and returns a bytes buffer and a code.
		:param coordinates:
		:return:
		"""
		pass

	@abstractmethod
	async def getData(self) -> dict:
		"""
		This function makes a dict with the useful info about the game.
		:return:
		"""
		pass

	@abstractmethod
	async def parseData(self, data: dict):
		"""
		If data is passed the init is from this instead of passed args.
		:param data:
		:return:
		"""
		pass