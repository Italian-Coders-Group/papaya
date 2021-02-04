from core.abc.database.database import AbstractDatabase
from core.abc.database.guild import AbstractGuild
from core.dataclass import PapGame, PapUser


class Guild(AbstractGuild):

	def __init__(self, guildId: int, db: AbstractDatabase):
		super(Guild, self).__init__(guildId, db)

	def getGame( self, gameId: str ) -> PapGame:
		return

	def setGame( self, gameId: str, game: PapGame ):
		pass

	def getMember( self, userId: int ) -> PapUser:
		pass
