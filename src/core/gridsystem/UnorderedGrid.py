from typing import Tuple, Dict, Iterator

from core.abc.gridsystem.AbstractCell import AbstractCell
from core.abc.gridsystem.AbstractGrid import AbstractGrid


class UnorderedGrid(AbstractGrid):

	_table: Dict[ str, AbstractCell ]
	_default: AbstractCell

	def __init__(self, size: Tuple[int, int], default: AbstractCell = None):
		self._size = size
		self._default = default
		self._table = {}
		self.clear()

	def getCell( self, x: int, y: int ) -> AbstractCell:
		self._check(x, y)
		if f'{x},{y}' in self._table.keys():
			return self._table[f'{x},{y}']
		else:
			return self._default

	def setCell( self, x: int, y: int, value: AbstractCell ) -> None:
		self._check(x, y)
		self._table[f'{x},{y}'] = value

	def clear( self ) -> None:
		for x in range( self._size[ 0 ] ):
			for y in range( self._size[ 1 ] ):
				self._table[ f'{x},{y}' ] = self._default

	def serialize( self ) -> str:
		pass

	def deserialize( self ) -> 'UnorderedGrid':
		pass

	def __getitem__( self, k: str ) -> AbstractCell:
		x, y = k.split(',')
		return self.getCell( int(x), int(y) )

	def __setitem__(self, key: str, value: AbstractCell) -> None:
		x, y = key.split( ',' )
		self.setCell( int(x), int(y), value )

	def __len__( self ) -> int:
		return self._size[0] * self._size[1]

	def __iter__( self ) -> Iterator[ str ]:
		return self._table.__iter__()
