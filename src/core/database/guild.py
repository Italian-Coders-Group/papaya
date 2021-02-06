from typing import Dict, Tuple, List, Optional
import json

from core.abc.database.database import AbstractDatabase
from core.abc.database.guild import AbstractGuild
from core.dataclass import PapGame, PapUser


class Guild(AbstractGuild):

	_gameCache: Dict[str, PapGame]
	_gameCache: Dict[int, PapUser]

	def __init__(self, guildID: int, db: AbstractDatabase):
		super(Guild, self).__init__(guildID, db)

	def getGame( self, gameID: str ) -> PapGame:
		if gameID not in self._gameCache.keys():
			gameData: List[ Tuple ] = self.db.makeRequest('SELECT * FROM games WHERE guildID = ? AND gameID = ?', self.guildID, gameID )
			self._gameCache[gameID ] = PapGame(
				userIds=[ int(num) for num in gameData[0][1].split(',')  ],
				gameData=json.loads( gameData[0][2] )
			)
		return self._gameCache.get( gameID )

	def setGame( self, gameID: str, game: PapGame ) -> None:
		self._gameCache[ gameID ] = game
		if self.hasGame( gameID ):
			self.db.makeRequest('DELETE FROM games WHERE guildID = ? AND gameID = ?', self.guildID, gameID )
		self.db.makeRequest(
			'INSERT INTO games (guildID, gameID, userIDs, gameData) VALUES (?, ?, ?, ?)',
			self.guildID,
			gameID,
			str( game.userIds )[1:][:-1].replace(' ', ''),
			json.dumps( game.gameData, indent=None, separators=(',', ':') )
		)
		self.db.save()

	def getUser( self, userID: int ) -> PapUser:
		pass

	def hasGame( self, gameID: str ) -> bool:
		if gameID in self._gameCache.keys():
			return True
		return True in [
			gameID == x[0] for x in self.db.makeRequest(
				'SELECT * FROM games WHERE guildID = ? AND gameID = ?',
				self.guildID,
				gameID
			)
		]

	def hasUser( self, userId: int ) -> bool:
		pass

	def getGamesForUser( self, userID: int, user: Optional[PapUser] = None ) -> List[PapGame]:
		pass
