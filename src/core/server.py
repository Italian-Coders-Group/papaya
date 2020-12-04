import asyncio
from typing import Dict, Callable, Coroutine, Union

from discord import Message
import discord

import logging

# from . import database
from .abc.server import AbstractServer
from .logging import get_logger
import core.commandList


async def DefCommand( server: AbstractServer, msg: discord.Message ) -> int:
	return 1


class Server( AbstractServer ):

	guild: discord.Guild
	prefix: str = '!'
	roleRules: Dict[ str, object ]
	commands: core.commandList.CommandList
	logger: logging.Logger

	def __init__(self, guild: discord.Guild):
		self.guild = guild
		self.logger = get_logger( guild.name )
		self.commands = core.commandList.CommandList()
		# options = database.loadGuild(guild.id)
		# print(options)

	async def handleMsg( self, msg: Message ):
		# setup
		if not msg.content.startswith( self.prefix ):
			return
		msg.content = msg.content.replace( self.prefix, '', 1 )
		cmd = msg.content.split( " " )
		self.logger.info(
			f'guild: {self.guild.name}, command: {cmd[ 0 ].lower()}, parameters: {cmd[ 1::len( cmd ) - 1 ] if len( cmd ) > 1 else None}, issuer: {msg.author.name} '
		)
		# get function/coroutine
		coro: Union[Coroutine, Callable] = self.commands.getOrDefault( cmd[ 0 ].lower(), DefCommand )
		# check if its a command/coroutine
		if not asyncio.iscoroutinefunction(coro):
			return
		# execute command
		code = await coro(self, msg)
		# check return code
		if code == 1:
			await msg.channel.send( f'Unknown command: {cmd[ 0 ]}' )

	def Can( self, user: discord.User, ):
		pass


def reloadModules():
	import importlib
	importlib.reload( core.commandList )