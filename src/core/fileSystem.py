from io import BytesIO,  TextIOWrapper
from pathlib import Path
from typing import  Union, TextIO
from lzma import compress, decompress
import mimetypes

import PIL.Image

from core.abc.fileSystem import AbstractFileSystem, AbstractFile, openingReadMode, openingWriteMode, AbstractFolder
from core.exception import FileSystemError


class File(AbstractFile):
	"""
	Specialized class for file operations.
	this class can:
	- read
	- write
	- read a BytesIO
	- read a StringIO
	- check if file is an image
	"""

	def __init__(self, path: Union[Path, str] = None, data: Union[BytesIO, bytes] = None):
		"""
		Construct a File object
		:param path:
		:param data:
		"""
		if path is not None:
			self.path = path if isinstance(path, Path) else Path(path)
		elif data is not None:
			self.content = data if isinstance(data, BytesIO) else BytesIO(data)
		else:
			pass

	def toBytes( self ) -> bytes:
		"""
		Gets the bytes from this File object
		:return: content in bytes
		"""
		self._read()
		return self.content.read()

	def fromBytes( self, data: bytes, resetPath: bool = True ) -> None:
		"""
		Replace the content of this File obj with the given bytes.
		if resetPath is True (default) removes the path for this obj
		:param data: bytes to write
		:param resetPath: if True, removes the path for this obj
		"""
		if resetPath:
			self.path = None
		self.content = BytesIO( data )

	def read( self, mode: openingReadMode = openingReadMode.readBytes) -> Union[ bytes, str ]:
		"""
		Implementation of read.
		this method can read both text and bytes, given the right openingReadMode
		:param mode: mode to use
		:return: bytes or str
		"""
		self._read()
		self.content.seek(0)
		if mode is openingReadMode.readBytes:
			return self.content.read()
		else:
			data = self.content.read()
			return data.decode()

	def readText( self ) -> str:
		""" This reads text, not much to say """
		return self.read( openingReadMode.readText )

	def readBytes( self ) -> bytes:
		""" This reads bytes, not much to say """
		return self.read( openingReadMode.readBytes )

	def write( self, mode: openingWriteMode, data: Union[ bytes, str ] ) -> None:
		"""
		Implementation of write.
		this method can write both text and bytes, given the right openingWriteMode
		:param mode: mode to use
		:param data: data to write, can be bytes or str
		"""
		self._read()
		self.content.write( data if mode is openingWriteMode.writeBytes else data.encode() )

	def writeText( self, data: str ) -> None:
		"""
		Writes text to this File
		:param data: text to write
		"""
		self.write( openingWriteMode.writeText, data )

	def writeBytes( self, data: bytes ) -> None:
		"""
		Writes bytes to this File
		:param data: bytes to write
		"""
		self.write( openingWriteMode.writeBytes, data )

	def getPath( self ) -> Union[Path, None]:
		""" Gets the path of this file, None if its not on disk """
		return self.path

	def getBytesIO( self ) -> BytesIO:
		"""	Gets the content of this File obj as BytesIO buffer """
		self._read()
		return self.content

	def getTextIO( self ) -> TextIO:
		"""	Gets the content of this File obj as StringIO buffer """
		self._read()
		return TextIOWrapper(self.content)

	def updateFile( self ) -> None:
		""" Updates the file on disk """
		if self.path is None:
			raise RuntimeError('This File object has no disk path!')
		self.content.seek(0)
		self.path.write_bytes( self.content.read() )

	def compress( self ) -> None:
		""" Compresses the content of this File with LZMA """
		self._read()
		if super()._compressed:
			raise RuntimeError('File is already compressed!')
		data: bytes
		try:
			data = compress( self.content.read() )
		except:
			raise
		else:
			self.setCompressed()
			self.content = BytesIO( data )

	def copy( self ) -> AbstractFile:
		"""
		Clones this object
		:return: a copy of this object
		"""
		self._read()
		file = File()
		file.content = BytesIO( self.content.read() ) if isinstance( self.content, BytesIO ) else None
		file.path = Path( self.path ) if isinstance( self.content, Path ) else None
		return file

	def exists( self ) -> bool:
		""" Checks if this file exist on disk """
		if self.path is None:
			return False
		return self.path.exists()

	def touch( self ) -> None:
		"""	Creates this file on disk """
		if self.path is None:
			raise RuntimeError( 'This File object has no disk path!' )
		self.path.touch(exist_ok=True)

	def isFolder( self ) -> bool:
		return False

	def isImage( self ) -> bool:
		"""
		Checks if this File object is pointing to a valid image
		:return: True if it is, False otherwise
		"""
		self._read()
		try:
			PIL.Image.open( fp=self.getBytesIO() )
		except:
			return False
		else:
			return True

	def toImage( self ) -> PIL.Image.Image:
		"""
		Reads a PIL images from this file
		:return: Image obj
		"""
		self._read()
		try:
			image = PIL.Image.open( fp=self.getBytesIO() )
		except:
			raise RuntimeError('The content is not an image!')
		else:
			return image

	def _read( self ) -> None:
		""" private method, do not use """
		if self.content is not None:
			return
		if self.path is not None:
			self.content = BytesIO( self.path.read_bytes() )
		else:
			self.content = BytesIO()

	def __str__(self) -> str:
		return f'File object. file path: { str( self.path.resolve() if isinstance( self.path, Path ) else None ) }'

	def __enter__(self):
		pass

	def __exit__(self, exc_type, exc_val, exc_tb):
		if self.path is not None:
			self.updateFile()

	@staticmethod
	def decompress( compFile: Union[ AbstractFile, bytes ] ) -> AbstractFile:
		"""
		Decompresses a previusly LZMA compressed File object or bytes.
		:param compFile: compressed File or bytes
		:return: decompressed File object
		"""
		if isinstance( compFile, AbstractFile ):
			if not compFile.getCompressed():
				raise RuntimeError( 'Trying to decompress non-compressed data.' )
			compData = compFile.readBytes()
		else:
			compData = compFile
		try:
			data = decompress( compData )
		except:
			raise
		file = File()
		file.content = data
		file.path = compFile.path if isinstance(compFile, File) else None
		return file

	@staticmethod
	def openFile( path: Union[ Path, str ] ) -> AbstractFile:
		"""
		Opens a file and returns a File object, equivalent of File(path)
		:param path: file to open
		:return: File object
		"""
		return File(path=path)


class Folder(File, AbstractFolder):

	def isFolder( self ) -> bool:
		return True

	def walk( self ) -> AbstractFile:
		for file in self.path.glob('*'):
			yield File( file ) if file.is_file() else Folder( file )

	def __iter__( self ):
		pass

	def __next__( self ) -> AbstractFile:
		pass


class FileSystem(AbstractFileSystem):

	def __init__( self, path: Union[Path, str] ):
		if not isinstance(path, Path):
			path = Path(path)
		self.sandbox = path

	def getAsset( self, path: Union[Path, str], layer: int = 0 ) -> AbstractFile:
		if not isinstance(path, Path):
			path = Path(path)

		if path.parts[layer] in self.cache.keys():
			if isinstance( self.cache[ path.parts[layer] ], FileSystem):
				return self.cache[ path.parts[layer] ].getAsset(path, layer + 1)
		try:
			path.relative_to(self.sandbox)
		except:
			raise FileSystemError(f'{str(path)} its not inside {str(self.sandbox)}')

		path = path.relative_to(self.sandbox)

		if '..' in path.parts:
			raise FileSystemError( f'{str( path )} its not inside {str( self.sandbox )}' )

		if path.parts.count('/') > layer:
			folder = FileSystem( path='/'.join( path.parts[:layer + 1] ) )
			if folder.asFile().exists():
				self.cache[ path.parts[ layer ] ] = folder
				return self.cache[ path.parts[layer] ].getAsset(path, layer + 1)
			else:
				raise FileSystemError( f'Unknown path {str( path )}' )
		else:
			self.cache[ path.parts[layer] ] = File(path)
			return self.cache[ path.parts[layer] ]

	def getFolder( self, path: Union[Path, str], layer: int = 0 ) -> AbstractFile:
		pass

	def create( self, path: str ) -> None:
		pass

	def asFolder( self ) -> AbstractFolder:
		self.fileForm = Folder( self.sandbox )
		return self.fileForm

	def __iter__(self):
		pass

	def __next__(self):
		pass

	def __contains__(self, item):
		pass
