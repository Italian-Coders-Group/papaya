from typing import Dict, List, Optional, Any

from core.abc.database.database import AbstractDatabase
from core.abc.database.guild import AbstractGuild
from core.dataclass import PapStats
from core.dataclass.PapGame import PapGame
from core.dataclass.PapUser import PapUser


class Guild(AbstractGuild):
	_gameCache: Dict[str, PapGame]
	_userCache: Dict[int, PapUser]

	def __init__(self, guildID: int, db: AbstractDatabase):
		super(Guild, self).__init__(guildID, db)
		self._gameCache = {}
		self._userCache = {}

	def getGame(self, gameID: str) -> PapGame:
		"""
		Returns a PapGame object with the requested ID
		:param gameID: the ID to search for
		:return: the PapGame object
		"""
		if gameID not in self._gameCache.keys():
			# EXPLANATION: select a game with gameID gameID and guildID of this guild
			gameData: Dict[str, Any] = self.db.makeRequest(
				'SELECT * FROM games WHERE guildID = ? AND gameID = ?',
				self.guildID,
				gameID,
				table='games'
			)
			self._gameCache[gameID] = PapGame(**gameData)
		return self._gameCache.get(gameID)

	def setGame(self, game: PapGame) -> None:
		"""
		Update the database by adding this game or by updating the saved game with this one
		:param game: a PapGame object with new values
		"""
		self._gameCache[game.gameID] = game
		if self.hasGame(game.gameID, checkCache=False):
			self.db.makeRequest(
				# EXPLANATION: delete a game
				'UPDATE games SET userIDs = ?, gameData = ?, live = ? WHERE guildID = ? AND gameID = ? AND gameType = ?',
				# data
				PapGame.serializeUsers(game.userIDs),
				PapGame.serializeGameData(game.gameData),
				game.live,
				# identification
				self.guildID,
				game.gameID,
				game.gameType
			)
		else:
			self.db.makeRequest(
				# EXPLANATION: insert a game with all their values
				'INSERT INTO games (guildID, gameID, gameType, userIDs, gameData, live) VALUES (?, ?, ?, ?, ?, ?)',
				# identification
				self.guildID,
				game.gameID,
				game.gameType,
				# data
				PapGame.serializeUsers(game.userIDs),
				PapGame.serializeGameData(game.gameData),
				game.live
			)
		self.db.save()

	def getUser(self, userID: int) -> PapUser:
		"""
		Gets a PapUser from the user id
		:param userID: the discord id of the user
		:return: the corresponding PapUser user
		"""
		if userID not in self._userCache.keys():
			# EXPLANATION: select an user with userID userID and guildID of this guild
			userData = self.db.makeUniqueRequest(
				'SELECT * FROM users WHERE guildID = ? AND discordID = ?',
				self.guildID,
				userID,
				table='users')
			userData.pop('guildID')
			self._userCache[userID] = PapUser(**userData)
		return self._userCache.get(userID)

	def setUser(self, user: PapUser) -> None:
		"""
		Update the database by adding this user or by updating the saved user with this one
		:param user: a PapUser object with new values
		"""
		self._userCache[user.discordID] = user
		if self.hasUser(user.discordID, checkCache=False):
			self.db.makeRequest(
				# EXPLANATION: update an existing user
				'UPDATE users SET personalPrefix = ?, permissions = ? WHERE guildID = ? AND discordID = ?',
				# data
				user.personalPrefix,
				PapUser.serializePermissions(user.permissions),
				# identification
				self.guildID,
				user.discordID
			)
		else:
			self.db.makeRequest(
				# EXPLANATION: insert a game with all their values
				'INSERT INTO users (guildID, discordID, personalPrefix, permissions) VALUES (?, ?, ?, ?)',
				# identification
				self.guildID,
				user.discordID,
				# data
				user.personalPrefix,
				PapUser.serializePermissions(user.permissions)
			)
		self.db.save()

	def hasGame(self, gameID: str, checkCache: bool = True, gameType: Optional[str] = 'any') -> bool:
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
		return len(games) > 0

	def hasUser(self, discordID: int, checkCache: bool = True) -> bool:
		"""
		Checks if has an user with that ID
		:param discordID: the user ID to search for
		:param checkCache: True if should check the cache too
		:return: True if we have it
		"""
		if checkCache:
			if discordID in self._userCache.keys():
				return True
		users: list = self.db.makeRequest(
			# EXPLANATION: select all games that are from this guild, are of type gameType and
			# their id is gameID
			'SELECT * FROM users WHERE guildID = ? AND discordID = ?',
			self.guildID,
			discordID
		)
		return len(users) > 0

	def hasGameType(self, gameType: str) -> bool:
		"""
		Returns True if game type exist else False
		:param gameType:
		:return:
		"""
		if gameType == 'any':
			hasGameType = True
		else:
			selection = self.db.makeRequest(
				'SELECT gametype FROM gametypes WHERE gametype = ?',
				gameType
			)
			if len(selection) == 0:
				hasGameType = False
			else:
				hasGameType = True
		return hasGameType

	def getGameTypes(self) -> list:
		"""
		Returns a list of Available categories
		:return:
		"""
		lastGameTypes = []
		crudeGameTypes = self.db.makeRequest(
			'SELECT gametype from gametypes'
		)
		for gametype in crudeGameTypes:
			lastGameTypes.append(gametype[0])

		return lastGameTypes

	def getGamesForUser(self, discordID: int, gameType: str = 'any', user: Optional[PapUser] = None) -> List[PapGame]:
		"""
		Returns a list with all games that this user has played
		:param gameType: the type of the game, use "any" for any type
		:param discordID: the user to get the games from, put None if use use a PapUser in the user param
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
			f'%{discordID}%',
			table='games'
		) if gameType != 'any' else self.db.makeRequest(
			# EXPLANATION: select all games that are from this guild and include userID in userIDs
			'SELECT * FROM games WHERE guildID = ? AND userIDs LIKE ?',
			self.guildID,
			f'%{discordID}%',
			table='games'
		)
		for game in dbGames:
			if str(discordID) in game['userIDs']:
				game.pop('guildID')
				games.append(
					PapGame(**game)
				)
		return games

	def getLiveGameForUser(self, discordID: int, gameType: str = 'any', user: Optional[PapUser] = None) -> List[
		PapGame]:
		pass

	def getLiveGameForUserForGametype(self, discordID: int, gameType: str = 'any', user: Optional[PapUser] = None) -> PapGame:
		"""
		Returns a list with all live games that this user is playing
		:param gameType: the type of the game, use "any" for any type
		:param discordID: the user to get the games from, put None if use use a PapUser in the user param
		:param user: ALTERNATIVE: a PapUser
		:return: list of games
		"""
		gameData: dict = self.db.makeUniqueRequest(
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
		gameData.pop('guildID')
		returnGame = PapGame(**gameData)
		return returnGame

	def getLiveGamesForGuild(self) -> List[PapGame]:
		"""
		Returns the list of current games in the guild.
		:return List of games
		"""

		return_list = []

		game_list = self.db.makeRequest(
			'SELECT * FROM games WHERE guildID = ? AND live = 1',
			self.guildID
		)

		if len(game_list) == 0:
			raise GameNotFound

		for game in game_list:
			return_list.append(
				PapGame(
					**game
				)
			)

		return return_list

	def getStatsForUserForGameTypeInGuild(self, discordID: int, gameType: str) -> PapStats:
		"""
		Returns a user in the guild with his stats, None if not found
		:param discordID:
		:param gameType:
		:return: user
		"""
		validType = 'any' if not self.hasGameType(gameType) else gameType

		user = self.db.makeRequest(
			'SELECT guildID, discordID,'
			'(SELECT SUM(wins) FROM stats WHERE discordID = ? AND guildID = ?) AS totalWins,'
			'(SELECT SUM(losses) FROM stats WHERE discordID = ? AND guildID = ?) AS totalLoses,'
			'(SELECT SUM(ties) FROM stats WHERE discordID = ? AND guildID = ?) AS totalTies'
			' FROM stats WHERE discordID = ? AND guildID = ?',
			discordID,
			self.guildID,
			discordID,
			self.guildID,
			discordID,
			self.guildID,
			discordID,
			self.guildID,
			table='stats'
		) if gameType == "any" else self.db.makeRequest(
			'SELECT * FROM stats WHERE discordID = ? AND guildID = ? AND gameType = ?',
			discordID,
			self.guildID,
			validType,
			table='stats'
		)

		if len(user) == 0:
			return None

		if validType == 'any':
			return PapStats(**user, rank=None, gameType='any')
		else:
			return PapStats(
				**user,
				rank=self.getRankForUserInGame(
					wins=user['wins'],
					losses=user['losses'],
					ties=user['ties'],
					gameType=user['gameType']
				)
			)

	def getStatsForUserInGuild(self, userID: int, gameType: str = 'any') -> PapStats:
		"""
		Returns a user in the guild with his stats, None if not found
		:param userID:
		:param gameType:
		:return: user
		"""
		pass

	def getRankForUserInGame(self, wins: int, losses: int, ties: int, gameType: str) -> str:
		"""
		Returns the string for the rank in a specified guild
		:param ties:
		:param losses:
		:param wins:
		:param gameType:
		:return:
		"""
		rank = self.db.makeRequest(
			"SELECT rank from ranks WHERE ? BETWEEN minPoints AND maxPoints",
			_calculateRankForStats(wins, losses, ties) if gameType != "any" else 0
		)

		return rank[0][0] if not None else "no rank"

	def makeGameRequest(self, discordID: int, discordID2: int, channelID: int, gametype: str):
		"""
		Make an accept action
		:param channelID:
		:param discordID:
		:param discordID2:
		:param gametype:
		:return:
		"""

		check = self._checkGameRequest(discordID)
		if not check:
			self.db.makeRequest(
				'INSERT INTO gameRequests(discordID, discord2ID, guildID, channelID, gameType) VALUES (?, ?, ?, ?, ?)',
				discordID,
				discordID2,
				self.guildID,
				channelID,
				gametype
			)
			self.db.save()
			return True
		return False

	def _checkGameRequest(self, userID: int):
		"""
		Returns True if accept exist, else False
		:param userID:
		:return:
		"""

		check = self.db.makeRequest(
			'SELECT * FROM gameRequests WHERE (discordID = ? OR discord2ID = ?)  AND guildID = ?',
			userID,
			userID,
			self.guildID
		)
		if len(check) > 0:
			returnCheck = True
		else:
			returnCheck = False

		return returnCheck

	def delGameRequest(self, discordID: int):
		"""
		Deletes accept
		"""
		check = self._checkGameRequest(discordID)
		if check:
			self.db.makeRequest(
				"DELETE FROM gameRequests WHERE (discordID = ? OR discord2ID = ?) AND guildID = ?",
				discordID,
				discordID,
				self.guildID
			)
			self.db.save()
			return True
		return False

	def getGameRequest(self, userID: int) -> Dict[str, Any]:
		"""
		returns an accept request
		:param userID:
		:return:
		"""
		requests = self.db.makeRequest(
			'SELECT * FROM gameRequests WHERE discordID = ? AND guildID = ?',
			userID,
			self.guildID,
			table='gameRequests'
		)
		if len(requests) > 0:
			return requests[0]
		else:
			return {'userID': None, 'user2ID': None, 'guildID': None, 'channelID': None}

	def _checkForUserInStats(self, userID: str):
		"""
		This checks if the user has been inserted into the stats table.
		:param userID:
		:return:
		"""

		data = self.db.makeUniqueRequest('SELECT discordID FROM stats WHERE discordID = ?',
		                                 userID)

		if len(data) > 0:
			return True

		return False

	def initStatsForUserInGuild(self, userID: str, gameType: str):
		"""
		Enters the record for that user and gametype to allow the function 'saveStatsForUserInGuild'
		:param gameType:
		:param userID:
		:return:
		"""
		if not self._checkForUserInStats(userID):
			self.db.makeRequest('INSERT INTO stats(guildID, discordID, gameType) VALUES (?, ?, ?)',
			                    self.guildID,
			                    userID,
			                    gameType)

			self.db.save()

	def saveStatsForUserInGuild(self, userID: str, gameType: str, loss: bool = False, win: bool = False, tie: bool = False):
		"""
		Updates +1 if win, tie or loss is True.
		:param gameType:
		:param userID:
		:param loss:
		:param win:
		:param tie:
		:return:
		"""

		winPoint = 1 if win else 0
		lossPoint = 1 if loss else 0
		tiePoint = 1 if tie else 0

		self.db.makeRequest(
			'UPDATE stats SET wins = wins + ?, losses = losses + ?, ties = ties + ? WHERE guildID = ? AND discordID = ? AND gameType = ?',
			winPoint, lossPoint, tiePoint,
			self.guildID,
			userID,
			gameType
		)
		self.db.save()


def _calculateRankForStats(wins: int, losses: int, ties: int) -> int:
	"""	Calculates the rank for single gameType. Returns 0 if gameType is any """
	return (wins * 1) + (losses * -1) + (ties * 0)
