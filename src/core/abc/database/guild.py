from abc import ABCMeta, abstractmethod
from typing import Any, Dict

from core.dataclass import PapGame, PapUser


class AbstractGuild:

	guild: int

	def __init__(self, guildId: int):
		self.guild = guildId

	@abstractmethod
	def getGame( self, gameId: str ) -> PapGame:
		pass

	@abstractmethod
	def setGame( self, gameId: str, game: PapGame ):
		pass

	@abstractmethod
	def getMember( self, userId: int ) -> PapUser:
		pass
