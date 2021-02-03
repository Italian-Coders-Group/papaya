from core.abc.database.guild import AbstractGuild
from core.dataclass import PapGame, PapUser


class Guild(AbstractGuild):

	def __init__(self, guildId: int):
		super(Guild, self).__init__(guildId)

	def getGame( self, gameId: str ) -> PapGame:
		pass

	def setGame( self, gameId: str, game: PapGame ):
		pass

	def getMember( self, userId: int ) -> PapUser:
		pass