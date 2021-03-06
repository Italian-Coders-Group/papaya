import asyncio
from typing import Dict, Callable, Coroutine, Union

from discord import Message
import discord

import logging

from . import Database
from .abc.database.guild import AbstractGuild
from .abc.server import AbstractServer
from .dataclass.PapUser import PapUser
from .logging import get_logger
import core.commandList


defaultPerms = {
	'manage bot': True,
	'start game': True,
	'edit permissions': True,
}


async def DefCommand( server: AbstractServer, msg: discord.Message ) -> int:
	return 1


class Server( AbstractServer ):

	guild: discord.Guild
	prefix: str = '*'
	roleRules: Dict[ str, object ]
	commands: core.commandList.CommandList
	logger: logging.Logger

	def __init__(self, guild: discord.Guild):
		self.guild = guild
		self.logger = get_logger( guild.name )
		self.commands = core.commandList.instance
		self.secondaryPrefix = {
			350938367405457408: '$$'
		}

	async def handleMsg( self, msg: Message ):
		"""
		Handles a discord message object
		:param msg: message to handle
		"""
		# setup
		# user db check
		if not self.GetDatabase().hasUser( msg.author.id ):
			self.GetDatabase().setUser(
				PapUser(
					discordID=msg.author.id,
					personalPrefix=self.prefix,
					permissions=PapUser.serializePermissions( [ x for x in defaultPerms.values() ] )
				)
			)
		prefix = self.prefix
		if not msg.content.startswith( prefix ):
			if msg.author.id not in self.secondaryPrefix.keys():
				self.secondaryPrefix[ msg.author.id ] = self.GetDatabase().getUser( msg.author.id ).personalPrefix
			prefix = self.secondaryPrefix[msg.author.id]
			if not msg.content.startswith( prefix ):
				return
		msg.content = msg.content[ len(prefix): ]
		del prefix
		cmd = msg.content.split( " " )
		self.logger.info(
			f'guild: {self.guild.name}, '
			f'command: {cmd[ 0 ].lower()}, '
			f'parameters: {"".join(cmd).replace(cmd[0], "", 1) if len( cmd ) > 1 else None}, '
			f'issuer: {msg.author.name}'
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

	def Can( self, user: discord.User, permission: str) -> bool:
		"""
		Check if an user can do something
		:param user: the user to check
		:param permission: the permission to check for
		:return: bool, true if the user has the permission, false otherwise
		"""
		return True

	def GetDatabase( self ) -> AbstractGuild:
		"""
		Getter for this guild's database interface
		:return: Database object
		"""
		return Database.instance.getGuild( self.guild.id )
