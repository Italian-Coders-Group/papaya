from abc import ABCMeta, abstractmethod
from typing import Dict

import discord


class AbstractServer(metaclass=ABCMeta):

	guild: discord.Guild
	prefix: str = '!!'
	roleRules: Dict[ str, object ]

	@abstractmethod
	async def handleMsg( self, msg: discord.Message ):
		"""
		Handles a discord message object
		:param msg: message to handle
		"""
		pass

	@abstractmethod
	def Can( self, user: discord.User, permission: str ) -> bool:
		"""
		Check if an user can do something
		:param user: the user to check
		:param permission: the permission to check for
		:return: bool, true if the user has the permission, false otherwise
		"""
		pass
