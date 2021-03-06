from abc import abstractmethod, ABCMeta
from typing import Any, List


class AbstractBackend( metaclass=ABCMeta ):
	path: str

	def __init__(self, path: str):
		self.path = path

	@abstractmethod
	def save( self ) -> None:
		"""	Commit changes to the database file	"""
		pass

	@abstractmethod
	def makeRequest( self, sqlCode: str, *args: List[Any] ) -> Any:
		"""
		Makes a request with SQL code to the database.
		DO NOT USE VARIABLES IN THE SQL CODE!
		IS **VERY** INSECURE AND CAN CAUSE DATA LOSS!
		:param sqlCode: SQL code
		:param args: arguments for value sanitizing
		:return: a List with the result (can be emtpy)
		"""
		pass
