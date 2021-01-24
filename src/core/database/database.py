from core.abc.database.database import AbstractDatabase, Game, Guild
from core.database.backends import JsonBackend


# TODO: finish this
class Database(AbstractDatabase):

	def __init__(self):
		self.backend = JsonBackend('./resources/database.json')
		self.backend.load()

	def getGuild( self, guild: int ) -> Guild:
		return Guild( self.backend.getGuild(guild) )

	def updateGameToGuild( self, game: Game ) -> None:
		pass


