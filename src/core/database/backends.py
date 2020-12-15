import json
from typing import Any, Dict, Union, List

from core.abc.database.backends import AbstractBackend


GuildId = str
Games = List[Dict]
Members = List[Dict]


class JsonBackend( AbstractBackend ):

	data: Dict[ GuildId, Dict[ str, Union[ Games, Members ] ] ]

	def __init__(self, path: str = None):
		self.data = {}
		if path is not None:
			self.path = path

	def save( self, path: str = None ) -> None:
		if path is None:
			path = self.path
		with open( path, 'w' ) as file:
			json.dump( self.data, file, indent=4 )

	def load( self, path: str = None ) -> None:
		if path is None:
			path = self.path
		with open(path, 'r') as file:
			self.data = json.load( file )

	def getGuild( self, uuid: int ) -> dict:
		return self.data[ str( uuid ) ]


# TODO: implement sql backend
class SqlBackend(AbstractBackend):

	def __init__(self):
		raise NotImplementedError

	def save( self, path: str = None ) -> None:
		raise NotImplementedError

	def load( self, path: str = None ) -> None:
		raise NotImplementedError

	def getGuild( self, uuid: int ) -> dict:
		raise NotImplementedError
