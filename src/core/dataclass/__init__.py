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

	def __init__( self, gameID: str, userIDs: List[int], gameData: Dict[str, Any] ):
		self.gameID = gameID
		self.userIDs = userIDs
		self.gameData = gameData
