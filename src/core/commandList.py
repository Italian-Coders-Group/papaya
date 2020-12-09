from typing import Coroutine, Dict, Awaitable

from discord import Message

from core.abc.server import AbstractServer


class CommandList:

	__Commands: Dict[str, Coroutine] = {}

	async def echo( self, server: AbstractServer, msg: Message ):
		await msg.channel.send( msg.content.replace('echo', '', 1) )

	async def hello( self, server: AbstractServer, msg: Message ):
		await msg.channel.send( 'hello there!' )

	# INSTANCE METHODS: NOT COMMANDS

	def Command( self, func: Coroutine[ Awaitable[int], AbstractServer, Message ], cname: str = None ):
		"""
		The @decorator for commands
		:param func: coroutine to mark as command
		:param cname: usually None, used to set the command name
		"""
		name = func.__code__.co_name.lower()
		self.__Commands[ name if cname is None else cname ] = func

	def getOrDefault( self, item: str, default: Coroutine[ Awaitable[int], AbstractServer, Message ] ) -> Coroutine[ Awaitable[ int ], AbstractServer, Message ]:
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


instance: CommandList = CommandList()


def Command( func: Coroutine[ Awaitable[ int ], AbstractServer, Message ], cname: str = None ):
	"""
	The @decorator for commands
	:param func: coroutine to mark as command
	:param cname: usually None, used to set the command name
	"""
	instance.Command(func, cname)


def getOrDefault( item: str, default: Coroutine[ Awaitable[ int ], AbstractServer, Message ] ) -> Coroutine[ Awaitable[ int ], AbstractServer, Message ]:
	"""
	Get the specified command or if not found, returns the one given on default
	:param item: the item to get
	:param default: fallback coroutine
	:return: the command or the default coroutine
	"""
	return instance.getOrDefault(item, default)
