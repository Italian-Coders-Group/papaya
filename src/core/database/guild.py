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
			# EXPLANATION: select a game with gameID gameID and guildID guildID
			gameData: Tuple = self.db.makeRequest('SELECT * FROM games WHERE guildID = ? AND gameID = ?', self.guildID, gameID )[0]
			self._gameCache[ gameID ] = PapGame(
				gameID=gameID,
				gameType=gameData[2],
				userIDs=[ int(num) for num in gameData[3].split(',')  ],
				gameData=json.loads( gameData[4] ),
				live=gameData[5]
			)
		return self._gameCache.get( gameID )

	def setGame( self, game: PapGame ) -> None:
		"""
		Update the database by adding this game or by updating the saved game with this one
		:param game: a PapGame object with new values
		"""
		self._gameCache[ game.gameID ] = game
		if self.hasGame( game.gameID, checkCache=False ):
			self.db.makeRequest(
				# EXPLANATION: delete a game
				'DELETE FROM games WHERE guildID = ? AND gameID = ? AND gameType = ?',
				self.guildID,
				game.gameID,
				game.gameType
			)
		self.db.makeRequest(
			# EXPLANATION: insert a game with all thir values
			'INSERT INTO games (guildID, gameID, gameType, userIDs, gameData, live) VALUES (?, ?, ?, ?, ?, ?)',
			self.guildID,
			game.gameID,
			game.gameType,
			str( game.userIDs )[1:][:-1].replace(' ', ''),
			json.dumps( game.gameData, indent=None, separators=(',', ':') ),
			game.live
		)
		self.db.save()

	def getUser( self, userID: int ) -> PapUser:
		"""
		NOT IMPLEMENTED
		:param userID:
		:return:
		"""
		raise NotImplementedError()

	def hasGame( self, gameID: str, checkCache: bool = True, gameType: Optional[ str ] = 'any' ) -> bool:
		"""
		Checks if has a game with that ID
		:param gameID: the game ID to search for
		:param checkCache: True if should check the cache too
		:param gameType: the type of the game to search, optional, can make searching faster
		:return: True if we have it
		"""
		if checkCache:
			if gameID in self._gameCache.keys():
				return True
		games: list = self.db.makeRequest(
			# EXPLANATION: select all games that are from this guild, are of type gameType and
			# their id is gameID
			'SELECT * FROM games WHERE guildID = ? AND gameID = ? AND gameType = ?',
			self.guildID,
			gameID
		) if gameType != 'any' else self.db.makeRequest(
			# EXPLANATION: select all games that are from this guild and their id is gameID
			'SELECT * FROM games WHERE guildID = ? AND gameID = ?',
			self.guildID,
			gameID,
			gameType
		)
		return len( games ) > 0

	def hasUser( self, userID: int ) -> bool:
		"""
		NOT IMPLEMENTED
		:param userID:
		:return:
		"""
		raise NotImplementedError()

	def getGamesForUser( self, userID: int, gameType: str = 'any', user: Optional[PapUser] = None ) -> List[PapGame]:
		"""
		Returns a list with all games that this user has played
		:param gameType: the type of the game, use "any" for any type
		:param userID: the user to get the games from, put None if use use a PapUser in the user param
		:param user: ALTERNATIVE: a PapUser
		:return: list of games
		"""
		games = []
		dbGames: list = self.db.makeRequest(
			# EXPLANATION: select all games that are from this guild, have the type ?,
			# and include userID in userIDs
			'SELECT * FROM games WHERE guildID = ? AND gameType = ? AND userIDs LIKE ?',
			self.guildID,
			gameType,
			f'%{userID}%'
		) if gameType != 'any' else self.db.makeRequest(
			# EXPLANATION: select all games that are from this guild and include userID in userIDs
			'SELECT * FROM games WHERE guildID = ? AND userIDs LIKE ?',
			self.guildID,
			f'%{userID}%'
		)
		for game in dbGames:
			if str(userID) in game[3].split(','):
				games.append(
					PapGame(
						gameID=game[1],
						live=bool( game[5] ),
						gameType=game[2],
						userIDs=[ int( num ) for num in game[ 3 ].split( ',' ) ],
						gameData=json.loads( game[ 4 ] )
					)
				)
		return games

	def getLiveGameForUser( self, userID: int, gameType: str = 'any', user: Optional[ PapUser ] = None ) -> List[ PapGame ]:
		"""
		Returns a list with all live games that this user is playing
		:param gameType: the type of the game, use "any" for any type
		:param userID: the user to get the games from, put None if use use a PapUser in the user param
		:param user: ALTERNATIVE: a PapUser
		:return: list of games
		"""
		games = [ ]
		dbGames: list = self.db.makeRequest(
			# EXPLANATION: select all games that are live, from this guild, are of the type gameType,
			# and include userID in userIDs
			'SELECT * FROM games WHERE live = 1 AND guildID = ? AND gameType = ? AND userIDs LIKE ?',
			self.guildID,
			gameType,
			f'%{userID}%'
		) if gameType != 'any' else self.db.makeRequest(
			# EXPLANATION: select all games that are live, from this guild and include userID in userIDs
			'SELECT * FROM games WHERE live = 1 AND guildID = ? AND userIDs LIKE ?',
			self.guildID,
			f'%{userID}%'
		)
		for game in dbGames:
			if str( userID ) in game[ 3 ].split( ',' ):
				games.append(
					PapGame(
						gameID=game[ 1 ],
						live=bool( game[ 5 ] ),
						userIDs=[ int( num ) for num in game[ 3 ].split( ',' ) ],
						gameData=json.loads( game[ 4 ] ),
						gameType=game[2]
					)
				)
		return games
