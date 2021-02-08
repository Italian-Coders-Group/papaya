from typing import List, Any, Dict


class PapUser:

	userId: int
	permissions: List[bool]
	gamesWinned: int
	gamesLost: int

	def __init__( self, userId: int, permissions: List[bool], gamesWinned: int, gamesLost: int ):
		self.userId = userId
		self.permissions = permissions
		self.gamesWinned = gamesWinned
		self.gamesLost = gamesLost


class PapGame:

	gameID: str
	userIDs: List[int]
	gameData: Dict[str, Any]
	gameType: str
	live: bool

	def __init__( self, gameID: str, gameType: str, userIDs: List[int], gameData: Dict[str, Any], live: bool ):
		self.gameID = gameID
		self.gameType = gameType
		self.userIDs = userIDs
		self.gameData = gameData
		self.live = live
