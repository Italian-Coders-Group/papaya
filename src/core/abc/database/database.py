from abc import ABCMeta, abstractmethod
from typing import List, Any, Dict

from core.database.backends import AbstractBackend


class Member:

	def __init__(self, data: dict):
		self.uuid = data['uuid']
		self.permissions = data['permissions']

	uuid: int
	permissions: int


class Game:

	def __init__(self, data: dict):
		self.players = data['players']
		self.data = data['data']

	players: List[Member]
	data: Dict[str, Any]


class Guild:

	def __init__(self, data: dict):
		self.members = data['members']
		self.games = data['games']

	members: List[Member]
	games: List[Game]


class AbstractDatabase(metaclass=ABCMeta):

	backend: AbstractBackend

	@abstractmethod
	def getGuild( self, guild: int ) -> Guild:
		pass

	@abstractmethod
	def updateGameToGuild( self, game: Game ) -> None:
		pass
