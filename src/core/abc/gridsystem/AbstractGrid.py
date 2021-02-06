from abc import ABCMeta, abstractmethod
from typing import Iterator, Any, Tuple

from core.abc.gridsystem.AbstractCell import AbstractCell


class AbstractGrid(metaclass=ABCMeta):

	_size: Tuple[ int, int ]

	@abstractmethod
	def getCell( self, x: int, y: int ) -> AbstractCell:
		"""
		Gets the cell at X, Y
		:param x: x pos
		:param y: y pos
		:return: that cell
		"""
		pass

	@abstractmethod
	def setCell( self, x: int, y: int, value: AbstractCell ) -> None:
		"""
		Sets the cell at X, Y
		:param x: x pos
		:param y: y pos
		"""
		pass

	@abstractmethod
	def clear( self ) -> None:
		""" Clear the grid """
		pass

	@abstractmethod
	def serialize( self ) -> str:
		""" Serialize this grid to a json string """
		pass

	@abstractmethod
	def deserialize( self ) -> 'AbstractGrid':
		""" Deserialize a json string into a grid """
		pass

	@abstractmethod
	def __getitem__( self, k: str ) -> AbstractCell:
		pass

	@abstractmethod
	def __setitem__( self, key: str, value ) -> None:
		pass

	@abstractmethod
	def __len__( self ) -> int:
		pass

	@abstractmethod
	def __iter__( self ) -> Iterator[ Any ]:
		pass

	def _check( self, x: int, y: int ) -> bool:
		"""
		PRIVATE METHOD
		checks if the position X,Y is inside the grid
		:param x: x pos
		:param y: y pos
		:return: True if is a valid position, False otherwise
		"""
		if x > self._size[ 0 ] or y > self._size[ 1 ]:
			raise IndexError( f'index out of range! {x}, {y} > {self._size[ 0 ]}, {self._size[ 1 ]}' )
		if x < 0 or y < 0:
			raise IndexError( f'index out of range! {x}, {y} < 0, 0' )
