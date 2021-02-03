from typing import List, Any, Dict


class PapUser:

	userId: int
	permissions: List[bool] = ''
	gamesWinned: int
	gamesLost: int

	def __init__( self, userId: int, permissions: List[bool], gamesWinned: int, gamesLost: int ):
		self.userId = userId
		self.permissions = permissions
		self.gamesWinned = gamesWinned
		self.gamesLost = gamesLost


class PapGame:

	userIds: List[int]
	gameData: Dict[str, Any]

	def __init__(self, userIds: List[int], gameData: Dict[str, Any]):
		self.userIds = userIds
		self.gameData = gameData
