from abc import ABCMeta, abstractmethod

import discord


class AbstractServer(metaclass=ABCMeta):

	@abstractmethod
	async def handleMsg( self, msg: discord.Message ):
		pass

	@abstractmethod
	def Can( self, user: discord.User, permission: str ) -> bool:
		pass
