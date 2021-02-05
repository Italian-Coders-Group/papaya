from typing import Dict, Tuple, List
import json

from core.abc.database.database import AbstractDatabase
from core.abc.database.guild import AbstractGuild
from core.dataclass import PapGame, PapUser


class Guild(AbstractGuild):

	_gameCache: Dict[str, PapGame]
	_gameCache: Dict[int, PapUser]

	def __init__(self, guildId: int, db: AbstractDatabase):
		super(Guild, self).__init__(guildId, db)

	def getGame( self, gameId: str ) -> PapGame:
		if gameId not in self._gameCache.keys():
			gamedata: List[ Tuple ] = self.db.makeRequest('SELECT * FROM games WHERE gameId = ?', gameId)
			self._gameCache[gameId] = PapGame(
				userIds=[ int(num) for num in gamedata[0][0].split(',')  ],
				gameData=json.loads( gamedata[0][1] )
			)
		return self._gameCache.get( gameId )

	def setGame( self, gameId: str, game: PapGame ):
		self._gameCache[ gameId ] = game
		if self.hasGame(gameId):
			self.db.makeRequest('DELETE FROM games WHERE gameId = ?', gameId)
		self.db.makeRequest(
			'INSERT INTO games (gameId, userIds, gameData) VALUES (?, ?, ?)',
			gameId,
			str( game.userIds )[1:][:-1].replace(' ', ''),
			json.dumps( game.gameData, indent=None, separators=(',', ':') )
		)

	def getMember( self, userId: int ) -> PapUser:
		pass

	def hasGame( self, gameId: str ):
		pass

	def hasUser( self, userId: int ):
		pass
