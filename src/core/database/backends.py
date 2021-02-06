import json
import sqlite3 as sql
from pathlib import Path
from typing import Dict, Union, List, Any

from core.logging import get_logger
from core.abc.database.backends import AbstractBackend


GuildId = str
Games = List[Dict]
Members = List[Dict]
logger = get_logger('database')


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


class SqlBackend(AbstractBackend):

	dinstance: sql.Connection
	cursor: sql.Cursor
	dbpath: Path

	def __init__( self, path: str = None ):
		super(SqlBackend, self).__init__( path )
		self.dbpath = Path(path)
		# as the connect() function always creates the database file, we need a way to check if it existed _before_
		# connect is called
		existed = True
		if not self.dbpath.exists():
			existed = False
			logger.warning(f'database not found at "{path}", will create one')
		self.dinstance = sql.connect(path)
		self.cursor = self.dinstance.cursor()
		if not existed:
			self.cursor.execute(
				sql='CREATE TABLE games ( guildID INT NOT NULL, gameID TEXT NOT NULL, userIDs TEXT, gameData TEXT, CONSTRAINT PK_game PRIMARY KEY (guildID, gameID) )'
			)

	def save( self ) -> None:
		self.dinstance.commit()

	def makeRequest( self, sqlCode: str, *args: List[Any] ) -> Any:
		self.cursor.execute( sqlCode, args )
		return self.cursor.fetchall()
