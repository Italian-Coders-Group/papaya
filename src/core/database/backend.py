import sqlite3 as sql
from pathlib import Path
from typing import Dict, List, Any

from core.abc.database.backend import AbstractBackend
from core.logging import get_logger

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
		self.dinstance = sql.connect(path)
		self.cursor = self.dinstance.cursor()
		# conditionally creates the tables
		self.cursor.execute(
			'''
			CREATE TABLE IF NOT EXISTS games (
				guildID INT NOT NULL,
				gameID TEXT NOT NULL,
				gameType TEXT NOT NULL,
				userIDs TEXT NOT NULL,
				gameData TEXT NOT NULL,
				live INT[0] NOT NULL,
				CONSTRAINT PK_game PRIMARY KEY (guildID, gameID)
			)
			'''
		)
		self.cursor.execute(
			'''
			CREATE TABLE IF NOT EXISTS stats (
				guildID INT NOT NULL,
				userID TEXT NOT NULL,
				gameType TEXT NOT NULL,
				wins INT NOT NULL DEFAULT 0,
				losses INT NOT NULL DEFAULT 0,
				ties INT NOT NULL DEFAULT 0,
				CONSTRAINT PK_stats PRIMARY KEY (guildID, userID, gameType)
			)
			'''
		)
		self.cursor.execute(
			'''
			CREATE TABLE IF NOT EXISTS ranks (
				rank TEXT NOT NULL,
				minPoints INT NOT NULL,
				maxPoints INT NOT NULL
			)
			'''
		)
		self.cursor.execute(
			'''
			CREATE TABLE IF NOT EXISTS gameTypes (
				gametype text NOT NULL,
				CONSTRAINT PK_gameTypes PRIMARY KEY (gameType)
			)
			'''
		)
		self.cursor.execute(
			'''
			CREATE TABLE IF NOT EXISTS gameRequests (
				userID text NOT NULL,
				user2ID text NOT NULL,
				guildID int NOT NULL,
				channelID int not null,
				CONSTRAINT PK_accept PRIMARY KEY (userID, user2ID, guildID)
			)
			'''
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
