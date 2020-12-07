from abc import ABCMeta, abstractmethod as abstract
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import Dict, Union, TextIO

from PIL.Image import Image


class openingReadMode(Enum):
	readText = 'r'
	readBytes = 'rb'


class openingWriteMode(Enum):
	writeText = 'w'
	writeBytes = 'wb'


class AbstractFile(metaclass=ABCMeta):

	content: BytesIO = None
	path: Path = None
	defaultReadMode: openingReadMode = openingReadMode.readBytes
	defaultWriteMode: openingWriteMode = openingWriteMode.writeBytes
	_compressed: bool = False

	@abstract
	def toBytes( self ) -> bytes:
		"""
		Gets the bytes from this File object
		:return: content in bytes
		"""
		pass

	@abstract
	def fromBytes( self, data: bytearray ) -> None:
		"""
		Replace the content of this File obj with the given bytes.
		if resetPath is True (default) removes the path for this obj
		:param data: bytes to write
		:param resetPath: if True, removes the path for this obj
		"""
		pass

	@abstract
	def read( self, mode: openingReadMode ) -> Union[bytes, str]:
		"""
		Implementation of read.
		this method can read both text and bytes, given the right openingReadMode
		:param mode: mode to use
		:return: bytes or str
		"""
		pass

	@abstract
	def readText( self ) -> str:
		""" This reads text, not much to say """
		pass

	@abstract
	def readBytes( self ) -> bytes:
		""" This reads bytes, not much to say """
		pass

	@abstract
	def write( self, mode: openingWriteMode, data: Union[bytes, str] ) -> None:
		"""
		Implementation of write.
		this method can write both text and bytes, given the right openingWriteMode
		:param mode: mode to use
		:param data: data to write, can be bytes or str
		"""
		pass

	@abstract
	def writeText( self, data: str ) -> None:
		"""
		Writes text to this File
		:param data: text to write
		"""
		pass

	@abstract
	def writeBytes( self, data: bytes ) -> None:
		"""
		Writes bytes to this File
		:param data: bytes to write
		"""
		pass

	@abstract
	def getPath( self ) -> Union[Path, None]:
		""" Gets the path of this file, None if its not on disk """
		pass

	@abstract
	def getBytesIO( self ) -> BytesIO:
		"""	Gets the content of this File obj as BytesIO buffer """
		pass

	@abstract
	def getTextIO( self ) -> TextIO:
		"""	Gets the content of this File obj as StringIO buffer """
		pass

	@abstract
	def updateFile( self ) -> None:
		""" Updates the file on disk """
		pass

	@abstract
	def compress( self ) -> None:
		""" Compresses the content of this File with LZMA """
		pass

	def setCompressed( self, compressed: bool = True ) -> None:
		""" Private method do not use """
		self._compressed = compressed

	def getCompressed( self ) -> bool:
		""" True if this object has compressed data, False otherwise"""
		return self._compressed

	@abstract
	def copy( self ) -> 'AbstractFile':
		"""
		Clones this object
		:return: a copy of this object
		"""
		pass

	@abstract
	def exists( self ) -> bool:
		""" Checks if this file exist on disk """
		pass

	@abstract
	def touch( self ) -> None:
		"""	Creates this file on disk """
		pass

	@abstract
	def isImage( self ) -> bool:
		"""
		Checks if this File object is pointing to a valid image
		:return: True if it is, False otherwise
		"""
		pass

	@abstract
	def toImage( self ) -> Image:
		"""
		Reads a PIL images from this file
		:return: Image obj
		"""
		pass

	@abstract
	def _read( self ) -> None:
		""" private method, do not use """
		pass

	@abstract
	def __str__(self) -> str:
		pass

	@abstract
	def __repr__(self) -> str:
		pass

	@abstract
	def __enter__(self) -> 'AbstractFile':
		pass

	@abstract
	def __exit__(self, exc_type, exc_val, exc_tb) -> None:
		pass

	@staticmethod
	def decompress( file: Union[ 'AbstractFile', bytes ] ) -> 'AbstractFile':
		"""
		Decompresses a previusly LZMA compressed File object or bytes.
		:param compFile: compressed File or bytes
		:return: decompressed File object
		"""
		pass

	@staticmethod
	def openFile( path: Union[Path, str] ) -> 'AbstractFile':
		"""
		Opens a file and returns a File object, equivalent of File(path)
		:param path: file to open
		:return: File object
		"""
		pass


class AbstractFileSystem(metaclass=ABCMeta):

	sandbox: Path
	cache: Dict[str, AbstractFile] = {}

	@abstract
	def getAsset( self, path: str ) -> AbstractFile:
		pass

	@abstract
	def getImage( self, path: str ) -> Image:
		pass

	@abstract
	def create( self, path: str ) -> None:
		pass

	@abstract
	def __iter__(self):
		pass

	@abstract
	def __next__(self):
		pass

	@abstract
	def __contains__(self, item) -> bool:
		pass
