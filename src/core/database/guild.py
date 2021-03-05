import json
from typing import Dict, Tuple, List, Optional

from core.abc.database.database import AbstractDatabase
from core.abc.database.guild import AbstractGuild
from core.dataclass import PapGame, PapUser, PapStats


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
			gameID,
			gameType
		) if gameType != 'any' else self.db.makeRequest(
			# EXPLANATION: select all games that are from this guild and their id is gameID
			'SELECT * FROM games WHERE guildID = ? AND gameID = ?',
			self.guildID,
			gameID
		)
		return len( games ) > 0

	def hasUser( self, userID: int ) -> bool:
		"""
		NOT IMPLEMENTED
		:param userID:
		:return:
		"""
		raise NotImplementedError()

	def hasGametype(self, gameType: str) -> list:
		"""
		Returns True if game type exist else False
		:param gameType:
		:return:
		"""
		if gameType == "any":
			hasGametype = [True, 1]
		else:
			selection = self.db.makeRequest(
				"SELECT gametype FROM gametypes WHERE gametype = ?",
				gameType
			)
			if len(selection) == 0:
				hasGametype = [False, 0]
			else:
				hasGametype = [True, 0]
		return hasGametype

	def getGametypes(self) -> list:
		"""
		Returns a list of Available categories
		:return:
		"""
		lastGameTypes = []
		crudeGameTypes = self.db.makeRequest(
			"SELECT gametype from gametypes"
		)
		for gametype in crudeGameTypes:
			lastGameTypes.append(gametype[0])

		return lastGameTypes

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

	def getLiveGameForUser( self, userID: int, gameType: str = 'any', user: Optional[ PapUser ] = None ) -> List[
		PapGame ]:
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

	def getStatsForUserInGuild(self, userID: int, gameType: str = "any") -> PapStats:
		"""
		Returns a user in the guild with his stats, None if not found
		:param userID:
		:param gameType:
		:return: user
		"""
		validGametype = self.hasGametype(gameType)
		print(validGametype)
		if not validGametype[0]:
			validType = "any"
		else:
			validType = gameType
		print(validType)
		print(gameType)
		user = self.db.makeRequest(
			'SELECT guildID, userID,'
			'(SELECT SUM(wins) FROM stats WHERE userID = ? AND guildID = ?) AS totalWins,'
			'(SELECT SUM(losses) FROM stats WHERE userID = ? AND guildID = ?) AS totalLoses,'
			'(SELECT SUM(ties) FROM stats WHERE userID = ? AND guildID = ?) AS totalTies'
			' FROM stats WHERE userID = ? AND guildID = ?',
			userID,
			self.guildID,
			userID,
			self.guildID,
			userID,
			self.guildID,
			userID,
			self.guildID
		) if gameType == "any" else self.db.makeRequest(
			'SELECT * FROM stats WHERE userID = ? AND guildID = ? AND gameType = ?',
			userID,
			self.guildID,
			validType
		)

		if len(user) > 0:
			middleUser = user[0]
			if validType == "any":
				returnUser = PapStats(
					userId=middleUser[1],
					gameType=validType,
					gamesWon=middleUser[2],
					gamesLost=middleUser[3],
					gamesTied=middleUser[4],
					rank=None
				)
			else:
				returnUser = PapStats(
					userId=middleUser[1],
					gameType=middleUser[2],
					gamesWon=middleUser[3],
					gamesLost=middleUser[4],
					gamesTied=middleUser[5],
					rank=self.getRankForUserInGame([middleUser[3], middleUser[4], middleUser[5]], middleUser[2])
				)

		return returnUser

	def getRankForUserInGame(self, userStats: list, gameType: str) -> str:
		"""
        Returns the string for the rank in a specified guild, returns 0 if gameType is any
        :param userStats:
        :param gameType:
        :return:
        """
		rank = self.db.makeRequest(
			"SELECT rank from ranks WHERE ? BETWEEN minPoints AND maxPoints",
			self.calculateRankForUserStats(userStats) if gameType != "any" else 0
		)

		return rank[0][0] if not None else "no rank"

	def calculateRankForUserStats(self, userStats: list) -> int:
		"""
		Calculates the rank for single gameType. Returns 0 if gametype is any
		:param userStats:
		:return:
		"""

		wins, losses, ties = userStats

		final = (wins * 1) + (losses * -1) + (ties * 0)

		return final

	def makeAccept(self, userID: int, user2ID: int,  channelID):
		"""
        Make an accept action
        :param channelID:
        :param user2ID:
        :param userID:
        :return:
        """
		check = self.checkAccept(userID)
		if not check:
			accept = self.db.makeRequest(
				'INSERT INTO accept(userID, guildID, channelID) VALUES (?, ?, ?)',
				userID,
				self.guildID,
				user2ID
			)
		else:
			return False
		self.db.save()
		return True

	def checkAccept(self, userID: int):
		"""
		Returns True if accept exist, else False
		:param userID:
		:return:
		"""
		check = self.db.makeRequest(
			'SELECT * FROM accept WHERE (userID = ? OR user2ID = ?)  AND guildID = ?',
			userID,
			userID,
			self.guildID
		)
		if len(check) > 0:
			returnCheck = True
		else:
			returnCheck = False

		return returnCheck

	def delAccept(self, userID: int):
		"""
		Deletes accept
		:param userID:
		:return:
		"""
		check = self.checkAccept(userID)
		if check:
			delete = self.db.makeRequest(
				"DELETE FROM accept WHERE (userID = ? OR user2ID = ?) AND guildID = ?",
				userID,
				userID,
				self.guildID
			)
		else:
			return False
		return True

	def getAccept(self, userID: int):
		"""
		returns an accept request
		:param userID:
		:return:
		"""
		requests = self.db.makeRequest(
			'SELECT * FROM accept WHERE userID = ? AND guildID = ?',
			userID,
			self.guildID
		)
		if len(requests) > 0:
			returnRequest = requests[0]
		else:
			returnRequest = False

		return returnRequest

	def saveStatsForUserInGuild(self, userID: str, gameType: str, win: bool = False, loss: bool = False, tie: bool = False):
		"""
		Updates +1 if win, tie or loss is True.
		:param gameType:
		:param userID:
		:param win:
		:param loss:
		:param tie:
		:return:
		"""

		if win:
			self.db.makeRequest(
				"UPDATE stats SET wins = wins + 1 WHERE guildID = ? AND userID = ? AND gameType = ?",
				self.guildID,
				userID,
				gameType
			)
		elif loss:
			self.db.makeRequest(
				"UPDATE stats SET losses = losses + 1 WHERE guildID = ? AND userID = ? AND gameType = ?",
				self.guildID,
				userID,
				gameType
			)
		elif tie:
			self.db.makeRequest(
				"UPDATE stats SET ties = ties + 1 WHERE guildID = ? AND userID = ? AND gameType = ?",
				self.guildID,
				userID,
				gameType
			)

		return