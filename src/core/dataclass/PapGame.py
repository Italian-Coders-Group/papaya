import json
from typing import List, Dict, Any


class PapGame:
	gameID: str
	userIDs: List[ int ]
	gameData: Dict[ str, Any ]
	gameType: str
	live: bool

	def __init__( self, gameID: str, gameType: str, userIDs: str, gameData: str, live: bool ):
		self.gameID = gameID
		self.gameType = gameType
		self.userIDs = PapGame.deserializeUsers(userIDs)
		self.gameData = PapGame.deserializeGameData( gameData )
		self.live = live

	@staticmethod
	def serializeGameData( data: dict ) -> str:
		return json.dumps( data, indent=None, separators=(',', ':') )

	@staticmethod
	def deserializeGameData( data: str ) -> Dict[ str, Any ]:
		return json.loads(data)

	@staticmethod
	def serializeUsers( userIDs: List[int] ):
		return str( userIDs )[ 1: ][ :-1 ].replace( ' ', '' )

	@staticmethod
	def deserializeUsers( users: list ):
		return [ int( user ) for user in users.split( ',' ) ]
		# return ''.join(f', {user}' for user in users)