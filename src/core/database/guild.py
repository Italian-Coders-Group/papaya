from typing import Dict, Tuple, List
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
			gamedata: List[ Tuple ] = self.db.makeRequest('SELECT * FROM games WHERE gameID = ?', gameID )
			self._gameCache[gameID ] = PapGame(
				userIds=[ int(num) for num in gamedata[0][0].split(',')  ],
				gameData=json.loads( gamedata[0][1] )
			)
		return self._gameCache.get( gameID )

	def setGame( self, gameID: str, game: PapGame ):
		self._gameCache[ gameID ] = game
		if self.hasGame( gameID ):
			self.db.makeRequest('DELETE FROM games WHERE gameID = ?', gameID )
		self.db.makeRequest(
			'INSERT INTO games (gameID, userIDs, gameData) VALUES (?, ?, ?)',
			gameID,
			str( game.userIds )[1:][:-1].replace(' ', ''),
			json.dumps( game.gameData, indent=None, separators=(',', ':') )
		)

	def getMember( self, userID: int ) -> PapUser:
		pass

	def hasGame( self, gameID: str ):
		pass

	def hasUser( self, userId: int ):
		pass
