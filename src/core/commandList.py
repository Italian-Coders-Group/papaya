from typing import Coroutine, Dict, Callable, Awaitable

from discord import Message

import core.abc.server
from core.abc.server import AbstractServer


class CommandList:

	__Commands: Dict[str, Coroutine] = {}

	async def echo( self, server: AbstractServer, msg: Message ):
		await msg.channel.send( msg.content.replace('echo', '', 1) )

	async def hello( self, server: AbstractServer, msg: Message ):
		await msg.channel.send( 'hello there!' )

	def Command( self, func: Coroutine[ Awaitable[int], AbstractServer, Message ] ):
		name = func.__code__.co_name.lower()
		self.__Commands[ name ] = func

	def getOrDefault( self, item: str, default: Coroutine[ Awaitable[int], AbstractServer, Message ] ):
		if item in self.__Commands.keys():
			return self.__Commands.get( item )
		else:
			return getattr( self, item, default )