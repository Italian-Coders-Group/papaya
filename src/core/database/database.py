from typing import Dict, Any

from core.abc.database.database import AbstractDatabase
from core.database.backends import SqlBackend
from core.database.guild import Guild


class Database(AbstractDatabase):

	_cache: Dict[int, Guild] = {}
	instance: 'Database'

	def __init__( self ):
		self.backend = SqlBackend('./resources/database.db')
		Database.instance = self

	def getGuild( self, guild: int ) -> Guild:
		"""
		Returns a Guild object for interacting with the database
		:param guild: guid ID
		:return: the Guild Object
		"""
		if guild not in self._cache.keys():
			self._cache[guild] = Guild(guild, self)
		return self._cache.get(guild)

	def makeRequest( self, sql: str, *args ) -> Any:
		"""
		Makes a request with SQL code to the database.
		DO NOT USE VARIABLES IN THE SQL CODE!
		IS **VERY** INSECURE AND CAN CAUSE DATA LOSS!
		:param sql: SQL code
		:param args: arguments for value sanitizing
		:return: a List with the result (can be emtpy)
		"""
		return self.backend.makeRequest(sql, *args)

	def save( self ) -> None:
		"""	Commit changes to the database file	"""
		self.backend.save()

	def __del__( self ):
		# save when closing!
		self.save()
