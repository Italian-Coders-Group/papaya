import importlib
import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Dict

from core import moduleUtils, utils
from core.utils import placeHolderFunc
from core.eventSystem import Listener

__games: Dict[str, ModuleType] = {}


def initializeGames():
	"""	Initialize all games in the modules package	"""
	for file in Path(__file__).parent.glob('*'):
		if file.is_file() or file.name == '__pycache__':
			continue
		moduleName = f'modules.{file.name}'
		module = importlib.import_module( moduleName )
		__games[moduleName] = module


@Listener
async def onReload():
	"""	Reload all instatiated games """
	for game in utils.copyList( __games.keys() ):
		getattr(__games[game], 'reloadModules', placeHolderFunc)()
		moduleUtils.reload(__games[game], __games)


def reloadGame(name: str):
	"""
	Reload the game name
	:param name: package/game to reload
	"""
	if name in __games.keys():
		getattr( __games[ name ], 'reloadModules', placeHolderFunc )()
		moduleUtils.reload(__games[name], __games)
