import asyncio
from core.eventSystem import EventSystem, Events
from core.types import Coroutine
from typing import Dict

from discord import Message, Reaction, Member
import discord

import logging

from . import Database, utils, commandSystem
from .abc.database.guild import AbstractGuild
from .abc.server import AbstractServer
from .dataclass.PapUser import PapUser
from .logging import get_logger


defaultPerms = {
	'manage bot': True,
	'start game': True,
	'edit permissions': True,
}


class Server( AbstractServer ):

	guild: discord.Guild
	prefix: str = '*'
	roleRules: Dict[ str, object ]
	commands: commandSystem.CommandSystem
	logger: logging.Logger

	def __init__(self, guild: discord.Guild):
		self.guild = guild
		self.logger = get_logger( guild.name )
		self.commands = commandSystem.instance
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
					permissions=[ x for x in defaultPerms.values() ]
				)
			)
		await EventSystem.INSTANCE.invoke(
			event=Events.MessageArrived,
			server=self,
			msg=msg
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
		coro: Coroutine = self.commands.getOrDefault( cmd[ 0 ].lower(), None )
		# check if its a command/coroutine
		if ( coro is None ) or ( not asyncio.iscoroutinefunction(coro) ):
			# no command found
			await msg.channel.send( f'Unknown command: {cmd[ 0 ]}' )
			return
		# execute command
		await coro(self, msg)

	async def handleReactionAdd( self, reaction: Reaction, user: Member ) -> None:
		"""
		Handles reacting to a message with an emoji
		:param reaction: the reaction object
		:param user: the user who caused this event
		"""
		self.logger.info(
			f'guild: {self.guild.name}, '
			f'emoji: {reaction.emoji if isinstance(reaction.emoji, str) else reaction.emoji.name}, '
			f'cause: {user.name}'
		)
		await EventSystem.INSTANCE.invoke(
			event=Events.ReactionAdded,
			reaction=reaction,
			cause=user
		)

	async def handleReactionRemove( self, reaction: Reaction, user: Member ) -> None:
		"""
		Handles removing a reaction to a message
		:param reaction: the reaction object
		:param user: the user who caused this event
		"""
		self.logger.info(
			f'guild: {self.guild.name}, '
			f'emoji: {reaction.emoji if isinstance(reaction.emoji, str) else reaction.emoji.name}, '
			f'cause: {user.name}'
		)
		await EventSystem.INSTANCE.invoke(
			event=Events.ReactionRemoved,
			reaction=reaction,
			cause=user
		)

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
