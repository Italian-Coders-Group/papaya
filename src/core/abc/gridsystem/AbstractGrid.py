from abc import ABCMeta, abstractmethod
from typing import Iterator, Any, Tuple

from core.abc.gridsystem.AbstractCell import AbstractCell


class AbstractGrid(metaclass=ABCMeta):

	_size: Tuple[ int, int ]

	@abstractmethod
	def getCell( self, x: int, y: int ) -> AbstractCell:
		pass

	@abstractmethod
	def setCell( self, x: int, y: int, value: AbstractCell ) -> None:
		pass

	@abstractmethod
	def clear( self ) -> None:
		pass

	@abstractmethod
	def serialize( self ) -> str:
		pass

	@abstractmethod
	def deserialize( self ) -> 'AbstractGrid':
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

	def _check( self, x: int, y: int ):
		if x > self._size[ 0 ] or y > self._size[ 1 ]:
			raise IndexError( f'index out of range! {x}, {y} > {self._size[ 0 ]}, {self._size[ 1 ]}' )
		if x < 0 or y < 0:
			raise IndexError( f'index out of range! {x}, {y} < 0, 0' )
