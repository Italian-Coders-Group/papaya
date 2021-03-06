from typing import List, Any, Dict


class PapUser:

	userId: int
	permissions: List[bool]

	def __init__( self, userId: int, permissions: List[bool]):
		self.userId = userId
		self.permissions = permissions


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
