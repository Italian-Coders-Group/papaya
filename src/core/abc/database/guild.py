from abc import ABCMeta, abstractmethod
from typing import List, Optional

from core.abc.database.database import AbstractDatabase
from core.dataclass import PapStats
from core.dataclass.PapGame import PapGame
from core.dataclass.PapUser import PapUser


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
		Gets a PapUser from the user id
		:param userID: the discord id of the user
		:return: the corresponding PapUser user
		"""

	@abstractmethod
	def setUser( self, user: PapUser ) -> None:
		"""
		Update the database by adding this user or by updating the saved user with this one
		:param user: a PapUser object with new values
		"""

	@abstractmethod
	def hasGame( self, gameID: str, checkCache: bool = True, gameType: Optional[str] = 'any' ) -> bool:
		"""
		Checks if has a game with that ID
		:param gameID: the game ID to search for
		:param checkCache: True if should check the cache too
		:param gameType: the type of the game to search, optional, can make searching faster
		:return: True if we have it
		"""

	@abstractmethod
	def hasUser( self, userID: int, checkCache: bool = True ) -> bool:
		"""
		Checks if has an user with that ID
		:param userID: the user ID to search for
		:param checkCache: True if should check the cache too
		:return: True if we have it
		"""

	@abstractmethod
	def hasGameType( self, gameType: str ) -> list:
		"""
		Returns True if game type exist else False
		:param gameType:
		:return:
		"""
		pass

	@abstractmethod
	def getGameTypes( self ) -> list:
		"""
		Returns a list of Available categories
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
	def getLiveGameForUser( self, discordID: int, gameType: str = 'any', user: Optional[ PapUser ] = None ) -> List[
		PapGame ]:
		"""
		Returns a list with all live games that this user is playing
		:param gameType: the type of the game, use "any" for any type
		:param discordID: the user to get the games from, put None if use use a PapUser in the user param
		:param user: ALTERNATIVE: a PapUser
		:return: list of games
		"""
		pass

	@abstractmethod
	def getLiveGameForUserForGametype(self, discordID: int, gameType: str, user: Optional[PapUser] = None) -> PapGame:
		"""
		Returns a list with all live games that this user is playing
		:param gameType: the type of the game, use "any" for any type
		:param discordID: the user to get the games from, put None if use use a PapUser in the user param
		:param user: ALTERNATIVE: a PapUser
		:return: list of games
		"""
		gameData = self.db.makeUniqueRequest(
			# EXPLANATION: select the game that is live, from this guild, is of the type gameType,
			# and include userID in userIDs
			'SELECT * FROM games WHERE live = 1 AND guildID = ? AND gameType = ? AND userIDs LIKE ?',
			self.guildID,
			gameType,
			f'%{discordID}%',
			table='games'
		)
		# 	if gameType != 'any' else self.db.makeRequest(
		# 	# EXPLANATION: select all games that are live, from this guild and include userID in userIDs
		# 	'SELECT * FROM games WHERE live = 1 AND guildID = ? AND userIDs LIKE ?',
		# 	self.guildID,
		# 	f'%{discordID}%',
		# 	table='games'
		# )

		returnGame = PapGame(**gameData)
		return returnGame

	@abstractmethod
	def getLiveGamesForGuild( self ) -> List[ PapGame ]:
		"""
		Returns the list of current games in the guild.
		:return List of games
		"""

	@abstractmethod
	def getStatsForUserInGuild(self, userID: int, gameType: str = 'any') -> PapStats:
		"""
		Returns a user in the guild with his stats, None if not found
		:param userID:
		:param gameType:
		:return: user
		"""

	@abstractmethod
	def getRankForUserInGame(self, wins: int, losses: int, ties: int, gameType: str) -> str:
		"""
		Returns the string for the rank in a specified guild
		:param ties:
		:param losses:
		:param wins:
		:param gameType:
		:return:
		"""

	@abstractmethod
	def makeGameRequest(self, discordID: int, discordID2: int,  channelID: int, gametype: str):
		"""
		Make an accept action
		:param discordID:
		:param discordID2:
		:param channelID:
		:param gametype:
		:return:
		"""

	@abstractmethod
	def delGameRequest(self, userID: int, accepted: bool):
		"""
		Deletes accept
		:param accepted:
		:param userID:
		:return:
		"""

	@abstractmethod
	def getGameRequest(self, userID: int):
		"""
		returns an accept request
		:param userID:
		:return:
		"""

	@abstractmethod
	def initStatsForUserInGuild(self, userID: str, gameType: str):
		"""
		Enters the record for that user and gametype to allow the function 'saveStatsForUserInGuild'
		:param gameType:
		:param userID:
		:return:
		"""

	@abstractmethod
	def saveStatsForUserInGuild( self, userID: str, gameType: str, win: bool = False, loss: bool = False, tie: bool = False ):
		"""
		Updates +1 if win, tie or loss is True.
		:param gameType:
		:param userID:
		:param win:
		:param loss:
		:param tie:
		:return:
		"""