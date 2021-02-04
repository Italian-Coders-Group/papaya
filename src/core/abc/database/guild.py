from abc import ABCMeta, abstractmethod
from typing import Any, Dict

from core.abc.database.database import AbstractDatabase
from core.dataclass import PapGame, PapUser


class AbstractGuild(metaclass=ABCMeta):

	guild: int
	db: AbstractDatabase

	def __init__(self, guildId: int, db: AbstractDatabase):
		self.guild = guildId
		self.db = db

	@abstractmethod
	def getGame( self, gameId: str ) -> PapGame:
		pass

	@abstractmethod
	def setGame( self, gameId: str, game: PapGame ):
		pass

	@abstractmethod
	def getMember( self, userId: int ) -> PapUser:
		pass
