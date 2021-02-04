from abc import abstractmethod, ABCMeta
from typing import Any


class AbstractBackend( metaclass=ABCMeta ):
	path: str

	def __init__(self, path: str):
		self.path = path

	@abstractmethod
	def save( self ) -> None:
		pass

	@abstractmethod
	def makeRequest( self, sqlCode: str ) -> Any:
		pass
