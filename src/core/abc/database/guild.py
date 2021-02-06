from abc import ABCMeta, abstractmethod
from typing import List, Optional

from core.abc.database.database import AbstractDatabase
from core.dataclass import PapGame, PapUser


class AbstractGuild(metaclass=ABCMeta):

	guildID: int
	db: AbstractDatabase

	def __init__(self, guildID: int, db: AbstractDatabase):
		self.guildID = guildID
		self.db = db

	@abstractmethod
	def getGame( self, gameID: str ) -> PapGame:
		pass

	@abstractmethod
	def setGame( self, gameID: str, game: PapGame ):
		pass

	@abstractmethod
	def getUser( self, userID: int ) -> PapUser:
		pass

	@abstractmethod
	def hasGame( self, gameID: str ):
		pass

	@abstractmethod
	def hasUser( self, userID: int ):
		pass

	@abstractmethod
	def getGamesForUser( self, userID: int, user: Optional[PapUser] = None ) -> List[PapGame]:
		pass
