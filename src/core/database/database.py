from typing import Dict

from core.abc.database.database import AbstractDatabase
from core.database.backends import SqlBackend
from core.database.guild import Guild


# TODO: finish this
class Database(AbstractDatabase):

	_cache: Dict[int, Guild] = {}

	def __init__(self):
		self.backend = SqlBackend('./resources/database.json')
		self.backend.load()

	def getGuild( self, guild: int ) -> Guild:
		return Guild( guild, self )

	def makeRequest( self, sql: str ):
		self.backend

