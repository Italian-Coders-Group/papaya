from abc import abstractmethod, ABCMeta
from typing import Any, List


class AbstractBackend( metaclass=ABCMeta ):
	path: str

	def __init__(self, path: str):
		self.path = path

	@abstractmethod
	def save( self ) -> None:
		pass

	@abstractmethod
	def makeRequest( self, sqlCode: str, *args: List[Any] ) -> Any:
		pass
