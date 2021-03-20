from types import FunctionType

from typing import Coroutine, Dict, Awaitable, List, Union

from discord import Message

from core import utils, types
from core.logging import get_logger
from core.abc.server import AbstractServer


logger = get_logger()


class CommandSystem:

	__Commands: Dict[str, types.Coroutine] = {}

	def Command( self, func: Coroutine[ Awaitable[int], AbstractServer, Message ], cname: str = None ):
		"""
		The @decorator for commands
		:param func: coroutine to mark as command
		:param cname: usually None, used to set the command name
		"""
		func: types.Coroutine
		name = func.__code__.co_name.lower()
		self.__Commands[ name if cname is None else cname ] = func
		return func

	def getOrDefault(
			self,
			item: str,
			default: Union[ Coroutine[ int, AbstractServer, Message ], types.Coroutine ]
	) -> Union[ Coroutine[ Awaitable[ int ], AbstractServer, Message ], types.Coroutine ]:
		"""
		Get the specified command or if not found, returns the one given on default
		:param item: the item to get
		:param default: fallback coroutine
		:return: the command or the default coroutine
		"""
		if item in self.__Commands.keys():
			return self.__Commands.get( item )
		else:
			return getattr( self, item, default )


instance: CommandSystem = CommandSystem()


def Command( *args, **kwargs ):
	"""
		The @decorator for commands.
		this decorator may have a parameter: cname,
		cname is the command name to use instead of the decorated coroutine name.
	"""
	# check if called without parameters
	if len( args ) > 0 and type( args[0] ) == FunctionType:
		return instance.Command( args[0], None )

	# called with parameter, get it
	cname: str = kwargs.get( 'cname' ) if 'cname' in kwargs else args[0]

	# return a lambda that calls instance.Command, like above
	return lambda func: instance.Command(func, cname)


logger.debug( 'Registering default commands' )
from . import defaultCommands
logger.debug( 'Registered default commands' )
