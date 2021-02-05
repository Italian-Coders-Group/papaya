import json
import sqlite3 as sql
from typing import Dict, Union, List, Any

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

	def makeRequest( self, sqlCode: str, *args: List[Any] ) -> Any:
		pass


# TODO: implement sql backend
class SqlBackend(AbstractBackend):

	dinstance: sql.Connection
	cursor: sql.Cursor

	def __init__( self, path: str = None ):
		super(SqlBackend, self).__init__( path )

	def save( self ) -> None:
		self.dinstance.commit()

	def makeRequest( self, sqlCode: str, *args: List[Any] ) -> Any:
		self.cursor.execute( sqlCode, args )
		return self.cursor.fetchall()
