from abc import ABCMeta, abstractmethod
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import Dict, Union, TextIO, Final

import discord
from PIL.Image import Image


class openingReadMode(Enum):
	readText = 'r'
	readBytes = 'rb'


class openingWriteMode(Enum):
	writeText = 'w'
	writeBytes = 'wb'


class fileType(Enum):
	folder = 'folder'
	file = 'file'
	both = 'both'


class AbstractFile(metaclass=ABCMeta):

	content: BytesIO = None
	path: Path = None
	defaultReadMode: openingReadMode = openingReadMode.readBytes
	defaultWriteMode: openingWriteMode = openingWriteMode.writeBytes
	_compressed: bool = False

	@abstractmethod
	def toBytes( self ) -> bytes:
		"""
		Gets the bytes from this File object
		:return: content in bytes
		"""
		pass

	@abstractmethod
	def fromBytes( self, data: bytearray ) -> None:
		"""
		Replace the content of this File obj with the given bytes.
		if resetPath is True (default) removes the path for this obj
		:param data: bytes to write
		:param resetPath: if True, removes the path for this obj
		"""
		pass

	@abstractmethod
	def read( self, mode: openingReadMode ) -> Union[bytes, str]:
		"""
		Implementation of read.
		this method can read both text and bytes, given the right openingReadMode
		:param mode: mode to use
		:return: bytes or str
		"""
		pass

	@abstractmethod
	def readText( self ) -> str:
		""" This reads text, not much to say """
		pass

	@abstractmethod
	def readBytes( self ) -> bytes:
		""" This reads bytes, not much to say """
		pass

	@abstractmethod
	def write( self, mode: openingWriteMode, data: Union[bytes, str] ) -> None:
		"""
		Implementation of write.
		this method can write both text and bytes, given the right openingWriteMode
		:param mode: mode to use
		:param data: data to write, can be bytes or str
		"""
		pass

	@abstractmethod
	def writeText( self, data: str ) -> None:
		"""
		Writes text to this File
		:param data: text to write
		"""
		pass

	@abstractmethod
	def writeBytes( self, data: bytes ) -> None:
		"""
		Writes bytes to this File
		:param data: bytes to write
		"""
		pass

	@abstractmethod
	def getPath( self ) -> Union[Path, None]:
		""" Gets the path of this file, None if its not on disk """
		pass

	@abstractmethod
	def getBytesIO( self ) -> BytesIO:
		"""	Gets the content of this File obj as BytesIO buffer """
		pass

	@abstractmethod
	def getTextIO( self ) -> TextIO:
		"""	Gets the content of this File obj as StringIO buffer """
		pass

	@abstractmethod
	def updateFile( self ) -> None:
		""" Updates the file on disk """
		pass

	@abstractmethod
	def compress( self ) -> None:
		""" Compresses the content of this File with LZMA """
		pass

	def setCompressed( self, compressed: bool = True ) -> None:
		""" Private method do not use """
		self._compressed = compressed

	def getCompressed( self ) -> bool:
		""" True if this object has compressed data, False otherwise"""
		return self._compressed

	@abstractmethod
	def copy( self ) -> 'AbstractFile':
		"""
		Clones this object
		:return: a copy of this object
		"""
		pass

	@abstractmethod
	def exists( self ) -> bool:
		""" Checks if this file exist on disk """
		pass

	@abstractmethod
	def touch( self ) -> None:
		"""	Creates this file on disk """
		pass

	@abstractmethod
	def isFolder( self ) -> bool:
		""" Returns false if this is not a folder """
		pass

	@abstractmethod
	def isImage( self ) -> bool:
		"""
		Checks if this File object is pointing to a valid image
		:return: True if it is, False otherwise
		"""
		pass

	@abstractmethod
	def toImage( self ) -> Image:
		"""
		Reads a PIL images from this file
		:return: Image obj
		"""
		pass

	@abstractmethod
	def toDiscord( self, name: str = None, useName: bool = False, spoiler: bool = False ) -> discord.File:
		"""
		Converts this file to a discord file
		:param name: Optional discord file name
		:param useName: True to use the disk's filename
		:param spoiler: Self explanatory
		:return: discord.File
		"""
		pass

	@abstractmethod
	def _read( self ) -> None:
		""" private method, do not use """
		pass

	@abstractmethod
	def __str__(self) -> str:
		pass

	@abstractmethod
	def __enter__(self) -> 'AbstractFile':
		pass

	@abstractmethod
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


class AbstractFolder( metaclass=ABCMeta ):

	path: Path = None

	@abstractmethod
	def walk( self, ftype: fileType = fileType.both ) -> Union[AbstractFile, 'AbstractFolder']:
		pass

	@abstractmethod
	def exists( self ) -> bool:
		""" Checks if this file exist on disk """
		pass

	@abstractmethod
	def touch( self ) -> None:
		"""	Creates this file on disk """
		pass

	@abstractmethod
	def isFolder( self ) -> bool:
		pass

	@abstractmethod
	def __iter__(self):
		pass

	@abstractmethod
	def __next__(self) -> Union[AbstractFile, 'AbstractFolder']:
		pass


class AbstractFileSystem(metaclass=ABCMeta):

	sandbox: Path
	fileForm: AbstractFolder = None
	cache: Dict[str, Union[ AbstractFile, AbstractFolder, 'AbstractFileSystem' ] ] = {}

	@abstractmethod
	def get( self, path: str, ftype: fileType, layer: int = 0 ) -> Union[AbstractFile, AbstractFolder]:
		pass

	@abstractmethod
	def getAsset( self, path: str, layer: int = 0 ) -> AbstractFile:
		pass

	@abstractmethod
	def getFolder( self, path: Union[Path, str], layer: int = 0 ) -> AbstractFolder:
		pass

	@abstractmethod
	def create( self, path: str ) -> None:
		pass

	@abstractmethod
	def asFolder( self ) -> AbstractFolder:
		pass

	@abstractmethod
	def __iter__(self):
		pass

	@abstractmethod
	def __next__(self):
		pass

	@abstractmethod
	def __contains__(self, item) -> bool:
		pass
