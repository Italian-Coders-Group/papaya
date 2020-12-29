from abc import ABCMeta
from typing import Iterator, Tuple, List, Union

from core.abc.gridsystem.AbstractCell import AbstractCell
from core.abc.gridsystem.AbstractGrid import AbstractGrid


class CellData(metaclass=ABCMeta):
	pass


class Cell(AbstractCell):
	x: int
	y: int
	cellData: CellData

	def __init__(self, x: int, y: int, data: Union[None, CellData]):
		self.x = x
		self.y = y
		self.cellData = data


class OrderedGrid(AbstractGrid):

	_cells: List[Cell]

	def __init__(self, size: Tuple[int, int], initialize: bool = True):
		self._cells = []
		self._size = size
		if initialize:
			self.clear()

	def getCell( self, x: int, y: int ) -> CellData:
		self._check(x, y)
		for i in range( self._cells.__len__() ):
			if self._cells[ i ].x == x and self._cells[ i ].y == y:
				return self._cells[ i ].cellData

	def setCell( self, x: int, y: int, value: CellData ) -> None:
		self._check(x, y)
		for i in range( self._cells.__len__() ):
			if self._cells[i].x == x and self._cells[i].y == y:
				self._cells[i].cellData = value

	def clear( self ) -> None:
		self._cells.clear()
		for x in range(self._size[0]):
			for y in range(self._size[1]):
				self._cells.append( Cell(x, y, None ) )

	def serialize( self ) -> str:
		pass

	def deserialize( self ) -> 'OrderedGrid':
		pass

	def __getitem__( self, k: str ) -> CellData:
		x, y = k.split(',')
		return self.getCell(x, y)

	def __setitem__( self, key: str, value: CellData ) -> None:
		x, y = key.split(',')
		self.setCell(x, y, value)

	def __len__( self ) -> int:
		return self._cells.__len__()

	def __iter__( self ) -> Iterator[ Cell ]:
		return self._cells.__iter__()
