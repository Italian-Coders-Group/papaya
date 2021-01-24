import json
from typing import Dict, Union, List

from core.abc.database.backends import AbstractBackend


GuildId = str
Games = List[Dict]
Members = List[Dict]


class JsonBackend( AbstractBackend ):

	data: Dict[ GuildId, Dict[ str, Union[ Games, Members ] ] ]

	def __init__(self, path: str = None):
		super(JsonBackend, self).__init__(path)
		self.data = {}

	def save( self ) -> None:
		with open( self.path, 'w' ) as file:
			json.dump( self.data, file, indent=4 )

	def load( self ) -> None:
		with open(self.path, 'r') as file:
			self.data = json.load( file )

	def getGuild( self, uuid: int ) -> dict:
		return self.data[ str( uuid ) ]


# TODO: implement sql backend
class SqlBackend(AbstractBackend):

	def __init__( self, path: str = None ):
		super(SqlBackend, self).__init__( path )
		raise NotImplementedError

	def save( self ) -> None:
		raise NotImplementedError

	def load( self, path: str = None ) -> None:
		raise NotImplementedError

	def getGuild( self, uuid: int ) -> dict:
		raise NotImplementedError
