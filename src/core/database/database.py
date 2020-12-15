# TODO: finish this
from core.abc.database.database import AbstractDatabase, Game, Guild
from core.database.backends import JsonBackend


class Database(AbstractDatabase):

	def __init__(self):
		self.backend = JsonBackend('./assets/test.json')
		self.backend.load()

	def getGuild( self, guild: int ) -> Guild:
		return Guild( self.backend.getGuild(guild) )

	def updateGame( self, game: Game ) -> None:
		pass

	def __del__(self):
		self.backend.save()
