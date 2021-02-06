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
		"""	Commit changes to the database file	"""
		self.dinstance.commit()

	def makeRequest( self, sqlCode: str, *args: List[Any] ) -> Any:
		"""
		Makes a request with SQL code to the database.
		DO NOT USE VARIABLES IN THE SQL CODE!
		IS **VERY** INSECURE AND CAN CAUSE DATA LOSS!
		:param sqlCode: SQL code
		:param args: arguments for value sanitizing
		:return: a List with the result (can be emtpy)
		"""
		self.cursor.execute( sqlCode, args )
		return self.cursor.fetchall()
