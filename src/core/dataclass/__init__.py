from typing import List, Any, Dict


class PapUser:

	userID: int
	personalPrefix: str
	permissions: List[bool]

	def __init__( self, userID: int, personalPrefix: str, permissions: str ):
		self.userID = userID
		self.personalPrefix = personalPrefix
		self.permissions = [ bool( int( value ) ) for value in permissions ]


class PapStats:

	userId: int
	gameType: str
	gamesWon: int
	gamesLost: int
	gamesTied: int
	rank: str

	def __init__(self, userId: int, gameType: str, wins: int, losses: int, ties: int, rank: str):
		self.userId = userId
		self.gameType = gameType
		self.gamesWon = wins
		self.gamesLost = losses
		self.gamesTied = ties
		self.rank = rank


class PapGame:

	gameID: str
	userIDs: List[int]
	gameData: Dict[str, Any]
	gameType: str
	live: bool

	def __init__( self, gameID: str, gameType: str, userIDs: str, gameData: Dict[str, Any], live: bool ):
		self.gameID = gameID
		self.gameType = gameType
		self.userIDs = [ int(user) for user in userIDs.split(',') ]
		self.gameData = gameData
		self.live = live
