from abc import abstractmethod, ABCMeta
from typing import Any


class AbstractBackend( metaclass=ABCMeta ):
	path: str

	@abstractmethod
	def save( self, path: str = None ) -> None:
		pass

	@abstractmethod
	def load( self, path: str = None ) -> None:
		pass

	@abstractmethod
	def getGuild( self, uuid: int ) -> dict:
		pass
