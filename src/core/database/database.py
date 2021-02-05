from typing import Dict, List, Any

from core.abc.database.database import AbstractDatabase
from core.database.backends import SqlBackend
from core.database.guild import Guild


# TODO: finish this
class Database(AbstractDatabase):

	_cache: Dict[int, Guild] = {}
	instance: 'Database'

	def __init__(self):
		self.backend = SqlBackend('./resources/database.db')
		Database.instance = self

	def getGuild( self, guild: int ) -> Guild:
		if guild not in self._cache.keys():
			self._cache[guild] = Guild(guild, self)
		return self._cache.get(guild)

	def makeRequest( self, sql: str, *args: List[Any] ):
		self.backend.makeRequest(sql, *args)

