from dataclasses import dataclass

import json
from typing import List, Dict, Any


@dataclass
class PapGame:
	gameID: str
	userIDs: List[ int ]
	gameData: Dict[ str, Any ]
	gameType: str
	live: bool

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
	def deserializeUsers( users: str ):
		return [ int( user ) for user in users.split( ',' ) ]
