from abc import ABCMeta, abstractmethod
from typing import Dict

import discord

from core.abc.database.guild import AbstractGuild


class AbstractServer(metaclass=ABCMeta):

	guild: discord.Guild
	prefix: str = '!!'
	roleRules: Dict[ str, object ]
	secondaryPrefix: Dict[int, str]

	@abstractmethod
	async def handleMsg( self, msg: discord.Message ):
		"""
		Handles a discord message object
		:param msg: message to handle
		"""
		pass

	@abstractmethod
	async def handleReactionAdd( self, reaction: discord.Reaction, user: discord.Member ) -> None:
		"""
		Handles reacting to a message with an emoji
		:param reaction: the reaction object
		:param user: the user who caused this event
		"""

	@abstractmethod
	async def handleReactionRemove( self, reaction: discord.Reaction, user: discord.Member ) -> None:
		"""
		Handles removing a reaction to a message
		:param reaction: the reaction object
		:param user: the user who caused this event
		"""

	@abstractmethod
	def Can( self, user: discord.User, permission: str ) -> bool:
		"""
		Check if an user can do something
		:param user: the user to check
		:param permission: the permission to check for
		:return: bool, true if the user has the permission, false otherwise
		"""
		pass

	@abstractmethod
	def GetDatabase( self ) -> AbstractGuild:
		"""
		Getter for this guild's database interface
		:return: Database object
		"""
		pass
