from io import BytesIO,  TextIOWrapper
from pathlib import Path
from time import time
from typing import Union, TextIO, List
from lzma import compress, decompress

import PIL.Image
import discord

from core.abc.fileSystem import AbstractFileSystem, AbstractFile, openingReadMode, openingWriteMode, AbstractFolder, fileType
from core.exception import FileSystemError


__repoUrl: str = 'https://github.com/Italian-Coders-Group/papaya/raw/main/'


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

	def __init__(self, path: [Path, str] = None, data: [BytesIO, bytes] = None):
		"""
		Construct a File object
		:param path:
		:param data:
		"""
		if path is not None:
			self.path = path if isinstance(path, Path) else Path(path)
			self.lastEdit = float( self.path.stat().st_mtime )
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

	def read( self, mode: openingReadMode = openingReadMode.readBytes) -> [ bytes, str ]:
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

	def write( self, mode: openingWriteMode, data: [ bytes, str ] ) -> None:
		"""
		Implementation of write.
		this method can write both text and bytes, given the right openingWriteMode
		:param mode: mode to use
		:param data: data to write, can be bytes or str
		"""
		self._read()
		self.content.write( data if mode is openingWriteMode.writeBytes else data.encode() )
		self.lastEdit = time()

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

	def getPath( self ) -> [Path, None]:
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
		file.lastEdit = self.lastEdit
		return file

	def exists( self ) -> bool:
		""" Checks if this file exist on disk """
		if self.path is None:
			return False
		return self.path.exists()

	def touch( self ) -> None:
		"""	Creates this file on disk """
		if self.path is None:
			raise FileSystemError( 'This File object has no disk path!' )
		self.path.touch(exist_ok=True)

	def isFolder( self ) -> bool:
		""" Returns false if this is not a folder """
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

	def isDirty( self ) -> bool:
		"""
		Checks if this File object content was modified and not saved to disk
		:raises FileSystemError: if this file doesn't have a disk path
		:return: true if it was
		"""
		if self.lastEdit is None:
			raise FileSystemError( 'This File object has no disk path!' )
		return self.lastEdit > self.path.stat().st_mtime

	def isDiskDirty( self ) -> bool:
		"""
		Checks if this File object content was not synced with the disk
		:return: true if the disk has a more updated copy
		"""
		if self.lastEdit is None:
			raise FileSystemError( 'This File object has no disk path!' )
		return self.lastEdit < self.path.stat().st_mtime

	def toImage( self ) -> PIL.Image.Image:
		"""
		Reads a PIL images from this file
		:return: Image obj
		"""
		self._read()
		try:
			image = PIL.Image.open( fp=self.getBytesIO() )
		except:
			raise RuntimeError('The content is not an image! did you check using isImage?')
		else:
			return image

	def toDiscord( self, name=None, useName: str = False, spoiler: bool = False ) -> discord.File:
		"""
		Converts this file to a discord file
		:param name: Optional discord file name
		:param useName: True to use the disk's filename
		:param spoiler: Self explanatory
		:return: discord.File
		"""
		return discord.File(self.content, filename=self.path.name if useName else name, spoiler=spoiler)

	def toGithubUrl( self ) -> str:
		"""
		Makes the github raw url
		:return: file url on github
		"""
		global __repoUrl
		return f'{__repoUrl}/resources/{self.path}'

	def _read( self, force: bool = False ) -> None:
		""" private method, do not use """
		if self.path is None:
			if self.content is None:
				self.content = BytesIO()
		else:
			if self.lastEdit >= self.path.stat().st_mtime:
				if ( self.content is None ) or ( not force ):
					return
			self.content = BytesIO( self.path.read_bytes() )
			self.lastEdit = self.path.stat().st_mtime

	def __str__(self) -> str:
		return f'<File object of { str( self.path.resolve() if isinstance( self.path, Path ) else None ) }>'

	def __repr__(self) -> str:
		return self.__str__()

	def __enter__(self):
		pass

	def __exit__(self, exc_type, exc_val, exc_tb):
		if self.path is not None:
			self.updateFile()

	@staticmethod
	def decompress( compFile: [ AbstractFile, bytes ] ) -> AbstractFile:
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
	def openFile( path: [ Path, str ] ) -> AbstractFile:
		"""
		Opens a file and returns a File object, equivalent of File(path)
		:param path: file to open
		:return: File object
		"""
		return File(path=path)


class Folder(AbstractFolder):

	def __init__( self, parentFS: AbstractFileSystem, path: [Path, str] ):
		if not isinstance(path, Path):
			path = Path(path)
		if not path.is_dir():
			if path.exists():
				raise FileSystemError('The provided path is not a folder!')
		self._path = path
		self._parentFS = parentFS

	def walk( self, ftype: fileType = fileType.folderOrFile ) -> [AbstractFile, AbstractFolder]:
		""" walk on all folders and files, basically same as Folder.__iter__(), but with a fancy name """
		for file in self._path.glob('*'):
			if file.is_dir():
				if ftype is fileType.folder or fileType.both:
					yield Folder( file )
			elif file.is_file():
				if ftype is fileType.file or fileType.both:
					yield File( file )

	def exists( self ) -> bool:
		""" Checks if this folder exist on disk """
		return self._path.exists()

	def touch( self ) -> None:
		"""	Creates this folder on disk """
		self._path.mkdir()

	def isFolder( self ) -> bool:
		""" returns True if this object represents a folder """
		return True

	def asFileSystem( self ) -> 'AbstractFileSystem':
		""" Returns this folder as a FileSystem obejct """
		return self._parentFS.get( self._path.name, ftype=fileType.fileSystem )

	def listContents( self ) -> List[ Union[ AbstractFile, 'AbstractFolder' ] ]:
		""" Returns a list with all the containing files/folders """
		return [ file for file in self ]

	def getPath( self ) -> Path:
		""" Returns the path of this folder """

	def getParent( self ) -> 'AbstractFolder':
		""" Returns the parent Folder object, if possible """

	def getParentFS( self ) -> 'AbstractFileSystem':
		""" Returns the parent FileSystem object, if possible """

	def __str__(self) -> str:
		return f'<Folder object of { str( self._path.resolve() if isinstance( self._path, Path ) else None ) }>'

	def __repr__(self) -> str:
		return self.__str__()

	def __iter__( self ) -> 'AbstractFolder':
		self.__tmp_iter_array_index = 0
		self.__tmp_iter_array = [ file for file in self._path.glob( '*' ) ]
		return self

	def __next__( self ) -> [AbstractFile, AbstractFolder]:
		if self.__tmp_iter_array_index < len( self.__tmp_iter_array ):
			file = self.__tmp_iter_array[ self.__tmp_iter_array_index ]
			self.__tmp_iter_array_index += 1
			return File( file ) if file.is_file() else Folder( self, file )
		del self.__tmp_iter_array_index
		del self.__tmp_iter_array
		raise StopIteration

	def __contains__(self, item):
		return self._path.joinpath( item ).exists()


class FileSystem(AbstractFileSystem):

	def __init__( self, path: [Path, str] ):
		if not isinstance(path, Path):
			path = Path(path)
		self._sandbox = path.absolute().resolve()
		self.cache = {}

	def get( self, path: [Path, str], ftype: fileType = fileType.file, layer: int = 0 ) -> [AbstractFile, AbstractFolder, AbstractFileSystem]:
		"""
		Gets a file, folder from this on
		:param path: path to file/folder to get
		:param ftype: file type, should be fileType.file or fileType.folder, defaults to fileType.file
		:param layer: PRIVATE PARAMETER
		:return: a File or Folder object
		"""
		# make path a Path obj
		if not isinstance(path, Path):
			path = Path(path)

		# check if the path is in the sandbox
		try:
			if path.name not in self:
				path.relative_to(self._sandbox)
		except:
			raise FileSystemError(f'{str(path)} its not inside {str( self._sandbox )}')

		# recursion things to get a file in a folder
		if len( path.parts ) > layer:
			tmp = Path( '/'.join( path.parts[:layer + 1] ) )
			if tmp.is_dir():
				folder = FileSystem( path=tmp )
				if folder.asFolder().exists():
					self.cache[ path.parts[ layer ] ] = folder
					return self.cache[ path.parts[layer] ].get(path, ftype, layer + 1)
				else:
					raise FileSystemError( f'Unknown path {str( path )}' )

		path = self._sandbox.joinpath(path)

		# get the file/folder/fileSystem object
		if ftype is fileType.folder:
			if path.exists() and ( not path.is_dir() ):
				raise FileSystemError('The specified path points to a file, not a folder')
			self.cache[ path.parts[layer] ] = Folder(self, path)
			return self.cache[ path.parts[layer] ]
		elif ftype is fileType.file:
			if path.exists() and ( not path.is_file() ):
				raise FileSystemError( 'The specified path points to a folder, not a file' )
			self.cache[ path.parts[layer] ] = File(path)
			return self.cache[ path.parts[layer] ]
		elif ftype is fileType.fileSystem:
			return FileSystem(path)
		else:
			raise ValueError(f'Unknown file type "{ftype}"')

	def getResource( self, path: str ) -> AbstractFile:
		"""
		Gets a file from path
		:param path: file path
		:return: File object
		"""
		return self.get(path, ftype=fileType.file)

	def getFolder( self, path: [Path, str] ) -> AbstractFolder:
		"""
		Gets a folder from path
		:param path: folder path
		:return: Folder object
		"""
		return self.get(path, fileType.folder)

	def getParent( self ) -> 'AbstractFileSystem':
		""" Returns the parent FileSystem object, if possible """
		pass

	def create( self, path: str, name: str ) -> None:
		"""
		Creates a folder or file on this path
		NOT IMPLEMENTED
		:param path: path to the folder/file
		:param name: file/folder name
		"""
		raise NotImplementedError()

	def asFolder( self ) -> AbstractFolder:
		"""
		Get this filesystem as folder object
		:return: folder object representing this filesystem path
		"""
		self._folderForm = Folder( None, self._sandbox )
		return self._folderForm

	def __iter__( self ):
		self.__tmp_iter_array_index = 0
		self.__tmp_iter_array = [ file for file in self._sandbox.glob( '*' ) ]
		return self

	def __next__( self ) -> [ AbstractFile, AbstractFolder ]:
		if self.__tmp_iter_array_index < len( self.__tmp_iter_array ):
			file = self.__tmp_iter_array[ self.__tmp_iter_array_index ]
			self.__tmp_iter_array_index += 1
			return File( file ) if file.is_file() else Folder( self, file )
		del self.__tmp_iter_array_index
		del self.__tmp_iter_array
		raise StopIteration

	def __contains__(self, item):
		if item in self.cache:
			return True

		return self._sandbox.joinpath(item).exists()
