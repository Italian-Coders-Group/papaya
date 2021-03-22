from pathlib import Path

from core.abc.fileSystem import AbstractFileSystem
from core.fileSystem import FileSystem

resources: AbstractFileSystem = FileSystem( Path('../../resources') )
images: FileSystem = resources.getFolder('images')
