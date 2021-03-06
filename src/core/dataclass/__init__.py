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



