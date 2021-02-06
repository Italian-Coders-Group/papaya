import json
from typing import Dict, Tuple, List, Optional

from core.abc.database.database import AbstractDatabase
from core.abc.database.guild import AbstractGuild
from core.dataclass import PapGame, PapUser


class Guild(AbstractGuild):

	_gameCache: Dict[str, PapGame]
	_userCache: Dict[int, PapUser]

	def __init__(self, guildID: int, db: AbstractDatabase):
		super(Guild, self).__init__(guildID, db)
		self._gameCache = {}
		self._userCache = {}

	def getGame( self, gameID: str ) -> PapGame:
		"""
		Returns a PapGame object with the requested ID
		:param gameID: the ID to search for
		:return: the PapGame object
		"""
		if gameID not in self._gameCache.keys():
			gameData: List[ Tuple ] = self.db.makeRequest('SELECT * FROM games WHERE guildID = ? AND gameID = ?', self.guildID, gameID )
			self._gameCache[gameID ] = PapGame(
				gameID=gameID,
				userIDs=[ int(num) for num in gameData[0][2].split(',')  ],
				gameData=json.loads( gameData[0][3] )
			)
		return self._gameCache.get( gameID )

	def setGame( self, game: PapGame ) -> None:
		"""
		Update the database by adding this game or by updating the saved game with this one
		:param game: a PapGame object with new values
		"""
		self._gameCache[ game.gameID ] = game
		if self.hasGame( game.gameID, checkCache=False ):
			self.db.makeRequest('DELETE FROM games WHERE guildID = ? AND gameID = ?', self.guildID, game.gameID )
		self.db.makeRequest(
			'INSERT INTO games (guildID, gameID, userIDs, gameData) VALUES (?, ?, ?, ?)',
			self.guildID,
			game.gameID,
			str( game.userIDs )[1:][:-1].replace(' ', ''),
			json.dumps( game.gameData, indent=None, separators=(',', ':') )
		)
		self.db.save()

	def getUser( self, userID: int ) -> PapUser:
		"""
		NOT IMPLEMENTED
		:param userID:
		:return:
		"""
		raise NotImplementedError()

	def hasGame( self, gameID: str, checkCache: bool = True ) -> bool:
		"""
		Checks if has a game with that ID
		:param gameID: the game ID to search for
		:param checkCache: True if should check the cache too
		:return: True if we have it
		"""
		if checkCache:
			if gameID in self._gameCache.keys():
				return True
		return True in [
			gameID == x[0] for x in self.db.makeRequest(
				'SELECT * FROM games WHERE guildID = ? AND gameID = ?',
				self.guildID,
				gameID
			)
		]

	def hasUser( self, userID: int ) -> bool:
		"""
		NOT IMPLEMENTED
		:param userID:
		:return:
		"""
		raise NotImplementedError()

	def getGamesForUser( self, userID: int, user: Optional[PapUser] = None ) -> List[PapGame]:
		"""
		Returns a list with all games that this user has played
		:param userID: the user to get the games from, put None if use use a PapUser in the user param
		:param user: ALTERNATIVE: a PapUser
		:return: list of games
		"""
		games = []
		for game in self.db.makeRequest( 'SELECT * FROM games WHERE guildID = ?', self.guildID ):
			if str(userID) in game[2].split(','):
				games.append(
					PapGame(
						gameID=game[1],
						userIDs=[ int( num ) for num in game[ 2 ].split( ',' ) ],
						gameData=json.loads( game[ 3 ] )
					)
				)
		return games

