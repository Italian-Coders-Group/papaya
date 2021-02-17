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
		"""
		Returns a PapGame object with the requested ID
		:param gameID: the ID to search for
		:return: the PapGame object
		"""
		pass

	@abstractmethod
	def setGame( self, game: PapGame ) -> None:
		"""
		Update the database by adding this game or by updating the saved game with this one
		:param game: a PapGame object with new values
		"""
		pass

	@abstractmethod
	def getUser( self, userID: int ) -> PapUser:
		"""
		NOT IMPLEMENTED
		:param userID:
		:return:
		"""
		pass

	@abstractmethod
	def hasGame( self, gameID: str, checkCache: bool = True, gameType: Optional[str] = 'any' ) -> bool:
		"""
		Checks if has a game with that ID
		:param gameID: the game ID to search for
		:param checkCache: True if should check the cache too
		:param gameType: the type of the game to search, optional, can make searching faster
		:return: True if we have it
		"""
		pass

	@abstractmethod
	def hasUser( self, userID: int ) -> bool:
		"""
		NOT IMPLEMENTED
		:param userID:
		:return:
		"""
		pass

	@abstractmethod
	def getGamesForUser( self, userID: int, gameType: str = 'any', user: Optional[PapUser] = None ) -> List[PapGame]:
		"""
		Returns a list with all games that this user has played
		:param gameType: the type of the game, use "any" for any type
		:param userID: the user to get the games from, put None if use use a PapUser in the user param
		:param user: ALTERNATIVE: a PapUser
		:return: list of games
		"""
		pass

	@abstractmethod
	def getLiveGameForUser( self, userID: int, gameType: str = 'any', user: Optional[ PapUser ] = None ) -> List[ PapGame ]:
		"""
		Returns a list with all live games that this user is playing
		:param gameType: the type of the game, use "any" for any type
		:param userID: the user to get the games from, put None if use use a PapUser in the user param
		:param user: ALTERNATIVE: a PapUser
		:return: list of games
		"""
		pass

	@abstractmethod
	def getStatsForUserInGuild(self, userID: int, guildID: str, gameType: str = 'any') -> PapUser:
		"""
		Returns a user in the guild with his stats, None if not found
		:param userID:
		:param guildID:
		:param gameType:
		:return: user
		"""
