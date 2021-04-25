from abc import ABCMeta, abstractmethod
from discord import Member
from os import path
from typing import Dict


# I have no idea what to put in this abc tbh :/
class Player(metaclass=ABCMeta):

	@abstractmethod
	def makeMove(self, data: Dict) -> int:
		"""
		This function returns a move number to be interpeted by the game.

		:param data:
		:return:
		"""
		pass
