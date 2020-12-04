from abc import ABCMeta, abstractmethod

import discord
import core


class BasePlayer(metaclass=ABCMeta):

	user: int
	team: int

	async def getUser( self ) -> discord.User:
		return await core.Bot.instance.client.fetch_user(self.user)
