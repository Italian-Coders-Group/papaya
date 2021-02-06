from abc import ABCMeta
from typing import Iterator, Tuple, List, Union

from core.abc.gridsystem.AbstractCell import AbstractCell
from core.abc.gridsystem.AbstractGrid import AbstractGrid


class CellData(metaclass=ABCMeta):
	""" a base cell, please subclass to save data in a cell """
	pass


class Cell(AbstractCell):
	""" Container object for CellData objects and cell position """
	x: int
	y: int
	cellData: CellData

	def __init__(self, x: int, y: int, data: Union[None, CellData]):
		self.x = x
		self.y = y
		self.cellData = data


class OrderedGrid(AbstractGrid):

	_cells: List[Cell]
	_default: CellData = None

	def __init__(self, size: Tuple[int, int], default: CellData = None):
		self._cells = []
		self._size = size
		self._default = default
		self.clear()

	def getCell( self, x: int, y: int ) -> CellData:
		"""
		Gets the cell at X, Y
		:param x: x pos
		:param y: y pos
		:return: that cell's CellData object with its data
		"""
		self._check(x, y)
		for i in range( self._cells.__len__() ):
			if self._cells[ i ].x == x and self._cells[ i ].y == y:
				return self._cells[ i ].cellData

	def setCell( self, x: int, y: int, value: CellData ) -> None:
		"""
		Sets the cell at X, Y
		:param value: a CellData object with data
		:param x: x pos
		:param y: y pos
		"""
		self._check(x, y)
		for i in range( self._cells.__len__() ):
			if self._cells[i].x == x and self._cells[i].y == y:
				self._cells[i].cellData = value

	def clear( self ) -> None:
		""" Clear the grid """
		self._cells.clear()
		for x in range(self._size[0]):
			for y in range(self._size[1]):
				self._cells.append( Cell(x, y, self._default ) )

	def serialize( self ) -> str:
		""" Serialize this grid to a json string """
		pass

	def deserialize( self ) -> 'OrderedGrid':
		""" Deserialize a json string into a grid """
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
